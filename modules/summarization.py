from transformers import pipeline


_SUMMARIZER = None


def _get_summarizer():
    global _SUMMARIZER
    if _SUMMARIZER is None:
        _SUMMARIZER = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")
    return _SUMMARIZER


def chunk_text(text, max_words=400):
    """
    Splits text into chunks of roughly max_words words.

    Parameters:
      text (str): The full text to split.
      max_words (int): Maximum number of words per chunk.

    Returns:
      list: List of text chunks.
    """
    words = text.split()
    if not words:
        return []

    chunks = []
    for idx in range(0, len(words), max_words):
        chunks.append(" ".join(words[idx: idx + max_words]))
    return chunks


def summarize_long_text(text, max_words=400, max_length=220, min_length=60, do_double_pass=True):
    """
    Summarize long text by:
      1. Splitting it into chunks,
      2. Summarizing each chunk,
      3. Combining the chunk summaries,
      4. Optionally re-summarizing the combined summary.

    Parameters:
      text (str): The full text to summarize.
      max_words (int): Maximum words per chunk.
      max_length (int): Maximum length for each summary.
      min_length (int): Minimum length for each summary.
      do_double_pass (bool): If True, run a second summarization on the combined summary.

    Returns:
      str: The final summary.
    """
    summarizer = _get_summarizer()

    text_chunks = chunk_text(text, max_words=max_words)
    if not text_chunks:
        return ""

    chunk_summaries = []
    for i, chunk in enumerate(text_chunks):
        try:
            chunk_words = max(1, len(chunk.split()))
            dynamic_max = min(max_length, max(40, chunk_words // 2))
            dynamic_min = min(min_length, max(20, dynamic_max // 3))

            summary = summarizer(
                chunk,
                max_length=dynamic_max,
                min_length=dynamic_min,
                do_sample=False,
                truncation=True,
            )
            chunk_summaries.append(summary[0]["summary_text"])
        except Exception as e:
            print(f"Error summarizing chunk {i}: {e}")

    combined_summary = " ".join(chunk_summaries).strip()
    if not combined_summary:
        return ""

    if do_double_pass and len(chunk_summaries) > 1:
        try:
            final_summary = summarizer(
                combined_summary,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
                truncation=True,
            )
            return final_summary[0]["summary_text"]
        except Exception as e:
            print("Error in double pass summarization:", e)

    return combined_summary
