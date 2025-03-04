# from django.shortcuts import render
from dotenv import load_dotenv
from django.http import JsonResponse

import requests
import os

# Create your views here.
load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def search_place(request):
     # 確保使用者有傳遞 place 參數
    place_name = request.GET.get("place","")
    if not place_name:
        return JsonResponse({"error": "Missing place parameter"}, status=400)

    google_url="https://places.googleapis.com/v1/places:searchText"


    headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY,
    "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.priceLevel"
    }

    body = {
        "textQuery": place_name,
        "languageCode": "zh-TW",
    }

    try:
        response = requests.post(google_url, headers=headers, json=body)
        # json() 是 requests.Response 物件的方法，將 response 的內容轉換成 Python 的字典
        data = response.json()
        if response.status_code != 200:
            return JsonResponse({"error": "API request failed", "details": data}, status=response.status_code)

        # 如果data這個字典裡沒有"places"這個key, 條件=True ; 如果 data["places"] value 是空的（[]、None、""、False），則條件為 True
        if "places" not in data or not data["places"]:
            return JsonResponse({"error": "No places found"}, status=404)
        

        # ✅ 美化回傳資料
        formatted_data = [
            {
                "name": place["displayName"]["text"],
                "address": place["formattedAddress"]
            }
            for place in data["places"]
        ]
        return JsonResponse({"results": formatted_data})
    
    except Exception as e:
        return JsonResponse({"error": "Server error", "details": str(e)}, status=500)
    