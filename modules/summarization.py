from transformers import pipeline


def chunk_text(text, max_tokens=1024):
    """
    Splits text into chunks of roughly max_tokens words.

    Parameters:
      text (str): The full text to split.
      max_tokens (int): Maximum number of words per chunk.

    Returns:
      list: List of text chunks.
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    for word in words:
        # Assume each word roughly equals one token.
        if current_length + 1 > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = 1
        else:
            current_chunk.append(word)
            current_length += 1
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks


def summarize_long_text(text, max_tokens=1024, max_length=300, min_length=150, do_double_pass=True):
    """
    Summarize long text by:
      1. Splitting it into chunks,
      2. Summarizing each chunk with a higher max and min length,
      3. Combining the chunk summaries,
      4. Optionally re-summarizing the combined summary for a more detailed final output.

    Parameters:
      text (str): The full text to summarize.
      max_tokens (int): Maximum words per chunk.
      max_length (int): Maximum length for each summary.
      min_length (int): Minimum length for each summary.
      do_double_pass (bool): If True, run a second summarization on the combined summary.

    Returns:
      str: The final summary.
    """
    # Use a smaller summarization model (or choose one that fits your needs)
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")

    # Split the input text into chunks
    text_chunks = chunk_text(text, max_tokens=max_tokens)

    chunk_summaries = []
    for i, chunk in enumerate(text_chunks):
        try:
            summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
            chunk_summaries.append(summary[0]['summary_text'])
        except Exception as e:
            print(f"Error summarizing chunk {i}: {e}")

    combined_summary = " ".join(chunk_summaries)

    # Optional double-pass summarization for more detail and coherence
    if do_double_pass and len(combined_summary.split()) > min_length:
        try:
            final_summary = summarizer(combined_summary, max_length=max_length, min_length=min_length, do_sample=False)
            return final_summary[0]['summary_text']
        except Exception as e:
            print("Error in double pass summarization:", e)
            # Return the combined summary if the second pass fails
            return combined_summary
    else:
        return combined_summary