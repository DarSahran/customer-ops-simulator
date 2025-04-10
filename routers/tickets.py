from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from enum import Enum
from db import get_db_connection
from datetime import datetime

router = APIRouter(prefix="/tickets", tags=["Support Tickets"])

# 🔒 Use Enum for strong validation
class TicketStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"

class TicketUpdateRequest(BaseModel):
    status: TicketStatus

@router.get("/")
def get_all_tickets():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tickets")
    result = cursor.fetchall()
    conn.close()
    return result

@router.get("/{ticket_id}")
def get_ticket_by_id(ticket_id: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tickets WHERE id = %s", (ticket_id,))
    result = cursor.fetchone()
    conn.close()
    if not result:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return result

@router.patch("/{ticket_id}")
def update_ticket_status(ticket_id: str, update: TicketUpdateRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if ticket exists
    cursor.execute("SELECT id FROM tickets WHERE id = %s", (ticket_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Update logic
    if update.status == TicketStatus.resolved:
        cursor.execute(
            "UPDATE tickets SET status = %s, resolved_at = %s WHERE id = %s",
            (update.status.value, datetime.now(), ticket_id)
        )
    else:
        cursor.execute(
            "UPDATE tickets SET status = %s, resolved_at = NULL WHERE id = %s",
            (update.status.value, ticket_id)
        )

    conn.commit()
    conn.close()
    return {
        "message": "Ticket status updated",
        "ticket_id": ticket_id,
        "new_status": update.status
    }
