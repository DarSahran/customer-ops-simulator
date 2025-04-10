from fastapi import APIRouter
from db import get_db_connection

router = APIRouter(prefix="/rules", tags=["Rules"])

@router.get("/")
def get_all_rules():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM rules")
    result = cursor.fetchall()
    conn.close()
    return result

@router.get("/{customer_id}")
def get_rules_for_customer(customer_id: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM rules WHERE customer_id = %s", (customer_id,))
    result = cursor.fetchall()
    conn.close()
    return result
