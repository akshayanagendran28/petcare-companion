import os

# Automatically bind to 0.0.0.0:$PORT for Render and Cloud Platforms
port = os.getenv("PORT", "10000")
bind = f"0.0.0.0:{port}"

workers = int(os.getenv("WEB_CONCURRENCY", "2"))
threads = 4
worker_class = "gthread"
timeout = 120
keepalive = 5

accesslog = "-"
errorlog = "-"
loglevel = "info"
