#!/usr/bin/env python3

import sys
import time
import logging
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/luke/cursor-projs/sc-job/sc-job/folder_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class NewFileHandler(FileSystemEventHandler):
    def __init__(self, processing_script, output_csv):
        self.processing_script = processing_script
        self.output_csv = output_csv

    def on_created(self, event):
        # Check if the new file is a file (not a directory)
        if not event.is_directory:
            filepath = event.src_path
            filename = os.path.basename(filepath)

            # Ignore temporary or hidden files
            if filename.startswith('.'):
                return

            logging.info(f"New file detected: {filename}")

            # Wait until the file is fully copied
            while not self.is_file_ready(filepath):
                time.sleep(0.1)

            # Check if the file is a PNG or JPEG image
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Call the processing script
                try:
                    logging.info(f"Processing file: {filename}")
                    subprocess.run([
                        '/usr/bin/env', 'python3',
                        self.processing_script,
                        '--input', filepath,
                        '--output', self.output_csv
                    ], check=True)
                    logging.info(f"File processed successfully: {filename}")
                except subprocess.CalledProcessError as e:
                    logging.error(f"Error processing file {filename}: {e}")
            else:
                logging.info(f"Ignoring non-image file: {filename}")

    def is_file_ready(self, filepath):
        # Check if a file is ready to be processed (finished copying)
        try:
            with open(filepath, 'rb'):
                return True
        except IOError:
            return False

def monitor_folder(folder_to_watch, processing_script, output_csv):
    event_handler = NewFileHandler(processing_script, output_csv)
    observer = Observer()
    observer.schedule(event_handler, path=folder_to_watch, recursive=False)
    observer.start()
    logging.info(f"Started monitoring folder: {folder_to_watch}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Stopped monitoring.")

    observer.join()

if __name__ == "__main__":
    # Set the folder you want to monitor
    folder_to_watch = '/Users/luke/Desktop/job-screenshots'

    # Set the path to your processing script and output CSV
    processing_script = '/Users/luke/cursor-projs/sc-job/sc-job/job_application_processor.py'
    output_csv = '/Users/luke/cursor-projs/sc-job/sc-job/log.csv'

    # Ensure the folder exists
    if not os.path.isdir(folder_to_watch):
        print(f"Folder does not exist: {folder_to_watch}")
        sys.exit(1)

    monitor_folder(folder_to_watch, processing_script, output_csv)
