from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

LANG_CODES = {
    "English": "eng_Latn",
    "Hindi": "hin_Deva",
    "Tamil": "tam_Taml",
    "Telugu": "tel_Telu",
    "Malayalam": "mal_Mlym",
    "Kannada": "kan_Knda"
}

def get_translator():
    if not hasattr(get_translator, "_translator"):
        model_name = "facebook/nllb-200-distilled-600M"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        get_translator._translator = (tokenizer, model)
    return get_translator._translator

def translate_summary(summary, target_lang):
    if target_lang == "English":
        return summary, None
    try:
        tokenizer, model = get_translator()
        inputs = tokenizer(summary, return_tensors="pt", max_length=1024, truncation=True)
        translated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.lang_code_to_id[LANG_CODES[target_lang]],
            max_length=512
        )
        translated_summary = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        return translated_summary, None
    except Exception as e:
        return None, str(e) 