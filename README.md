# AI Summarization to Audio/Video Pipeline

This project processes job description PDFs and generates:
1. A text summary using a transformer summarization model.
2. An MP3 narration from the summary using Google Text-to-Speech.
3. An MP4 video by combining a static background image with the narration.

## Project structure

- `main.py` — pipeline entrypoint.
- `modules/text_extraction.py` — PDF text extraction (`PyPDF2`).
- `modules/summarization.py` — chunked summarization with optional double pass.
- `modules/tts.py` — TTS generation (`gTTS`).
- `modules/video_creation_ffmpeg_python.py` — video generation (`ffmpeg-python` + `ffmpeg` binary).
- `modules/filename_utils.py` — helper to parse JD number from filenames.
- `tests/test_filename_utils.py` — unit tests for filename parsing.
- `docs/job_descriptions/` — input PDFs.
- `docs/ima.jpeg` — background image for generated videos.

## Requirements

- Python 3.10+
- `ffmpeg` installed and available on PATH
- Python dependencies listed in `requirements.txt.`

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Input naming and duration mapping

The pipeline extracts JD numbers from filenames such as:

- `jd1.pdf`
- `jd_1.pdf`
- `jd_2 (1).pdf`

Then it uses that number to pick a max video duration from `video_durations` in `main.py`.

## How to run

```bash
python main.py
```

For each PDF in `docs/job_descriptions/`, the script will:
- extract text,
- summarize it,
- generate `output_<pdf_basename>.mp3`,
- generate `output_<pdf_basename>.mp4`.

## Testing

Run unit tests:

```bash
python -m unittest discover -s tests -p 'test.py.'
```

## Notes and troubleshooting

- If summarization fails on first run, ensure model dependencies are installed, andthe  internet is available for model download.
- If audio generation fails, verify outbound network access for `gTTS`.
- If video generation fails, confirm `ffmpeg` is installed:

```bash
ffmpeg -version
```

## License

See `LICENSE`.
