import ffmpeg


def _audio_duration_seconds(audio_path):
    """Return audio duration in seconds if detectable, otherwise None."""
    try:
        metadata = ffmpeg.probe(audio_path)
        return float(metadata["format"]["duration"])
    except Exception:
        return None


def create_video_ffmpeg_python(image_path, audio_path, output_path="output_video.mp4", max_duration=60):
    """
    Create a video by looping a background image and overlaying an audio track.

    If max_duration is set, the output duration is capped to it. Otherwise output
    matches the audio duration. Uses shortest=1 to avoid trailing black/silent tails.

    Parameters:
      image_path (str): Path to the background image.
      audio_path (str): Path to the audio file.
      output_path (str): Path to save the output video.
      max_duration (int|float|None): Optional max video duration in seconds.

    Returns:
      str: Path to the output video if successful, or None otherwise.
    """
    try:
        audio_duration = _audio_duration_seconds(audio_path)

        if max_duration is None:
            target_duration = audio_duration
        elif audio_duration is None:
            target_duration = max_duration
        else:
            target_duration = min(float(max_duration), audio_duration)

        image_kwargs = {"loop": 1}
        output_kwargs = {
            "vcodec": "libx264",
            "acodec": "aac",
            "pix_fmt": "yuv420p",
            "shortest": 1,
            "vf": "scale=trunc(iw/2)*2:trunc(ih/2)*2",
        }

        if target_duration is not None:
            image_kwargs["t"] = target_duration
            output_kwargs["t"] = target_duration

        image_stream = ffmpeg.input(image_path, **image_kwargs)
        audio_stream = ffmpeg.input(audio_path)

        (
            ffmpeg.output(image_stream, audio_stream, output_path, **output_kwargs)
            .overwrite_output()
            .run()
        )
        print(f"Video created successfully at: {output_path}")
        return output_path
    except Exception as e:
        print("Error creating video with ffmpeg-python:", e)
        return None


if __name__ == "__main__":
    image = "docs/ima.jpeg"
    audio = "output_audio.mp3"
    video = create_video_ffmpeg_python(image, audio, output_path="output_video.mp4", max_duration=120)
    if video:
        print("Video creation succeeded.")
    else:
        print("Video creation failed.")
