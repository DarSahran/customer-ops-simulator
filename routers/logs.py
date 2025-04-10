from fastapi import APIRouter
from db import get_db_connection

router = APIRouter(prefix="/logs", tags=["Execution Logs"])

@router.get("/")
def get_all_logs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM execution_logs ORDER BY executed_at DESC")
    result = cursor.fetchall()
    conn.close()
    return result

@router.get("/{rule_id}")
def get_logs_for_rule(rule_id: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM execution_logs WHERE rule_id = %s ORDER BY executed_at DESC", (rule_id,))
    result = cursor.fetchall()
    conn.close()
    return result
