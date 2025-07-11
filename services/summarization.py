from transformers import pipeline

def get_summarizer():
    if not hasattr(get_summarizer, "_summarizer"):
        get_summarizer._summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    return get_summarizer._summarizer

def summarize_text(transcript):
    try:
        summarizer = get_summarizer()
        def chunk_text(text, max_tokens=1024):
            words = text.split()
            for i in range(0, len(words), max_tokens):
                yield " ".join(words[i:i+max_tokens])
        summary = ""
        for chunk in chunk_text(transcript):
            summary_piece = summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
            summary += summary_piece + " "
        return summary.strip(), None
    except Exception as e:
        return None, str(e) 