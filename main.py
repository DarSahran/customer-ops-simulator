from fastapi import FastAPI
from routers import customers, rules, logs, tickets
import threading
from scheduler import start_scheduler

app = FastAPI(title="Customer Ops Simulator API")

app.include_router(customers.router)
app.include_router(rules.router)
app.include_router(logs.router)
app.include_router(tickets.router)

# Start scheduler in background
threading.Thread(target=start_scheduler, daemon=True).start()
print("Routers loaded: /customers /rules /logs /tickets")
