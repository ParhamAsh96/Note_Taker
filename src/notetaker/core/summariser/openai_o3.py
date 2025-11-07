import json
from pathlib import Path
from openai import OpenAI

with open("src/notetaker/core/summariser/OpenAI_API.json", "r", encoding="utf-8") as file:
    config = json.load(file)

private_key = config["api_key"]

client = OpenAI(
  api_key=private_key
)


def summarize_transcript(path="src/notetaker/core/data/transcript.json"):
    data = json.loads(Path(path).read_text(encoding="utf-8"))

    course = data.get("Course", "Unknown course")
    title = data.get("Title", "Untitled")
    date  = data.get("Date", "Unknown date")
    text  = data.get("Description", "")

    system = (
        "You are a careful note-taker. Write in clear B2 English. "
        "Do not invent facts. If something is unclear, write 'Unknown'. "
        "Return valid JSON only."
    )

    user_instructions = (
        f"Course: {course}\n"
        f"Title: {title}\n"
        f"Date: {date}\n\n"
        "Task: Summarize the transcript, then list the most important take-aways "
        "with short explanations. Max 7 take-aways.\n\n"
        "Transcript:\n" + text
    )

    resp = client.responses.create(
        model="o3-mini",
        input=[{"role": "system", "content": [{"type": "input_text", "text": system}]},
               {"role": "user",   "content": [{"type": "input_text", "text": user_instructions}]}],
    )

    return resp.output_text


def save_summary():
    raw = summarize_transcript()
    try:
        data = json.loads(raw)

    except json.JSONDecodeError:
        data = {"summary": raw, "takeaways": []}


    with open("src/notetaker/core/data/summary.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


save_summary()