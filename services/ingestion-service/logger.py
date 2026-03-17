# import json
# import logging
# from datetime import datetime, timezone
# from typing import Any, Dict, Optional


# class JSONFormatter(logging.Formatter):
#     """Log formatter that outputs JSON with a fixed schema."""

#     def format(self, record: logging.LogRecord) -> str:
#         # Base payload
#         payload: Dict[str, Any] = {
#             "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
#             "level": record.levelname,
#             "service": getattr(record, "service", record.name),
#             "message": record.getMessage(),
#             "incident_id": getattr(record, "incident_id", None),
#             "correlation_id": getattr(record, "correlation_id", None),
#             "agent": getattr(record, "agent", None),
#             "duration_ms": getattr(record, "duration_ms", None),
#         }

#         # Include any other extras under "extra" for debugging / flexibility
#         extras = {
#             k: v
#             for k, v in record.__dict__.items()
#             if k
#             not in {
#                 "name",
#                 "msg",
#                 "args",
#                 "levelname",
#                 "levelno",
#                 "pathname",
#                 "filename",
#                 "module",
#                 "exc_info",
#                 "exc_text",
#                 "stack_info",
#                 "lineno",
#                 "funcName",
#                 "created",
#                 "msecs",
#                 "relativeCreated",
#                 "thread",
#                 "threadName",
#                 "processName",
#                 "process",
#                 "service",
#                 "incident_id",
#                 "correlation_id",
#                 "agent",
#                 "duration_ms",
#             }
#         }

#         if extras:
#             payload["extra"] = extras

#         return json.dumps(payload, ensure_ascii=False)


# class ContextLoggerAdapter(logging.LoggerAdapter):
#     """LoggerAdapter that merges provided `extra` with its own context."""

#     def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
#         extra = dict(self.extra or {})
#         extra.update(kwargs.get("extra", {}))
#         kwargs["extra"] = extra
#         return msg, kwargs


# def get_logger(
#     name: Optional[str] = None,
#     service: Optional[str] = None,
#     level: int = logging.INFO,
# ) -> logging.Logger:
#     """Return a JSON logger configured for this service.

#     Args:
#         name: Logger name to use. Defaults to the service name.
#         service: Service name to include in output. If not provided, falls back to `name`.
#         level: Log level.

#     Returns:
#         A configured `logging.Logger` instance.
#     """

#     logger_name = name or service or "root"
#     logger = logging.getLogger(logger_name)
#     logger.setLevel(level)

#     # Avoid adding multiple handlers when calling get_logger repeatedly
#     if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
#         handler = logging.StreamHandler()
#         handler.setFormatter(JSONFormatter())
#         handler.setLevel(level)
#         logger.addHandler(handler)

#     # Ensure required fields are always available as part of the record
#     logger = ContextLoggerAdapter(logger, {"service": service or logger_name})

#     return logger

# logger.py
import logging, json, sys, os
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "service": os.getenv("SERVICE_NAME", "unknown"),
            "message": record.getMessage(),
        }

        # Optional fields
        if hasattr(record, "incident_id"):
            log["incident_id"] = record.incident_id

        if hasattr(record, "correlation_id"):
            log["correlation_id"] = record.correlation_id

        if hasattr(record, "agent"):
            log["agent"] = record.agent

        if hasattr(record, "duration_ms"):
            log["duration_ms"] = record.duration_ms

        if record.exc_info:
            log["exception"] = self.formatException(record.exc_info)

        return json.dumps(log)


def get_logger(name: str) -> logging.Logger:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False

    return logger