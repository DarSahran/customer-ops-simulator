import uuid
from faker import Faker
import random
import mysql.connector
from datetime import datetime, timedelta

fake = Faker()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="customer_ops_simulator"
)
cursor = conn.cursor()

# ---------- Helper ----------
def insert_customer():
    customer_id = str(uuid.uuid4())
    query = """
        INSERT INTO customers (id, name, industry, priority_level, active, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        customer_id,
        fake.company(),
        fake.job(),
        random.choice(['High', 'Medium', 'Low']),
        True,
        fake.date_time_this_year()
    ))
    return customer_id

def insert_rule(customer_id):
    rule_id = str(uuid.uuid4())
    query = """
        INSERT INTO rules (id, customer_id, rule_name, rule_type, frequency, status, last_run)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        rule_id,
        customer_id,
        fake.bs().capitalize(),
        random.choice(['Commission', 'Compliance', 'Threshold']),
        random.choice(['hourly', 'daily']),
        'active',
        fake.date_time_this_month()
    ))
    return rule_id

def insert_log(customer_id, rule_id):
    query = """
        INSERT INTO execution_logs (id, rule_id, customer_id, status, output_summary, executed_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        str(uuid.uuid4()),
        rule_id,
        customer_id,
        random.choice(['success', 'failure']),
        fake.sentence(),
        fake.date_time_this_month()
    ))

def insert_ticket(customer_id, rule_id):
    query = """
        INSERT INTO tickets (id, customer_id, related_rule_id, issue_summary, status, created_at, resolved_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    created = fake.date_time_this_month()
    resolved = created + timedelta(days=random.randint(1, 5)) if random.random() > 0.4 else None
    cursor.execute(query, (
        str(uuid.uuid4()),
        customer_id,
        rule_id,
        fake.catch_phrase(),
        random.choice(['open', 'in_progress', 'resolved']),
        created,
        resolved
    ))

# ---------- Generate Data ----------
for _ in range(50):  # 50 customers
    cust_id = insert_customer()
    for _ in range(random.randint(1, 4)):  # 1–4 rules each
        rule_id = insert_rule(cust_id)
        for _ in range(random.randint(3, 8)):  # Execution logs
            insert_log(cust_id, rule_id)
        if random.random() > 0.7:
            insert_ticket(cust_id, rule_id)

conn.commit()
print("Mock data inserted successfully.")
conn.close()
