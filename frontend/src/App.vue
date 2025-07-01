<script setup>
import { ref } from "vue";
import axios from "axios";

const place = ref("");
const result = ref(null);
const error = ref("");

const searchPlace = async () => {
  if (!place.value.trim()) {
    error.value = "請輸入地點名稱";
    return;
  }

  error.value = "";
  result.value = null;

  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/search/`, {
      params: { place: place.value },
    });
    result.value = response.data;
  } catch (err) {
    error.value = "查詢失敗，請檢查 API 是否正確運作";
  }
};
</script>

<template>
  <div class="container">
    <h1>📍即時天氣查詢📍</h1>
    <h4>想知道他/她在的地方天氣是怎麼樣的嗎</h4>

    <input v-model="place" placeholder="輸入地點名稱，如台北101" />
    <button @click="searchPlace">查天氣</button>

    <p v-if="error" class="error">{{ error }}</p>

    <div v-if="result" class="result-box">
      <h2>🌎 地點資訊</h2>
      <p class="info"><strong>名稱：</strong>{{ result.location.name }}</p>
      <p class="info"><strong>地址：</strong>{{ result.location.address }}</p>

      <h2>🌤 天氣資訊</h2>
      <p class="info"><strong>溫度：</strong>{{ result.weather.temperature }}°C</p>
      <p class="info"><strong>天氣狀況：</strong>{{ result.weather.condition }}</p>
      <p class="info"><strong>濕度：</strong>{{ result.weather.humidity }}%</p>
      <p class="info"><strong>風速：</strong>{{ result.weather.wind_kph }} km/h</p>
    </div>
  </div>
</template>

<style>
.container {
  background: rgba(61, 4, 4, 0.181); 
  padding: 2rem 4rem;
  border-radius: 16px; 
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); 
  backdrop-filter: blur(4px); /* 背後模糊 */
  margin: 0 auto;
}


input {
  padding: 8px;
  width: 80%;
  margin-bottom: 10px;
}

button {
  padding: 8px 15px;
  background-color: #d16cbd;        
  color: white;
  font-weight: bold;
  border: 2px solid white;           /* 白色內邊 */
  box-shadow: 0 0 0 2px black;       /* 黑色外框 */
  border-radius: 10px;               
  cursor: pointer;
  margin-left: 10px;
}

button:hover {
  background-color: #a11a98;
}

.error {
  color: red;
}

.result-box {
  text-align: left;
  margin-top: 20px;
}

.info {
  color: #ffffff; 
  font-weight: bold;
}
body {
  margin: 0;
  padding: 0;
  background-image: url("/pinkcloud.jpg");
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  background-attachment: fixed;
}
</style>
