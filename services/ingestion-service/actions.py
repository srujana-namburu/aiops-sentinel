# actions.py

def restart_service(service_name: str):
    print(f"[ACTION] Restarting service: {service_name}")
    # simulate restart
    return f"{service_name} restarted"


def scale_service(service_name: str):
    print(f"[ACTION] Scaling service: {service_name}")
    return f"{service_name} scaled"


def notify_team(service_name: str, severity: str):
    print(f"[ALERT] Notify team: {service_name} | Severity: {severity}")
    return "team notified"


def no_action(service_name: str):
    print(f"[INFO] No action needed for: {service_name}")
    return "no action"