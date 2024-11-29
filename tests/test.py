import pytest
from model.translator import Translator

translator = Translator()

# Проверяем базовый перевод текста
def test_translate_text():
  input_text = "Привет, как дела?"
  expected_translation = "Hallo, wie geht's?"
  
  translation = translator.translate_text(input_text)
  
  assert translation == expected_translation, f"Ожидалось '{expected_translation}', но получили '{translation}'"

# Проверяем поведение при пустом вводе
def test_empty_text():
  input_text = ""
  translation = translator.translate_text(input_text)
  
  # Ожидаем пустой результат
  assert translation == "", "Перевод пустого текста должен быть пустым"
