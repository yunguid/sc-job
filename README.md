# Job Application Screenshot Processor

## Overview
This project automates the process of extracting job application information from screenshots using OpenAI's Vision API. It monitors a specified folder for new screenshots, processes them to extract key details, and logs the information in a CSV file. It also includes tools for quick statistics and daily reporting.

## Features
- Automatic folder monitoring for new screenshots
- Image processing using OpenAI's Vision API
- Extraction of job details: Title, Company, Location, Salary Range
- CSV logging of extracted information
- Error handling and logging
- Daily email statistics on job applications
- Quick stats command-line tool

## Prerequisites
- Python 3.7+
- OpenAI API key

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/job-application-processor.git
   cd job-application-processor
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python3 -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Usage
1. Start the folder monitor:
   ```
   python folder_monitor.py
   ```

   Alternatively, use the `jobs.sh` script to run the monitor in a virtual environment:
   ```
   ./jobs.sh
   ```

2. Place job application screenshots in the monitored folder (default: `/Users/luke/Desktop/job-screenshots`)

3. The script will automatically process new images and update the CSV file (default: `/Users/luke/cursor-projs/screenshot-job/log.csv`)

## Quick Stats
You can quickly view your job application statistics using the `quick_stats.sh` script:

1. Make the script executable:
   ```
   chmod +x quick_stats.sh
   ```

2. Run the script:
   ```
   ./quick_stats.sh
   ```

This will display:
- Applications submitted today
- Total applications
- Average applications per day
- Days since first application
- Last 5 companies applied to
- Remaining applications for today's goal (30)

### Setting up an alias
To make it easier to run the quick stats, you can set up an alias:

1. Add the following line to your `~/.zshrc` file:
   ```
   alias jobstats='/path/to/your/quick_stats.sh'
   ```

2. Reload your shell configuration:
   ```
   source ~/.zshrc
   ```

Now you can simply type `jobstats` in your terminal to see your application statistics.

## Configuration
- Modify `folder_monitor.py` to change the monitored folder or output CSV path
- Adjust logging settings in both `folder_monitor.py` and `job_application_processor.py` as needed

## Files
- `folder_monitor.py`: Watches for new files and triggers processing
- `job_application_processor.py`: Processes images and extracts job information
- `log.csv`: Stores extracted job application data
- `folder_monitor.log`: Logs folder monitoring events
- `job_application_processor.log`: Logs image processing events
- `jobs.sh`: Bash script to run the folder monitor in a virtual environment
- `quick_stats.sh`: Bash script to display quick job application statistics
- `daily_stats.py`: Python script for sending daily application statistics

## Troubleshooting
- Ensure your OpenAI API key is correctly set and has sufficient quota
- Check the log files for detailed error messages
- Verify that the monitored folder and output CSV paths are correct and accessible

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
[MIT License](LICENSE)
