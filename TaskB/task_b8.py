import speech_recognition as sr
from TaskB.task_b12 import B12
import os

def B8(audio_path, output_path):
    """
    Transcribes an MP3 audio file and saves the text output.

    Args:
        audio_path (str): Path to the input MP3 file.
        output_path (str): Path to save the transcribed text.

    Returns:
        dict: Success message or error details.
    """
    
    # Ensure paths are valid within /data/
    if not B12(audio_path) or not B12(output_path):
        return {"error": "Invalid file path. Must be within /data/."}

    # Sanitize paths to prevent directory traversal issues
    audio_path = os.path.join("data", os.path.basename(audio_path))
    output_path = os.path.join("data", os.path.basename(output_path))

    recognizer = sr.Recognizer()

    try:
        # Load the MP3 file
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)

        # Perform speech-to-text conversion
        text = recognizer.recognize_google(audio_data)

        # Save the transcription to a file
        with open(output_path, "w") as file:
            file.write(text)

        return {"success": f"Transcription saved at {output_path}"}

    except sr.UnknownValueError:
        return {"error": "Could not understand the audio."}
    except sr.RequestError:
        return {"error": "Speech recognition service is unavailable."}
    except Exception as e:
        return {"error": f"Failed to transcribe audio: {str(e)}"}
