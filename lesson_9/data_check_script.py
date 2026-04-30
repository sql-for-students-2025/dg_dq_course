import psycopg2
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


# Конфигурация подключения к БД
DB_CONFIG = {
    "dbname": os.getenv('DB_NAME'),
    "user":os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD'),
    "host": os.getenv('DB_HOST'),
    "port": 6432
}

# Вебхук URL (например, Slack, Discord, Teams, или кастомный)
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

def fetch_issues_to_alert():
    """Забирает из таблицы проверки с проблемами, по которым ещё не отправлен алерт"""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    query = """
        SELECT id, check_time, entity_name, issue_description
        FROM dq_dg.data_quality_checks_log
        WHERE issue_found = TRUE AND alert_sent = FALSE
        ORDER BY check_time;
    """
    cursor.execute(query)
    issues = cursor.fetchall()
    cursor.close()
    conn.close()
    return issues

def mark_alert_sent(issue_ids):
    """Обновляет флаг alert_sent для отправленных записей"""
    if not issue_ids:
        return
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE dq_dg.data_quality_checks_log
        SET alert_sent = TRUE
        WHERE id = ANY(%s)
    """, (issue_ids,))
    conn.commit()
    cursor.close()
    conn.close()

def send_alert(issue):
    issue_id, check_time, entity_name, issue_description = issue
    message = {
        "text": f"🚨 **Data Quality Alert** 🚨\n"
                f"*Time:* {check_time}\n"
                f"*Entity:* {entity_name}\n"
                f"*Issue:* {issue_description}\n"
                f"*ID:* {issue_id}"
    }
    
    response = requests.post(WEBHOOK_URL, json=message)
    if response.status_code not in (200, 201, 202, 204):
        print(f"Failed to send alert for issue {issue_id}: {response.status_code} {response.text}")
        return False
    return True

def main():
    issues = fetch_issues_to_alert()
    if not issues:
        print("No new issues to alert.")
        return
    
    sent_ids = []
    for issue in issues:
        print(f"Sending alert for issue {issue[0]}...")
        if send_alert(issue):
            sent_ids.append(issue[0])
    
    mark_alert_sent(sent_ids)
    print(f"Alerts sent for {len(sent_ids)} issues.")

if __name__ == "__main__":
    main()