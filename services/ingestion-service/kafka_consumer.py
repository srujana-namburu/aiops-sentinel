# kafka_consumer.py

from kafka import KafkaConsumer
import json
from database import SessionLocal, Incident
from ai_service import analyze_incident
from decision_engine import decide_action

consumer = KafkaConsumer(
    'incidents-topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='incident-group'
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