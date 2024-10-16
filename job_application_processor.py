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
import sys
import json
import base64
import openai
import datetime
from dataclasses import asdict

# Set your OpenAI API key
# Make sure you have set the environment variable OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

def process_screenshot(image_path):
    """
    Processes the screenshot using the OpenAI Vision API.
    Extracts job information such as job title, company name, etc.
    """
    logging.info(f"Processing screenshot: {image_path}")

    # Read and encode the image in base64
    try:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logging.error(f"Error reading image file: {e}")
        raise

    # Craft the prompt
    prompt = "Extract the following information from the job posting image:\n"
    prompt += "- Job Title\n"
    prompt += "- Company Name\n"
    prompt += "- Location\n"
    prompt += "- Salary Range\n"
    prompt += "- Required Skills\n"
    prompt += "Provide the information in JSON format with the above keys. If any information is missing, leave the value empty."

    # Create the message content
    message_content = [
        {"type": "text", "text": prompt},
        {
            "type": "image",
            "image": {
                "data": f"data:image/jpeg;base64,{base64_image}"
            }
        }
    ]

    # Send the request to the OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-vision",
            messages=[
                {
                    "role": "user",
                    "content": message_content
                }
            ],
            max_tokens=500,
            temperature=0.2  # Lower temperature for more focused responses
        )
    except Exception as e:
        logging.error(f"Error calling OpenAI API: {e}")
        raise

    # Parse the response
    try:
        # The assistant's reply is in response.choices[0].message.content
        assistant_reply = response.choices[0].message.content.strip()
        logging.info(f"Assistant reply: {assistant_reply}")

        # Extract JSON from the assistant's reply
        start_index = assistant_reply.find('{')
        end_index = assistant_reply.rfind('}') + 1
        json_str = assistant_reply[start_index:end_index]

        extracted_data = json.loads(json_str)

        # Ensure all required keys are present
        required_keys = ["Job Title", "Company Name", "Location", "Salary Range", "Required Skills"]
        for key in required_keys:
            if key not in extracted_data:
                extracted_data[key] = ""

        # Add date_applied as the current date and time
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
    fieldnames = ["Job Title", "Company Name", "Location", "Salary Range", "Required Skills", "Date Applied"]

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
            logging.FileHandler('/Users/luke/cursor-projs/sc-job/sc-job/job_application_processor.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    main()
