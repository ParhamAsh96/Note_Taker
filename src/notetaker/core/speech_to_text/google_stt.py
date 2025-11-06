from google.oauth2 import service_account
from google.cloud import speech


def transcribe_voice():
    client_file = "src/notetaker/core/speech_to_text/stt_API.json"
    credentials = service_account.Credentials.from_service_account_file(client_file)
    client = speech.SpeechClient(credentials=credentials)

    gs_uri = "gs://voice-data-bucket-12345/lecture_voice"
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        model="video",
        enable_automatic_punctuation=True
    )

    audio = speech.RecognitionAudio(uri=gs_uri)
    operation = client.long_running_recognize(config=config, audio=audio)


    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    full_text = " ".join(r.alternatives[0].transcript.strip() for r in response.results)

    return full_text