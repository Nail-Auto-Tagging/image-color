import requests
import numpy as np
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
from pymongo import MongoClient, ReadPreference
from utils import RGB_to_Hex, closest_color, convert_color_to_num


mongo_client = MongoClient("mongodb+srv://NailedItReadWrite:nailedit0916@nailedit.cpmjygq.mongodb.net/nailedit")
colors_read_db = mongo_client.get_database("nailedit", read_preference=ReadPreference.SECONDARY).get_collection("colors")
colors_write_db = mongo_client["nailedit"]["colors"]


if __name__ == '__main__':
    
    db_cursor = None
    limit = 100
    sort = [("member", 1), ("cropped_id", 1)]
    projection = {
        "_id": False, 
        "image": True,
        "cropped_id": True, 
    }
    search_query = {
        "member": "", 
        "is_tagged": False, 
        "colors": []
    }

    while True:
        if db_cursor:
            search_query["cropped_id"] = {"$gt": db_cursor}
            
        cropped_nails = list(
            colors_read_db.find(search_query, projection).sort(sort).limit(limit)
        )

        if not cropped_nails:
            break
        
        db_cursor = cropped_nails[-1]["cropped_id"]
        
        for cropped_nail in cropped_nails:
            print(cropped_nail["image"])
            try:
                image_uri = cropped_nail["image"]            
                binary_image = requests.get(image_uri).content
                image_data = Image.open(BytesIO(binary_image))
                
                # 추출할 기본 색상의 수
                num_colors = 2
                result = image_data.convert("P", palette=Image.ADAPTIVE, colors=num_colors)
                result = result.convert('RGB')
                main_colors = result.getcolors()
                main_colors.sort(reverse=True);
                col_extract = []
                
                # 추출된 기본 색상을 표시합니다.
                for count, rgb_color in main_colors:
                    color_code = RGB_to_Hex(rgb_color)
                    
                closest_color_name = closest_color(rgb_color)
                # print("이미지에서 가장 큰 비율의 색상 식별：" + color_code)
                # print("비슷한 색：" + closest_color_name)
                
                closest_color_num = convert_color_to_num(closest_color_name)
                
                if closest_color_num:
                    search_query = {"cropped_id": cropped_nail["cropped_id"]}
                    update_query = {"$set": {"colors": [closest_color_num]}}
                    colors_write_db.update_one(search_query, update_query, upsert=False)
            except Exception as e:
                print(e.__str__())
                continue
            
            # col_extract.append([col[i] / 255 for i in range(3)])
            
            # 추출된 기본 색상을 표시합니다.
            # plt.figure(dpi=150)
            # plt.bar(range(len(col_extract)), np.ones(len(col_extract)), color=(col_extract))
            # plt.xticks(range(len(col_extract)), (range(len(col_extract))))
            # plt.tight_layout()
            # plt.show()
