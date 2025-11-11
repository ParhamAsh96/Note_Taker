import time
from src.notetaker.core.audio_recorder.recorder import record_voice
from src.notetaker.core.google_storage.voice_saver import uplaod_voice
from src.notetaker.core.speech_to_text.google_stt import transcribe_voice
from src.notetaker.core.transcript_saver.transcript_saver import save_transcript
from src.notetaker.core.summariser.openai_o3 import summarize_transcript
from src.notetaker.core.summary_saver.summary_saver import save_summary
from src.notetaker.core.publisher.notion_publisher import publish_notes
from src.notetaker.core.cleaner.cleaner import clean_data


def main():
    course_name = input("Please enter the name of the course: \n")
    lecture_title = input("Please enter the lecture title: \n")
    
    # Pipe-and-Filter Style

    # Filter 1
    record_voice()

    start = time.time()
    # Filter 2
    uplaod_voice()

    # Filter 3
    full_text = transcribe_voice()

    # Filter 4
    save_transcript(course_name, lecture_title, full_text)

    # Filter 5
    summary = summarize_transcript(path="src/notetaker/core/data/transcript.json")

    # Filter 6
    save_summary(summary)
    
    # Filter 7
    publish_notes()

    # Filter 8
    clean_data()
    end = time.time()

    length = (end - start) / 60
    print(f"Operation duration: {length:.2f} minutes")


if __name__ == "__main__":
    main()