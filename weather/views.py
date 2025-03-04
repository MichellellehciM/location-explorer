import requests
import os
from django.http import JsonResponse
from dotenv import load_dotenv

# 載入 .env 變數
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(request):
    """查詢天氣資訊"""
    location = request.GET.get("location", "").strip()
    
    if not location:
        return JsonResponse({"error": "Missing location parameter"}, status=400)

    # 1️⃣ 先使用 WeatherAPI 的地點搜尋 API 獲取城市的標準名稱 & 經緯度
    search_url = f"http://api.weatherapi.com/v1/search.json?key={WEATHER_API_KEY}&q={location}"
    search_response = requests.get(search_url)
    search_data = search_response.json()

    if not search_data:
        return JsonResponse({"error": "Location not found in WeatherAPI"}, status=404)

    # 取得第一個匹配的城市
    city_data = search_data[0]
    lat, lon = city_data["lat"], city_data["lon"]
    city_name = city_data["name"]
    country = city_data["country"]

    # 2️⃣ 再用經緯度查詢天氣
    weather_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={lat},{lon}&lang=zh"

    try:
        response = requests.get(weather_url)
        data = response.json()

        if response.status_code != 200 or "current" not in data:
            return JsonResponse({"error": "Weather data not found", "details": data}, status=404)

        # 格式化回傳資料
        formatted_data = {
            "location": city_name,
            "country": country,
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "humidity": data["current"]["humidity"],
            "wind_kph": data["current"]["wind_kph"]
        }

        return JsonResponse({"results": formatted_data})

    except Exception as e:
        return JsonResponse({"error": "Server error", "details": str(e)}, status=500)
