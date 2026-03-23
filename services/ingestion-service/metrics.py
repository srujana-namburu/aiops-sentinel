# metrics.py

from prometheus_client import Counter, Histogram

# Total incidents received
incident_counter = Counter(
    "incidents_total",
    "Total number of incidents received"
)

# Incident severity count
severity_counter = Counter(
    "incident_severity_total",
    "Number of incidents by severity",
    ["severity"]
)

# Request latency
request_latency = Histogram(
    "request_latency_seconds",
    "Time spent processing request"
)