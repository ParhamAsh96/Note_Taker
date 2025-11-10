import json
import time
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
    summary  = data.get("Description", "")

    system = (
        "You are a careful note-taker. Write in clear B2 English. "
        "Do not invent facts. If something is unclear, write 'Unknown'. "
        "Return ONLY one valid JSON object (no prose, no markdown). "
        "Use exactly these keys: 'course', 'title', 'date', 'summary', 'take-aways'. "
        "For 'take-aways', write 6–8 short points"
        "Use standard JSON (double quotes, no trailing commas)."
    )

    user_instructions = (
        "Task: Read the transcript and produce the JSON object in the schema below.\n\n"
        f"Course: {course}\n"
        f"Title: {title}\n"
        f"Date: {date}\n\n"
        "Task: Summarize the transcript, then list the most important take-aways "
        "with short explanations. Max 8 take-aways.\n\n"
        "Rules:\n"
        "- Keep/confirm the course name.\n"
        "- Keep the given title (if any).\n"
        "- Description: one SINGLE continuous string of about 1950 characters total.\n"
        "- Inside that one string, include BOTH:\n"
        "    • At least 1000 characters that summarize the lecture.\n"
        "    • At least 550 characters that give a detailed explanation of the key ideas.\n"
        "- Blend summary and detailed explanation naturally (no headings, no labels, no section breaks, no bullet points).\n"
        "- Use simple B2-level language, coherent flow, and avoid repetition and filler.\n"
        "- take-aways: 6–8 key points joined into one string using '; '. (limit 400 characters).\n\n"
        "Output schema (example values only):\n"
        "{\n"
        "  'course': 'course name from the transcript',\n"
        "  'title': 'Lecture title from the input',\n"
        "  'date': 'Lecture title from the input',\n"
        "  'summary': '<one continuous ~800–900 word string combining summary (≥500 words) and detailed explanation (≥300 words)>',\n"
        "  'take-aways': 'point 1; point 2; point 3'\n"
        "}\n"
        "Return only the JSON object."
        "Transcript:\n" + summary
    )

    resp = client.responses.create(
        model="o3-mini",
        input=[{"role": "system", "content": [{"type": "input_text", "text": system}]},
               {"role": "user",   "content": [{"type": "input_text", "text": user_instructions}]}],
    )

    return resp.output_text
