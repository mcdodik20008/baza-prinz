import pytest
from model.translator import Translator

translator = Translator()

# Проверяем базовый перевод текста
def test_translate_text():
  input_text = "Привет, как дела?"
  expected_translation = "Hey, how's it going?"
  
  translation = translator.translate_text(input_text)
  
  assert translation == expected_translation, f"Ожидалось '{expected_translation}', но получили '{translation}'"

# Проверяем поведение при пустом вводе
def test_empty_text():
  input_text = "Привет."
  translation = translator.translate_text(input_text)
  expected_translation = "Hey, how's it going?"

  assert translation == "Hey.", f"Ожидалось '{expected_translation}', но получили '{translation}'"
