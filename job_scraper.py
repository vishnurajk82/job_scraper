import requests
import csv

def fetch_jobs():
    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": "9fd503c4b7msh99a37b4488d5882p153f8fjsn61d28ab0339c",
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    querystring = {
        "query": "software developer in Chennai",
        "page": "1",
        "num_pages": "1"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    jobs_list = data.get("data", [])

    filtered_jobs = []

    for job in jobs_list:
        title = job.get("job_title", "")
        company = job.get("employer_name", "")
        location = job.get("job_city", "")
        link = job.get("job_apply_link", "")

        if title and ("developer" in title.lower() or "engineer" in title.lower()):
            filtered_jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "link": link
            })

    # Save to CSV
    with open("jobs.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Company", "Location", "Link"])

        for job in filtered_jobs:
            writer.writerow([job["title"], job["company"], job["location"], job["link"]])

    return filtered_jobs