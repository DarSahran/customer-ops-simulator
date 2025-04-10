from fastapi import APIRouter
from db import get_db_connection

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("/")
def get_customers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    result = cursor.fetchall()
    conn.close()
    return result
