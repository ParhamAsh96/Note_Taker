# LectureLens
<p align="center">
  <img src="./assets/logo.png" alt="LectureLens Logo" width="180" />
</p>

Turn any **university lecture** into **clean notes, key explanations, and take-aways**—auto-saved to Notion.

> *One lecturer. Clear notes. In Notion.*

---

## Overview

LectureLens follows a **pipe-and-filter** flow. Each stage does one job and passes the result to the next stage.

1. **Record (Audio Recorder)**
   - Captures the lecturer’s voice with **PyAudio** as a `.wav`.
   - You type `stop` in the terminal to end the recording.

2. **Upload (Cloud Storage)**
   - The `.wav` file is uploaded to **Google Cloud Storage (GCS)**.

3. **Transcribe (Speech-to-Text)**
   - **Google Speech-to-Text** converts the audio into text.
   - The raw transcript is saved as a `.json` file.

4. **Summarize & Explain (LLM)**
   - **OpenAI (o3)** reads the transcript and produces:
     - a structured **summary**,
     - short **explanations** of important parts,
     - **take-aways** with brief notes.
   - The enhanced notes are saved as a `.json` file.

5. **Publish (Notion)**
   - The final content is sent to **Notion** as a clean page (title, sections, bullets).

---

## Architecture

This project uses the **Pipe-and-Filter** style. Every *filter* takes an input, processes it, and passes an output forward.  
This makes testing and swapping parts easy (for example, changing the STT provider later).

**Architecture Diagram (placeholder):**  
> `![LectureLens Architecture](./docs/architecture-pipe-and-filter.png)`

**High-level layout**
> `![LectureLens High-level Layout](./docs/high-level-layout.png)`


---

## Technology (short list)

- **Core libraries:** `pyaudio`, `wave`, `threading`, `time`, `os`, `math`, `json`, `datetime`, `requests`  
- **APIs:** Google Cloud Storage, Google Speech-to-Text, OpenAI, Notion

> Full pins are in `requirements.txt`. This README keeps the list short on purpose.

---

## Requirements

- **Python 3.12**
- Microphone access
- Internet connection
- Accounts/keys for: **Google Cloud** (GCS + STT), **OpenAI**, **Notion**  
  > Not all APIs are free. You may need billing enabled.

---

## Setup

### 1) Get credentials

- **Google Cloud**
  - Create a project and a **service account**.
  - Enable **Cloud Storage** and **Speech-to-Text** APIs.
  - Create a **bucket** for uploads.
  - Download the service account JSON key.

- **OpenAI**
  - Create an API key with access to **o3** (or the model you choose).

- **Notion**
  - Create an **internal integration**.
  - Get the **token**.
  - Share your target **Page** or **Database** with the integration.

### 2) Environment variables

Create a `.env` (or export in your shell):

```bash
# Google
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
GCP_PROJECT=my-gcp-project
GCS_BUCKET=lecturelens-audio

# OpenAI
OPENAI_API_KEY=sk-...

# Notion
NOTION_TOKEN=secret_...
NOTION_PAGE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# or:
# NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional
ENV=production
LOG_LEVEL=INFO
```
### 3) Install
```bash
git clone `https://github.com/ParhamAsh96/Note_Taker.git`
cd <repo-folder>
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
---

## Run

> Make sure your virtual environment is active and your environment variables are set (GCS, OpenAI, Notion).

### Start the app
```bash
python3.12 main.py
```
### What happens next
1. Enter the **course name** and **lecture title** when asked.
2. Recording starts immediately. Type `stop` and press **Enter** to finish.
3. The app will:
   - upload the `.wav` to **Google Cloud Storage**,
   - transcribe it with **Google Speech-to-Text**,
   - summarize, explain key parts, and create take-aways via **OpenAI (o3)**,
   - publish the result to **Notion**.

### See your notes
Open **Notion**. A new page appears with the summary, key explanations, and take-aways.

---

### Common issues
- **Notion 401/403:** share the target page or database with your Notion integration.
- **Google auth errors:** check `GOOGLE_APPLICATION_CREDENTIALS`, project, bucket name, and IAM roles.
- **STT quota or disabled API:** enable **Speech-to-Text** in Google Cloud and ensure billing/quota.
- **OpenAI errors:** confirm `OPENAI_API_KEY` and model access in your region.
- **No mic found:** verify OS input device settings or choose the correct device index.

---

### Privacy & policy notes
- Follow your university’s rules for recording.
- Store audio and transcripts securely. Remove sensitive content before sharing.

---

### Support
If something breaks, run with higher logging (e.g., set `LOG_LEVEL=DEBUG`) and check console output.
You can also open an issue with your console logs and steps to reproduce.

---

## Contributing & License

- See [LICENSE](LICENSE) for terms.
- Pull requests are welcome. Tests, prompt improvements, and stability fixes are especially helpful.

---

### Credits

Built for students who want to **listen first** and **organize later**.  
LectureLens makes lectures **study-ready** with almost no extra work.

---
