from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class Translator:
    def __init__(self, model_name: str = "Helsinki-NLP/opus-mt-en-de"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def translate_text(self, text: str) -> str:
        inputs = self.tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
        translated = self.model.generate(**inputs)
        translated_text = self.tokenizer.decode(translated[0], skip_special_tokens=True)

        return translated_text