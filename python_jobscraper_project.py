import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

BASE_URL = "https://careers.cshs.org/search-jobs?utm_source=google.com&utm_medium=paid_search&utm_campaign=Healthcare_Jobs&utm_content=search_engine&utm_term=343201292&ss=paid&gad_source=1&gclid=CjwKCAiAk8G9BhA0EiwAOQxmfr-pO26RLmIiTENJCSCal6S-R11SBlss1_ZwbWcX1ks8FQlj-dX9jBoCSAwQAvD_BwE"

def get_job_listings():
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        print("Failed to fetch job listings.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    
    job_section = soup.find("section", id ="search-results-list")  
    if not job_section:
        print("No job listings found.")
        return []

    job_listings = job_section.find_all("li")[:10]  

    jobs = []
    for job in job_listings:
        job_link = job.find("a")["href"]
        title = job.find("h2").text.strip()
        categories = [cat.text.strip() for cat in job.find_all("i")]
        location = job.find("span", class_="job-location").text.strip()

        full_job_link = urljoin(BASE_URL, job_link)  

        jobs.append({
            "Title": title,
            "Categories": ", ".join(categories),
            "Location": location,
            "Job Link": full_job_link
        })
    
    return jobs

def get_job_details(job_url):
    response = requests.get(job_url)
    if response.status_code != 200:
        print(f"Failed to fetch job details for {job_url}")
        return {
            "Job Description": "N/A",
            "Primary Duties and Responsibilities": [],
            "Education": "N/A",
            "Experience": "N/A",
            "Req ID": "N/A",
            "Working Title": "N/A",
            "Department": "N/A",
            "Business Entity": "N/A",
            "Job Category": "N/A",
            "Job Specialty": "N/A",
            "Overtime Status": "N/A",
            "Primary Shift": "N/A",
            "Shift Duration": "N/A",
            "Base Pay": "N/A"
        }

    soup = BeautifulSoup(response.text, "html.parser")

    job_description = "N/A"
    primary_duties = []

    education = "N/A"
    experience = "N/A"

    details_sections = soup.find_all("div", class_="job-details__description-content basic-formatter")

    for section in details_sections:
        data_bind = section.get("data-bind", "")

        if "pageData().job.description" in data_bind:
            paragraphs = section.find_all("p")
            job_description = paragraphs[0].text.strip() if paragraphs else "N/A"
            primary_duties = [li.text.strip() for li in section.find_all("li")]

        elif "pageData().job.qualifications" in data_bind:
            paragraphs = section.find_all("p")
            
            edu_list = []
            exp_list = []
            is_experience = False  

            for p in paragraphs:
                text = p.get_text(strip=True)

                if "Experience:" in text:
                    is_experience = True  

                elif is_experience:
                    exp_list.append(text)  

                else:
                    edu_list.append(text)  

            education = " ".join(edu_list) if edu_list else "N/A"
            experience = " ".join(exp_list) if exp_list else "N/A"

    job_meta = {}
    bold_tags = soup.find_all("b")
    for b in bold_tags:
        key = b.text.strip().replace(":", "")
        value = b.next_sibling.strip() if b.next_sibling else "N/A"
        job_meta[key] = value

    return {
        "Job Description": job_description,
        "Primary Duties and Responsibilities": primary_duties,
        "Education": education,
        "Experience": experience,
        "Req ID": job_meta.get("Req ID", "N/A"),
        "Working Title": job_meta.get("Working Title", "N/A"),
        "Department": job_meta.get("Department", "N/A"),
        "Business Entity": job_meta.get("Business Entity", "N/A"),
        "Job Category": job_meta.get("Job Category", "N/A"),
        "Job Specialty": job_meta.get("Job Specialty", "N/A"),
        "Overtime Status": job_meta.get("Overtime Status", "N/A"),
        "Primary Shift": job_meta.get("Primary Shift", "N/A"),
        "Shift Duration": job_meta.get("Shift Duration", "N/A"),
        "Base Pay": job_meta.get("Base Pay", "N/A")
    }

if __name__ == "__main__":
    jobs = get_job_listings()
    
    all_jobs_data = []
    for job in jobs:
        job_details = get_job_details(job["Job Link"])
        job.update(job_details)  
        all_jobs_data.append(job)

    with open("jobs_output.json", "w", encoding="utf-8") as json_file:
        json.dump(all_jobs_data, json_file, indent=4, ensure_ascii=False)

    print("Job details saved to jobs_output.json")