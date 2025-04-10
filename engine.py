# engine.py
import uuid
import random
from datetime import datetime
from db import get_db_connection

def execute_all_rules():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get active rules
    cursor.execute("SELECT * FROM rules WHERE status = 'active'")
    rules = cursor.fetchall()

    for rule in rules:
        rule_id = rule['id']
        customer_id = rule['customer_id']

        status = random.choice(['success'] * 4 + ['failure'])  # 80% success rate
        summary = f"Executed rule '{rule['rule_name']}' with status: {status}"

        # Insert execution log
        cursor.execute("""
            INSERT INTO execution_logs (id, rule_id, customer_id, status, output_summary, executed_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            str(uuid.uuid4()),
            rule_id,
            customer_id,
            status,
            summary,
            datetime.now()
        ))

        # Auto-create ticket if failure
        if status == "failure":
            cursor.execute("""
                INSERT INTO tickets (id, customer_id, related_rule_id, issue_summary, status, created_at, resolved_at)
                VALUES (%s, %s, %s, %s, %s, %s, NULL)
            """, (
                str(uuid.uuid4()),
                customer_id,
                rule_id,
                f"Issue during execution of rule '{rule['rule_name']}'",
                'open',
                datetime.now()
            ))

    conn.commit()
    conn.close()
    print("Rules executed & logs updated.")
