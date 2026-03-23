# decision_engine.py

def decide_action(severity):
    if severity == "CRITICAL":
        return "Restart service immediately"
    elif severity == "HIGH":
        return "Scale service and alert SRE"
    elif severity == "MEDIUM":
        return "Monitor closely and log alert"
    else:
        return "No immediate action required"