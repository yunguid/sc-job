# Job Application Screenshot Processor

## Overview
This project automates the process of extracting job application information from screenshots using OpenAI's Vision API. It monitors a specified folder for new screenshots, processes them to extract key details, and logs the information in a CSV file.

## Features
- Automatic folder monitoring for new screenshots
- Image processing using OpenAI's Vision API
- Extraction of job details: Title, Company, Location, Salary Range
- CSV logging of extracted information
- Error handling and logging

## Prerequisites
- Python 3.7+
- OpenAI API key

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/job-application-processor.git
   cd job-application-processor
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Usage
1. Start the folder monitor:
   ```
   python folder_monitor.py
   ```

2. Place job application screenshots in the monitored folder (default: `/Users/luke/Desktop/job-screenshots`)

3. The script will automatically process new images and update the CSV file (default: `/Users/luke/cursor-projs/screenshot-job/log.csv`)

## Configuration
- Modify `folder_monitor.py` to change the monitored folder or output CSV path
- Adjust logging settings in both `folder_monitor.py` and `job_application_processor.py` as needed

## Files
- `folder_monitor.py`: Watches for new files and triggers processing
- `job_application_processor.py`: Processes images and extracts job information
- `log.csv`: Stores extracted job application data
- `folder_monitor.log`: Logs folder monitoring events
- `job_application_processor.log`: Logs image processing events

## Troubleshooting
- Ensure your OpenAI API key is correctly set and has sufficient quota
- Check the log files for detailed error messages
- Verify that the monitored folder and output CSV paths are correct and accessible

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
[MIT License](LICENSE)
