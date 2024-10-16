#!/usr/bin/env python3

"""
Job Application Screenshot Processor Script

This script extracts job application information from a screenshot image
using the OpenAI Vision API and updates a CSV file.

Usage:
    python job_application_processor.py --input /path/to/screenshot.png --output /path/to/data.csv
"""

import argparse
import logging
import os
from openai import OpenAI
import sys
import json
import base64
import datetime

# Set your OpenAI API key
# Make sure you have set the environment variable OPENAI_API_KEY
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def process_screenshot(image_path):
    """
    Processes the screenshot using the OpenAI Vision API.
    Extracts job information such as job title, company name, etc.
    """
    logging.info(f"Processing screenshot: {image_path}")

    try:
        with open(image_path, "rb") as image_file:
            img_b64_str = base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logging.error(f"Error reading image file: {e}")
        raise

    prompt = (
        "Extract the following information from the job posting image provided:\n"
        "- Job Title\n"
        "- Company Name\n"
        "- Location\n"
        "- Salary Range\n"
        "Provide the information in JSON format with the above keys. If any information is missing, leave the value empty."
    )

    img_type = "image/png"  # Adjust if needed for different image types

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{img_type};base64,{img_b64_str}"},
                        },
                    ],
                }
            ],
            max_tokens=500
        )
    except Exception as e:
        logging.error(f"Error calling OpenAI API: {e}")
        raise

    try:
        assistant_reply = response.choices[0].message.content.strip()
        logging.info(f"Assistant reply: {assistant_reply}")

        try:
            extracted_data = json.loads(assistant_reply)
        except json.JSONDecodeError:
            start_index = assistant_reply.find('{')
            end_index = assistant_reply.rfind('}') + 1
            json_str = assistant_reply[start_index:end_index]
            extracted_data = json.loads(json_str)

        required_keys = ["Job Title", "Company Name", "Location", "Salary Range"]
        for key in required_keys:
            if key not in extracted_data:
                extracted_data[key] = ""

        extracted_data["Date Applied"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return extracted_data

    except Exception as e:
        logging.error(f"Error parsing API response: {e}")
        raise

def update_csv(data, csv_path):
    """
    Updates the CSV file with new data.
    """
    import csv

    # Check if CSV file exists
    file_exists = os.path.isfile(csv_path)

    # Define the fieldnames
    fieldnames = ["Job Title", "Company Name", "Location", "Salary Range", "Date Applied"]

    try:
        with open(csv_path, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header if file did not exist
            if not file_exists:
                writer.writeheader()

            # Write the data
            writer.writerow(data)

        logging.info(f"Data appended to CSV file: {csv_path}")
    except Exception as e:
        logging.error(f"Error updating CSV file: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Process a job application screenshot.")
    parser.add_argument('--input', '-i', required=True, help='Path to the input image file.')
    parser.add_argument('--output', '-o', required=True, help='Path to the output CSV file.')
    args = parser.parse_args()

    image_path = args.input
    csv_path = args.output

    # Process the screenshot
    try:
        data = process_screenshot(image_path)
    except Exception as e:
        logging.error(f"Error processing screenshot: {e}")
        sys.exit(1)

    # Update CSV file
    try:
        update_csv(data, csv_path)
    except Exception as e:
        logging.error(f"Error updating CSV file: {e}")
        sys.exit(1)

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('/Users/luke/cursor-projs/screenshot-job/job_application_processor.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    main()
