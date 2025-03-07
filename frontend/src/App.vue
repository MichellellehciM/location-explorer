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
      params: { place: place.value }
    });
    result.value = response.data;
  } catch (err) {
    error.value = "查詢失敗，請檢查 API 是否正確運作";
  }
};
</script>

<template>
  <div class="container">
    <h1>地點 & 天氣查詢</h1>
    
    <input v-model="place" placeholder="輸入地點名稱，如台北101" />
    <button @click="searchPlace">查詢</button>

    <p v-if="error" class="error">{{ error }}</p>

    <div v-if="result">
      <h2>📍 地點資訊</h2>
      <p><strong>名稱：</strong>{{ result.location.name }}</p>
      <p><strong>地址：</strong>{{ result.location.address }}</p>

      <h2>🌤 天氣資訊</h2>
      <p><strong>溫度：</strong>{{ result.weather.temperature }}°C</p>
      <p><strong>天氣狀況：</strong>{{ result.weather.condition }}</p>
      <p><strong>濕度：</strong>{{ result.weather.humidity }}%</p>
      <p><strong>風速：</strong>{{ result.weather.wind_kph }} km/h</p>
    </div>
  </div>
</template>

<style>
.container {
  max-width: 500px;
  margin: 20px auto;
  padding: 20px;
  text-align: center;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
}

input {
  padding: 8px;
  width: 80%;
  margin-bottom: 10px;
}

button {
  padding: 8px 15px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #36996b;
}

.error {
  color: red;
}
</style>
