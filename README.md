# DripShot

This website takes a picture of the outfit you are currently wearing to give you cafe recommendations based on the outfit you are wearing! 

## Implementation Description

1. Data Scraping (폴더명)
   - https://www.musinsa.com/snap/main/recommend (Style/Images)
   - https://map.naver.com/p/search/%EC%84%B1%EC%88%98%EC%97%AD%20%EC%B9%B4%ED%8E%98?c=14.00,0,0,0,dh (Cafes) 
2. CNN Model
   - Experimentations are located at CNN_Experimentations
   	-  ResNet-18
   	-  EfficientNet
   - Final Classification model located at CNN_Models
   	- Outputs JSON file with vector filled with [classification probabilities](CNN_Model/Classification_Results/classification_results.json)
   	- [Top_Classification_probabilities](CNN_Model/Classification_Results/top_classification_results.json) used in final implementation
3. NLP
   - Bert
   - 
4. Website
   - 설명할것




## Authors

Minseo Kim (DA), Dogeun Im (DA), Jiyeon Seo (DA), Isaac Chung (DE), Jaebin Cheong (DS)

## Version History

### 0.1
- **Initial Release**
  - Location: 성수역 / Seong-Su Station Only

## Acknowledgments

Inspiration, code snippets, etc.
* https://github.com/danielgatis/rembg
