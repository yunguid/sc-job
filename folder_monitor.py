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
        logging.FileHandler('/Users/luke/cursor-projs/screenshot-job/folder_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Add this set to keep track of processed files
processed_files = set()

class NewFileHandler(FileSystemEventHandler):
    def __init__(self, processing_script, output_csv):
        self.processing_script = processing_script
        self.output_csv = output_csv

    def on_created(self, event):
        # Check if the new file is a file (not a directory)
        if not event.is_directory:
            file_path = event.src_path
            file_name = os.path.basename(file_path)
            
            # Check if the file has already been processed
            if file_name not in processed_files:
                logging.info(f"New file detected: {file_name}")
                logging.info(f"Processing file: {file_name}")
                
                try:
                    subprocess.run([
                        '/usr/bin/env', 'python3',
                        self.processing_script,
                        '--input', file_path,
                        '--output', self.output_csv
                    ], check=True)
                    logging.info(f"File processed successfully: {file_name}")
                    
                    # Add the file to the set of processed files
                    processed_files.add(file_name)
                except subprocess.CalledProcessError as e:
                    logging.error(f"Error processing file {file_name}: {e}")
            else:
                logging.info(f"File already processed, skipping: {file_name}")

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
    processing_script = '/Users/luke/cursor-projs/screenshot-job/job_application_processor.py'
    output_csv = '/Users/luke/cursor-projs/screenshot-job/log.csv'

    # Ensure the folder exists
    if not os.path.isdir(folder_to_watch):
        print(f"Folder does not exist: {folder_to_watch}")
        sys.exit(1)

    monitor_folder(folder_to_watch, processing_script, output_csv)
