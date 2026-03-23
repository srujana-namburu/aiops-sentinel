# kafka_consumer.py

from kafka import KafkaConsumer
import json
from database import SessionLocal, Incident
from ai_service import analyze_incident
from decision_engine import decide_action
from metrics import severity_counter

consumer = KafkaConsumer(
    "incidents",
    bootstrap_servers='127.0.0.1:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id="aiops-group",   # 🔥 ADD THIS
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)


def start_consumer():
    print("Consumer is listening...")
   
    db = SessionLocal()

    for message in consumer:
        print("Received message:", message.value)

        event = message.value

        analysis = analyze_incident(
        event.get("service_name"),
        event.get("error_message"),
        event.get("error_count")
    )

        severity = analysis.get("severity", "LOW")
        severity_counter.labels(severity=severity).inc()
        decision = decide_action(severity)

        inc = Incident(
            service_name=event.get("service_name"),
            error_message=event.get("error_message"),
            error_count=event.get("error_count"),
            severity=severity,
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