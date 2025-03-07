import ffmpeg


def create_video_ffmpeg_python(image_path, audio_path, output_path="output_video.mp4", duration=60):
    """
    Create a video using ffmpeg-python by looping a background image and overlaying an audio track.
    The image is scaled to have even dimensions to satisfy the x264 encoder.

    Parameters:
      image_path (str): Path to the background image.
      audio_path (str): Path to the audio file.
      output_path (str): Path to save the output video.
      duration (int): Video duration in seconds.

    Returns:
      str: Path to the output video if successful, or None otherwise.
    """
    try:
        # Create input streams for image (looped) and audio.
        image_stream = ffmpeg.input(image_path, loop=1, t=duration)
        audio_stream = ffmpeg.input(audio_path)

        # Build the output stream.
        # The video filter 'scale=trunc(iw/2)*2:trunc(ih/2)*2' ensures both width and height are even.
        (
            ffmpeg
            .output(image_stream, audio_stream, output_path,
                    vcodec='libx264', acodec='aac',
                    pix_fmt='yuv420p', t=duration, shortest=None,
                    vf="scale=trunc(iw/2)*2:trunc(ih/2)*2")
            .overwrite_output()
            .run()
        )
        print(f"Video created successfully at: {output_path}")
        return output_path
    except Exception as e:
        print("Error creating video with ffmpeg-python:", e)
        return None



if __name__ == "__main__":
    image = "docs/ima.jpeg"  # Adjust path if needed.
    audio = "output_audio.mp3"  # Replace with your generated audio file path.
    video = create_video_ffmpeg_python(image, audio, output_path="output_video.mp4", duration=120)
    if video:
        print("Video creation succeeded.")
    else:
        print("Video creation failed.")
