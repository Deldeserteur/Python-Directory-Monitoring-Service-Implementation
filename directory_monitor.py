import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, log_file):
        self.log_file = log_file

    def on_any_event(self, event):
        event_data = {
            "event_type": event.event_type,
            "src_path": event.src_path,
            "is_directory": event.is_directory,
        }
        with open(self.log_file, "a") as log:
            log.write(json.dumps(event_data) + "\n")

def main():
    monitored_dir = "/home/damrosdeldesertos/ubuntu/bsm/test"
    log_file = "/home/damrosdeldesertos/ubuntu/bsm/logs/changes.json"
    
    if not os.path.exists(monitored_dir):
        os.makedirs(monitored_dir)
    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))

    event_handler = ChangeHandler(log_file)
    observer = Observer()
    observer.schedule(event_handler, monitored_dir, recursive=True)

    print(f"Monitoring changes in {monitored_dir}...")
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
