from gtts import gTTS

def generate_audio(text, output_path="output_audio.mp3", lang="en"):
    """
    Convert text to speech using gTTS and save as an MP3 file.

    Parameters:
      text (str): Text to convert.
      output_path (str): Path to save the MP3.
      lang (str): Language code.

    Returns:
      str: Path to the saved audio file.
    """
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(output_path)
        return output_path
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None
