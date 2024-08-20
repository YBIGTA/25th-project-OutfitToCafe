import torch
from torchvision import models, transforms
from PIL import Image
import torch.nn.functional as F
from rembg import remove
import io
import json

### To run this model the following commands must be downloaded (Assuming you already have downloaded other packages) 
"""
For CNN Model:
pip install —upgrade torch torchvision 
pip install —upgrade certifi
/Applications/Python\ 3.x/Install\ Certificates.command    (x 는 파이썬 (python)버전 번호로 바꾸면 됩니다!) 

For Background Removal
pip install rembg 
또한 https://onnxruntime.ai/를 확인하면서 다운받기 
(press Get Started at the top of the site and then click on the platforms to see how to download onnxruntime through bash/powershell) 
For clearer instructions: please reference: https://github.com/danielgatis/rembg
"""

# Loading our trained model
model_save_path = '/Users/dennycheong/24 여름방학/YBIGTA/신입플/CNN_Model/blur_best_efficientnetb0.pth'
efficientnet = models.efficientnet_b0(weights=None)

# 12 different classes 
num_classes = 12
efficientnet.classifier = torch.nn.Sequential(
    torch.nn.Dropout(0.4),
    torch.nn.Linear(efficientnet.classifier[1].in_features, num_classes)
)

# Loading the model weights/parameters that I trained with efficientnet
efficientnet.load_state_dict(torch.load(model_save_path, map_location=torch.device('cpu')))

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
efficientnet = efficientnet.to(device)

efficientnet.eval()

# Preprocessing for the image
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Load the image and remove the background
img_path = '/Users/dennycheong/24 여름방학/YBIGTA/신입플/CNN_Model/Sample_Image/sample_image.jpg'
with open(img_path, 'rb') as img_file:
    img_data = img_file.read()

# Applying the background removal 
removed_bg_data = remove(img_data)

# Convert the removed background data back to an image
image_without_bg = Image.open(io.BytesIO(removed_bg_data)).convert('RGB')

# Preprocessing the image with the ones described above
input_tensor = preprocess(image_without_bg)
input_batch = input_tensor.unsqueeze(0).to(device)  

# We use our model to this file
with torch.no_grad():
    output = efficientnet(input_batch)

# Apply softmax to get probabilities of the classes
probabilities = F.softmax(output, dim=1)

# Converting them to numpy array
probabilities = probabilities.cpu().numpy().flatten()

# Replacing Class 0-11 with actual names of the classes
idx_to_class = {0: "캐주얼", 1: "시크", 2: "시티보이", 3: "클래식", 4: "걸리시", 5: "미니멀", 
                6: "레트로", 7: "로맨틱", 8: "스포티", 9: "스트릿", 10: "워크웨어", 11: "고프코어"}

class_probabilities = {idx_to_class[i]: 0.0 for i in range(len(idx_to_class))} 

# Turning them into proper class probabilities
# We also change their type so it can be properly outputted in the json file
for i in range(len(probabilities)):
    class_probabilities[idx_to_class[i]] = float(probabilities[i])

# Convert to proper json file 
json_output_path = '/Users/dennycheong/24 여름방학/YBIGTA/신입플/CNN_Model/Classification_Results/classification_results.json'
with open(json_output_path, 'w', encoding='utf-8') as json_file:
    json.dump(class_probabilities, json_file, ensure_ascii=False, indent=4)

print(f"Classification results saved to {json_output_path}")
