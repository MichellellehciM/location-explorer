# **Location Explorer 專案介紹**
Location Explorer 是一個前後端分離的專案，前端使用 Vue 3，後端採用 Django REST Framework，負責提供 API 服務。專案的核心功能是讓使用者輸入地點名稱，查詢該地點的詳細資訊與天氣狀況。

後端部分整合 Google Places API 查詢地點資訊，並串接 Weather API 取得即時天氣數據。API 回應格式包含地點名稱、地址、當前溫度、天氣狀況、濕度與風速等資訊。此外，專案採用 django-cors-headers 解決 CORS 問題，確保前後端通訊順暢。

前端透過 Vite 建立 Vue 專案，並使用 Axios 與後端 API 互動。使用者可以輸入地點名稱，按下查詢按鈕後，畫面會顯示地點與天氣資訊，並適當處理 API 錯誤或無法查詢的情況。

前後端相互獨立，未來可擴展至更多地點資訊或地圖顯示功能，提升使用者體驗與系統靈活性。



## **📖 簡介**
此專案使用 **Django 後端 API** 搭配 **Vue 前端**，讓使用者輸入地點名稱，即可查詢：
- **地點資訊**（Google Places API）
- **即時天氣**（Weather API）
- **前端即時顯示查詢結果**

**架構：Django (REST API) + Vue (前端) + Vite (開發環境)**

---

## **📌 目標**
開發一個 **地點與天氣 API 應用**，提供：
1. **地點查詢**（Google Places API）
2. **即時天氣資訊**（Weather API）
3. **前後端分離設計**

---

## **📌 技術棧**
1. **後端**：Django REST Framework  
2. **前端**：Vue 3 + Vite  
3. **API 整合**：
   - Google Places API（地點查詢）
   - Weather API（天氣查詢）
4. **部署方式**
   - 本地開發：Django runserver + Vite
   - 部署：(尚未)

---

## **🔧 安裝與使用**
### **1️⃣ clone 此專案**
```bash
git clone https://github.com/MichellellehciM/location-explorer.git
cd location-explorer
```

### **2️⃣ 設定後端（Django）**
```
cd backend
poetry install
```

### **3️⃣ 設定後端（Django）**
```
GOOGLE_MAPS_API_KEY=
WEATHER_API_KEY=
```

### **4️⃣ 啟動 Django 伺服器 **
```
poetry run python manage.py migrate
poetry run python manage.py runserver
```

### **5️⃣ 設定前端（Vue） **
```
cd frontend
npm install
npm run dev
```
Vue 伺服器運行 http://localhost:5173/

### ** 測試 **
讓使用者輸入地點名稱（如：台北101、高雄85大樓），點擊「查詢」按鈕
![image](https://github.com/user-attachments/assets/3e34ccae-5ade-486a-ba6d-85f75a68859f)
顯示地點資訊 & 天氣資訊
![image](https://github.com/user-attachments/assets/e7399926-07df-414d-8926-c9b455ee1030)

