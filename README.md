# Customer Operations Simulator

A full-stack, real-time simulation platform for customer operations teams. This project combines backend automation (FastAPI) and an interactive dashboard (Streamlit) to simulate rule-based portfolio operations, ticket handling, and performance analytics.

---

## 🚀 Features

### 🔧 Backend (FastAPI)
- Customer and Rule Simulation Engine
- Daily Rule Execution with Log Tracking
- Support Ticket Auto-Generation on Failure
- Status Update API for Ticket Management
- MySQL Database Integration
- Scheduled Background Tasks with APScheduler

### 📊 Frontend (Streamlit)
- Dashboard for Executions, Tickets, and KPIs
- Filters by Customer Priority, Status, Name
- Success/Failure Bar Chart (Stacked Altair)
- Execution Trend Line Chart (Daily View)
- CSV Export for Reporting
- Summary Tables and Drilldowns

---

## 🗂️ Project Structure

```
customer_ops_simulator/
├── main.py                  # FastAPI app entrypoint
├── db.py                   # MySQL connection handler
├── engine.py               # Rule execution logic
├── scheduler.py            # Background job scheduler
├── routers/                # FastAPI routes
│   ├── customers.py
│   ├── rules.py
│   ├── logs.py
│   └── tickets.py
├── dashboard/              # Streamlit app
│   └── dashboard.py
├── requirements.txt        # Python dependencies
├── .gitignore              # Ignore venv, cache, .env, etc
└── README.md               # Project overview
```

---

## 🧪 Tech Stack

- **Backend**: FastAPI, MySQL, SQLAlchemy
- **Frontend**: Streamlit, Altair, Pandas
- **Scheduler**: APScheduler
- **Deployment**: Render (or local via Uvicorn/Streamlit)

---

## ⚙️ Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/customer-ops-simulator.git
cd customer-ops-simulator
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Database
- Ensure MySQL is running locally.
- Create database: `customer_ops_simulator`
- Update `db.py` with your DB credentials

### 5. Run Backend (FastAPI)
```bash
uvicorn main:app --reload
```

### 6. Run Dashboard (Streamlit)
```bash
streamlit run dashboard/dashboard.py
```

---

## 🌐 Deployment

### Render Setup:
- **Web Service 1** (FastAPI): `main.py`
- **Web Service 2** (Streamlit): `dashboard/dashboard.py`
- Add `requirements.txt`, set ports to 10000/10001 respectively

---

## 📷 Screenshots

| Dashboard Overview | Execution Trend | Success/Failure Chart |
|--------------------|------------------|------------------------|
| ![overview](images/overview.png) | ![trend](images/trend.png) | ![bars](images/barchart.png) |

---

## 📤 Data Exports
- Execution logs are exportable as `.csv`
- Success/Failure summary available for reports

---

## 🤝 Author & Credits

**Sahran Altaf**  
Data Science & Robotics @ Symbiosis Institute of Technology  
GitHub: [DarSahran](https://github.com/DarSahran)

---

## 📜 License

MIT License. Free to use, improve, and distribute.