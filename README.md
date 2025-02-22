# job-scraper
Web-Scraping list of Jobs (limited)

# Job Scraping Script
This Python script scrapes job listings from a given base URL, extracts the relevant job details, and fetches detailed information from individual job pages. It then combines the basic job information with detailed data such as job description, responsibilities, education, experience, and other job attributes. The script stores the final data in a JSON file.

## Features
- Fetches job listings from a base URL.
- Extracts essential details like job title, categories, location, and job link.
- Visits each job link to extract additional details like:
  - Job Description
  - Primary Duties and Responsibilities
  - Education and Experience
  - Req ID, Working Title, Department, Business Entity, etc.
- Saves the data in a structured JSON format.

## Requirements

- Python 3.x
- `requests` for sending HTTP requests to fetch data from the web.
- `beautifulsoup4` for parsing HTML and extracting the relevant job data.
- `urllib.parse` for properly joining URLs to ensure valid job links.
- `json` for storing the extracted data in a structured JSON format.

## Installation

### Step 1: Download GitHub Desktop and Clone the repository
### Step 2: Install Dependancies
Run below command
```bash
pip install requests beautifulsoup4
```

## Usage

### Step 1: Run the Script
Navigate to the folder containing the script in your terminal and run:

```bash
python python_jobscraper_project.py
```
### Step 2: Output
The script will:
- Fetch job listings from the BASE_URL.
- Visit each job-specific URL and scrape detailed job data.
- Save the data into a JSON file called hospital_jobs_detailed.json.
- This is available in the repository and saved as `jobs_output.json`.

## Troubleshooting
- Missing Fields or Incorrect Data 
  -Verify that the structure of the HTML from the job page matches the classes and tags the script expects. If there are changes to the website, you may need to       update the class names or tags in the script.
-Empty or Missing JSON File
  -If no jobs are saved in the output JSON file, check that the BASE_URL and job links are correct and lead to valid job pages.

## Acknowledgement
The project uses BeautifulSoup for HTML parsing, Requests for HTTP requests, and JSON for saving the extracted data.
