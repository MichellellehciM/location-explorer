from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse, HttpResponse
import requests
import os
from dotenv import load_dotenv


load_dotenv()

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

        # Google Maps Geocoding
        geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={GOOGLE_MAPS_API_KEY}"
        geo_res = requests.get(geo_url).json()

        if geo_res.get("status") != "OK":
            return JsonResponse({"error": "無法找到地點資訊"}, status=400)

        first_result = geo_res["results"][0]
        location_name = place
        address = first_result.get("formatted_address", "未知地址")
        lat = first_result["geometry"]["location"]["lat"]
        lng = first_result["geometry"]["location"]["lng"]

        # 查詢天氣
        weather = get_weather(lat, lng)
        if not weather:
            return JsonResponse({"error": "無法取得天氣資料"}, status=400)

        # 回傳結構整理好的 JSON
        return JsonResponse({
            "location": {
                "name": location_name,
                "address": address,
                "lat": lat,
                "lng": lng
            },
            "weather": weather
        })


def home(request):
    return HttpResponse("Welcome to the API home page")
