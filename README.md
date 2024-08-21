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
   	- Outputs JSON file with vector filled with classification probabilities \\
[View classification_results.json](CNN_Model/Classification_Results/classification_results.json)
   	- Top_Classification_probabilities used in final implemnentation
3. NLP
   - Bert
   - 
4. Final Results




## Executing program

# Website Backend

# Website Frontend





## Authors

Minseo Kim, Dogeun Im, Jiyeon Seo, Isaac Chung, Jaebin Cheong

## Version History

* 0.1
	* Initial Release (성수역/Seong-Su Station Only)

## Acknowledgments

Inspiration, code snippets, etc.
* https://github.com/danielgatis/rembg
