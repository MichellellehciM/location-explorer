from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
import requests
import json
import os
from django.http import HttpResponse



# 讀取 API 金鑰
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(latitude, longitude):
    """查詢 Weather API，取得天氣資訊"""
    weather_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={latitude},{longitude}&lang=zh"
    
    try:
        response = requests.get(weather_url) 
        data = response.json()

        if "current" not in data:
            return None  # ❌ 沒找到天氣資訊
        
        return {
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "humidity": data["current"]["humidity"],
            "wind_kph": data["current"]["wind_kph"]
        }
    except Exception as e:
        return {"error": str(e)}


@method_decorator(csrf_exempt, name='dispatch') 
class SearchView(View):  
    def get(self, request):
        place = request.GET.get("place")
        if not place:
            return JsonResponse({"error": "缺少 place 參數"}, status=400)

        geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={GOOGLE_MAPS_API_KEY}"
        geo_res = requests.get(geo_url).json()

        if geo_res.get("status") != "OK":
            return JsonResponse({"error": geo_res}, status=400)

        result = geo_res["results"][0]
        lat = result["geometry"]["location"]["lat"]
        lng = result["geometry"]["location"]["lng"]
        address = result["formatted_address"]

        # 再查天氣
        weather = get_weather(lat, lng)

        return JsonResponse({
            "location": {
                "name": place,
                "address": address,
                "lat": lat,
                "lng": lng,
            },
            "weather": weather
        })


def get(self, request):
    place = request.GET.get("place")
    if not place:
        return JsonResponse({"error": "缺少 place 參數"}, status=400)

    # Google Maps API 的邏輯（Geocoding）
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={api_key}"
    geo_res = requests.get(geo_url).json()

    if geo_res.get("status") != "OK":
        return JsonResponse({"error": geo_res}, status=400)

    # 傳回第一筆結果
    return JsonResponse({"result": geo_res["results"][0]})


def home(request):
    return HttpResponse("Welcome to the API home page")

