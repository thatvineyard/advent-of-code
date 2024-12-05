import multiprocessing
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, EVENT_TYPE_MODIFIED, FileModifiedEvent


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, callback, cooldown_seconds=1):
        super().__init__()
        self._callback = callback
        self._cooldown_seconds = cooldown_seconds
        self.previous_trigger = sys.float_info.min
        self.current_process: multiprocessing.Process | None = None

    def trigger(self):
        if self.is_running():
            self.current_process.terminate()
            self.current_process.join()
        
        self.current_process = multiprocessing.Process(target=self.run_callback)
        self.current_process.start()

    def run_callback(self):
        try:
            self._callback()
        except KeyboardInterrupt:
            print("❗ Run interrupted (press ctrl+c again to quit)")

    def is_running(self):
        return self.current_process and self.current_process.is_alive()

    def on_modified(self, event):
        if not event.is_directory and event.event_type == EVENT_TYPE_MODIFIED:
            if self.cooldown_expired():
                self.previous_trigger = time.time()
                print(f"File {event.src_path} has been modified!")
                self.trigger()

    def cooldown_expired(self):
        return time.time() > self.previous_trigger + self._cooldown_seconds


class Watcher:
    def __init__(self, watch_dir: str, on_change):
        self._watch_dir = watch_dir
        self._event_handler = FileChangeHandler(on_change)

    def start(self):
        print(f"👀 Starting to monitor files in {self._watch_dir}")
        self.monitor_file_changes(self._watch_dir, self._event_handler)

    @staticmethod
    def monitor_file_changes(directory, event_handler: FileChangeHandler):
        observer = Observer()
        observer.schedule(
            event_handler,
            path=directory,
            recursive=True,
        )
        observer.start()

        # Manually trigger the first run
        event_handler.on_modified(FileModifiedEvent(src_path=directory))

        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                if not event_handler.is_running():
                    observer.stop()
                    break

        observer.join()
