import os
import time
import json
import threading
from datetime import datetime, timezone
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from concurrent.futures import ThreadPoolExecutor

# ===============================
# IMPORT FROZEN CRYPTO MODULE
# ===============================
from crypto_engine.crypto_engine import crypto_check

# ===============================
# CONFIGURATION
# ===============================
WATCH_DIR = os.path.expanduser("~/Desktop")
LOG_DIR = os.path.expanduser("~/Desktop_monitor_logs")
LOG_FILE = os.path.join(LOG_DIR, "file_events.log")

STABILITY_INTERVAL = 0.2
STABILITY_WINDOW = 1.0
MAX_WORKERS = 4

IGNORED_EXTENSIONS = {".tmp", ".swp", ".log", ".DS_Store"}

os.makedirs(LOG_DIR, exist_ok=True)

# ===============================
# THREADING / STATE
# ===============================
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
registry_lock = threading.Lock()
log_lock = threading.Lock()
crypto_lock = threading.Lock()

stability_in_flight = set()
last_processed = {}

# ===============================
# UTILITIES
# ===============================
def utc_now():
    return datetime.now(timezone.utc).isoformat()

def should_ignore(path):
     # Ignore internal crypto baseline file
    if "crypto_engine" in path and "baselines.json" in path:
        return True
    _, ext = os.path.splitext(path)
    return ext in IGNORED_EXTENSIONS

def log_event(event):
    with log_lock:
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(event) + "\n")
    print(event)

def forward_to_ml(payload):
    """
    Forward only meaningful crypto results to ML.
    DELETE events are audit-only.
    """
    crypto = payload.get("crypto_result")

    if crypto is None:
        print("➡ Forwarded to ML: NO_CRYPTO_EVENT")
        return

    status = crypto.get("integrity_status", "UNKNOWN")
    print("➡ Forwarded to ML:", status)

def should_reprocess(path):
    try:
        mtime = os.path.getmtime(path)
    except FileNotFoundError:
        return False

    if last_processed.get(path) == mtime:
        return False

    last_processed[path] = mtime
    return True

# ===============================
# STABILITY CHECK + CRYPTO
# ===============================
def stability_check(path, event_type):
    if should_ignore(path):
        return

    with registry_lock:
        if path in stability_in_flight:
            return
        stability_in_flight.add(path)

    try:
        last_size = None
        last_change = time.time()

        while True:
            if not os.path.exists(path):
                return

            try:
                size = os.path.getsize(path)
            except (FileNotFoundError, PermissionError):
                time.sleep(STABILITY_INTERVAL)
                continue

            if size != last_size:
                last_size = size
                last_change = time.time()
            elif time.time() - last_change >= STABILITY_WINDOW:
                break

            time.sleep(STABILITY_INTERVAL)

        if not os.path.exists(path):
            return

        if not should_reprocess(path):
            return

        try:
            with crypto_lock:
                crypto_result = crypto_check(path)
        except Exception as e:
            crypto_result = {
                "integrity_status": "CRYPTO_ERROR",
                "error": str(e)
            }

        payload = {
            "file_event": {
                "file_path": path,
                "event_type": event_type,
                "timestamp": utc_now(),
                "file_size": last_size
            },
            "crypto_result": crypto_result
        }

        log_event(payload)
        forward_to_ml(payload)

    finally:
        with registry_lock:
            stability_in_flight.discard(path)

# ===============================
# EVENT HANDLER
# ===============================
class FileMonitorHandler(FileSystemEventHandler):

    def on_created(self, event):
        if not event.is_directory:
            executor.submit(stability_check, event.src_path, "CREATED")

    def on_modified(self, event):
        if not event.is_directory:
            executor.submit(stability_check, event.src_path, "MODIFIED")

    def on_deleted(self, event):
        if event.is_directory:
            return

        payload = {
            "file_event": {
                "file_path": event.src_path,
                "event_type": "DELETED",
                "timestamp": utc_now()
            },
            "crypto_result": None   # IMPORTANT: delete is NOT a crypto event
        }

        log_event(payload)
        forward_to_ml(payload)

# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    print(f"📂 Monitoring: {WATCH_DIR}")
    print(f"📝 Logs: {LOG_FILE}")

    observer = Observer()
    observer.schedule(FileMonitorHandler(), WATCH_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Stopping file monitor...")
        observer.stop()

    observer.join()
    executor.shutdown(wait=True)

