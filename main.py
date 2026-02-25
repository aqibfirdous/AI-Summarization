import os
from modules.text_extraction import extract_text_from_pdf
from modules.summarization import summarize_long_text
from modules.tts import generate_audio
from modules.video_creation_ffmpeg_python import create_video_ffmpeg_python
from modules.filename_utils import jd_number


def process_job_description(file_path, background_image, video_duration):
    print(f"Processing {file_path} ...")

    # 1. Extract text from the job description PDF.
    text = extract_text_from_pdf(file_path)
    if not text:
        print(f"No text extracted from {file_path}. Skipping.")
        return

    # 2. Summarize the extracted text using chunking.
    summary = summarize_long_text(text)
    if not summary:
        print(f"Summarization failed for {file_path}. Skipping.")
        return
    print("Summary:\n", summary)

    # 3. Convert the summary to audio.
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    audio_path = f"output_{base_name}.mp3"
    audio_path = generate_audio(summary, output_path=audio_path)
    if not audio_path:
        print(f"Audio generation failed for {file_path}. Skipping.")
        return

    # 4. Create a video from the generated audio and background image.
    video_path = f"output_{base_name}.mp4"
    video_path = create_video_ffmpeg_python(
        background_image,
        audio_path,
        output_path=video_path,
        max_duration=video_duration,
    )
    if video_path:
        print(f"Video created successfully: {video_path}\n")
    else:
        print(f"Video creation failed for {file_path}.\n")


def main():
    # Folder containing the job description PDFs.
    jd_folder = os.path.join("docs", "job_descriptions")
    background_image = os.path.join("docs", "ima.jpeg")

    # Define max durations (in seconds) for each JD number.
    video_durations = {
        1: 180,  # 3 minutes
        2: 150,  # 2.5 minutes
        3: 180,  # 3 minutes
        4: 240,  # 4 minutes
        5: 300,  # 5 minutes
    }

    # Process each job description file.
    for filename in sorted(os.listdir(jd_folder)):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(jd_folder, filename)
            jd_num = jd_number(filename)
            duration = video_durations.get(jd_num, 180)  # Default to 3 minutes if not specified.
            process_job_description(file_path, background_image, duration)


if __name__ == "__main__":
    main()
