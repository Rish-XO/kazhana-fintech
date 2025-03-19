# FastAPI Backend for Investment Dashboard

## 📌 Overview
This is a **FastAPI backend** that serves investment-related data, including:
- **Performance Metrics**
- **Sector Allocations**
- **Fund Overlaps (Sankey Chart Data)**

It connects to a **PostgreSQL database hosted on Supabase** and provides APIs for frontend consumption.

---

## 🚀 Getting Started
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-repo-url.git
cd your-backend-folder
```

### **2️⃣ Create a Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Configure Environment Variables**
Create a `.env` file in the root folder and add the following:
```env
DATABASE_URL=postgresql://your-user:your-password@your-supabase-url:5432/your-database
CORS_ORIGINS=["*"]  # Replace with frontend URL after deployment
```
send me mail at rishal.mhd009@gmail.com for env file

### **5️⃣ Run Migrations (if using Alembic)**
```sh
alembic upgrade head
```

### **6️⃣ Start the Server**
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
The API will be available at: `http://127.0.0.1:8000`

---

## 📡 API Endpoints
### **Swagger Documentation**
Visit `http://127.0.0.1:8000/docs` to explore APIs interactively.

### **1️⃣ Performance Summary**
**Endpoint:** `GET /performance_summary?timeframe=1M`

_Response Example:_
```json
{
  "current_investment_value": 500000,
  "initial_investment_value": 400000,
  "history": [
    {"date": "2024-01-01", "value": 450000},
    {"date": "2024-02-01", "value": 480000}
  ]
}
```

### **2️⃣ Sector Allocation**
**Endpoint:** `GET /sector_allocation`

_Response Example:_
```json
[
  {
    "name": "Financials",
    "amount": 3300000,
    "percentage": 35.0,
    "sub_allocations": [
      {"name": "HDFC Bank", "percentage": 22.0, "amount": 370000},
      {"name": "ICICI Bank", "percentage": 15.0, "amount": 370000}
    ]
  }
]
```

### **3️⃣ Fund Overlaps (Sankey Data)**
**Endpoint:** `GET /fund_overlap`

_Response Example:_
```json
{
  "nodes": [
    {"name": "Nippon Large Cap Fund"},
    {"name": "HDFC Large Cap Fund"},
    {"name": "Reliance Industries"}
  ],
  "links": [
    {"source": 0, "target": 2, "value": 8},
    {"source": 1, "target": 2, "value": 6}
  ]
}
```

---

## 📦 Deployment
### **Deploy on Render (Recommended)**
1. **Create an account** on [Render.com](https://render.com)
2. **Create a new Web Service**
3. **Connect GitHub repository**
4. **Set Start Command:**
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
5. **Set environment variables** (same as `.env`)
6. **Deploy** and get the public URL!

### **Alternative: Deploy on Railway.app**
1. **Sign up at** [Railway.app](https://railway.app)
2. **Create a new project**
3. **Deploy from GitHub repository**
4. **Set environment variables** (`DATABASE_URL`, etc.)
5. **Deploy and get the backend URL**

---

## 📜 License
This project is licensed under the MIT License.

### ✨ **Contributors**
Maintained by **[Your Name]** 🚀

