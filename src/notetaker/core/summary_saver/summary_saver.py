import time, json


def save_summary(raw):
    print("Summarizing...")
    time.sleep(5)
    try:
        data = json.loads(raw)

    except json.JSONDecodeError:
        data = {"summary": raw, "takeaways": []}


    with open("src/notetaker/core/data/summary.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    print("The summary file was successfully saved.\n")
