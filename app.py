from flask import Flask,render_template,request
import requests

app = Flask(__name__)

API_KEY = "9fd503c4b7msh99a37b4488d5882p153f8fjsn61d28ab0339c"

url = "https://jsearch.p.rapidapi.com/search"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

# 🔥 SKILL DATABASE (IMPORTANT)
SKILLS_DB = [
    "python", "java", "sql", "react", "node", "aws",
    "docker", "kubernetes", "javascript", "html", "css",
    "c++", "c#", ".net", "mongodb", "django", "flask"
]


@app.route("/", methods=["GET", "POST"])
def home():
    jobs = []

    if request.method == "POST":
        user_input = request.form.get("skills", "")
        user_skills = [s.strip().lower() for s in user_input.split(",") if s.strip()]

        querystring = {
            "query": "software developer in Chennai",
            "page": "1",
            "num_pages": "1"
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        if "data" not in data:
            return "API Error"

        for job in data["data"]:
            title = job.get("job_title", "")
            company = job.get("employer_name", "")
            location = job.get("job_city", "")
            link = job.get("job_apply_link", "")
            description = job.get("job_description", "")

            # 🧠 Combine text
            job_text = (title + " " + description).lower()

            # 🔥 STEP 1: Extract job skills
            job_skills = []
            for skill in SKILLS_DB:
                if skill in job_text:
                    job_skills.append(skill)

            # 🔥 STEP 2: Find matched skills
            matched = []
            for skill in user_skills:
                if skill in job_skills:
                    matched.append(skill)

            # 🔥 STEP 3: Find missing skills (IMPORTANT FIX)
            missing = []
            for skill in job_skills:
                if skill not in user_skills:
                    missing.append(skill)

            # 🔥 STEP 4: Score (based on job requirement)
            if job_skills:
                score = int((len(matched) / len(job_skills)) * 100)
            else:
                score = 0

            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "link": link,
                "score": score,
                "missing": missing
            })

        jobs = sorted(jobs, key=lambda x: x["score"], reverse=True)

    return render_template("index.html", jobs=jobs)


if __name__ == "__main__":
    app.run(debug=True)