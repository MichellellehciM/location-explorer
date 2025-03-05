from django.http import JsonResponse
import requests
import os

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

def get_location(request):
    """查詢 Google Places API，取得地點資訊，並回傳天氣"""
    place_name = request.GET.get("place", "").strip()
    
    if not place_name:
        return JsonResponse({"error": "Missing place parameter"}, status=400)

    google_url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location"
    }
    body = {"textQuery": place_name, "languageCode": "zh-TW"}

    try:
        response = requests.post(google_url, headers=headers, json=body)
        data = response.json()

        if "places" not in data or not data["places"]:
            return JsonResponse({"error": "No places found"}, status=404)

        # ✅ 取得第一筆地點資訊
        place_data = data["places"][0]
        location_name = place_data["displayName"]["text"]
        location_address = place_data["formattedAddress"]
        latitude = place_data["location"]["latitude"]
        longitude = place_data["location"]["longitude"]

        print(f"🔍 Google Maps 找到地點: {location_name}（{location_address}）")
        print(f"📍 經緯度: {latitude}, {longitude}")

        # ✅ 查詢 Weather API
        weather_info = get_weather(latitude, longitude)

        # ✅ 組合回應資料
        result = {
            "location": {
                "name": location_name,
                "address": location_address
            },
            "weather": weather_info if weather_info else {"error": "Weather data not available"}
        }

        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
