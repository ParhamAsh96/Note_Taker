import os

def clean_data():
    paths = {
        "audio": "src/notetaker/core/data/voice.wav",
        "transcript": "src/notetaker/core/data/transcript.json",
        "summary": "src/notetaker/core/data/summary.json",
    }

    print("Removing old files...")
    for name, path in paths.items():
        try:
            os.remove(path)
            print(f"The {name} file was deleted successfully.")

        except FileNotFoundError:
            print(f"The {name} file was not found.\n")
        
        except Exception as e:
            print(f"Something went wrong: {e}\n")