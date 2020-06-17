import speech_recognition as sr
import os

def recognize_speech_from_file(recognizer):
    """Transcribe speech from recorded from `microphone`.
    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # recognize from audio.wav file
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    savedAudio_path = os.path.join(BASE_DIR, "answer", "saved_data", "savedAudio.wav")

    recorded_audio = sr.AudioFile(savedAudio_path)
    with recorded_audio as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

def convert():
    # create recognizer and mic instances
    recognizer = sr.Recognizer()

    query = recognize_speech_from_file(recognizer)

    if query["error"]:
        return 1, query["error"]
    else:
        return 0, query["transcription"]

# if __name__ == "__main__":
#   say()
