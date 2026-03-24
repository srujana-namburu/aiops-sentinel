# kafka_consumer.py

from kafka import KafkaConsumer
import json
from database import SessionLocal, Incident
from ai_service import analyze_incident
from decision_engine import decide_action
from metrics import severity_counter
from actions import restart_service, scale_service, notify_team, no_action

consumer = KafkaConsumer(
    "incidents",
    bootstrap_servers='127.0.0.1:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id="aiops-group",
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)


def start_consumer():
    print("Consumer is listening...")
   
    db = SessionLocal()

    for message in consumer:
        data = message.value
        print("Received message:", data)

        event = data  # cleaner

        # =========================
        # 🤖 AI ANALYSIS
        # =========================
        analysis = analyze_incident(
            event.get("service_name"),
            event.get("error_message"),
            event.get("error_count")
        )

        # =========================
        # 🔥 OVERRIDE SEVERITY LOGIC
        # =========================
        error_message = event.get("error_message", "").lower()
        error_count = event.get("error_count", 0)

        print("DEBUG:", error_message, error_count)

        if "out of memory" in error_message or error_count >= 25:
            severity = "CRITICAL"
        elif error_count >= 15:
            severity = "HIGH"
        elif error_count >= 5:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        # =========================
        # 📊 METRICS
        # =========================
        severity_counter.labels(severity=severity).inc()

        # =========================
        # 🧠 DECISION ENGINE
        # =========================
        decision = decide_action(severity)

        # =========================
        # 🚀 AUTO-REMEDIATION
        # =========================
        if severity == "CRITICAL":
            action_result = restart_service(event["service_name"])
        elif severity == "HIGH":
            action_result = scale_service(event["service_name"])
        elif severity == "MEDIUM":
            action_result = notify_team(event["service_name"], severity)
        else:
            action_result = no_action(event["service_name"])

        print(f"Action Result: {action_result}")

        # =========================
        # 💾 STORE IN DB
        # =========================
        inc = Incident(
            service_name=event.get("service_name"),
            error_message=event.get("error_message"),
            error_count=event.get("error_count"),
            severity=severity,  # ✅ overridden value
            ai_analysis=str(analysis),
            sre_decision=decision
        )

        db.add(inc)
        db.commit()
        db.refresh(inc)

        print(f"Stored Incident {inc.display_id} | Severity: {severity} | Decision: {decision}")


if __name__ == "__main__":
    print("Starting Kafka consumer...")
    start_consumer()