import json
import requests


with open("src/notetaker/core/publisher/notion_API.json", "r", encoding="utf-8") as file:
    config = json.load(file)

private_key = config["api_key"]
database_id = config["database_id"]

NOTION_TOKEN = private_key
DATABASE_ID = database_id

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


def read_data():
    print("Reading the note...")
    
    with open("src/notetaker/core/data/summary.json", "r") as file:
        summary = json.load(file)

    take_aways = []
    for item in summary["take_aways"]:
        p = (item.get("point") or "").strip()
        e = (item.get("explanation") or "").strip()
        if p and e:
            take_aways.append(f"• {p} — {e}")
        elif p:
            take_aways.append(f"• {p}")
        elif e:
            take_aways.append(f"• {e}")

    
    course = summary["course"]
    title = summary["title"]
    date = summary["date"]
    description = summary["summary"]
    takeaways_text = "\n".join(take_aways)

    return course, title, date, description, takeaways_text

course, title, date, description, takeaways_text = read_data()

def create_template(course, title, date, description, takeaways_text):
    data = {
    "Course": {"title": [{"text": {"content": course}}]},
    "Title": {"rich_text": [{"text": {"content": title}}]},
    "Date": {"rich_text": [{"text": {"content": date}}]},
    "Description": {"rich_text": [{"text": {"content": description}}]},
    "Take-aways": {"rich_text": [{"text": {"content": takeaways_text}}]},
    }

    return data

data = create_template(course, title, date, description, takeaways_text)

def create_page(data: dict) :
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)
    if res.status_code == 200:
        print("The note was successfully transferred to the Notion app.")
    else:
        print(f"Something went wrong: Error {res.status_code}")
              
    return res


create_page(data)