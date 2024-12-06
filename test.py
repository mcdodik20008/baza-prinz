from model.translator import Translator


translator = Translator()


# Проверяем базовый перевод текста
def test_translate_text():
    input_text = "Привет, как дела?"
    expected_translation = "Hey, how's it going?"
    translation = translator.translate_text(input_text)
    message_error = (f"Ожидалось '{expected_translation}', "
                     f"но получили '{translation}'")
    assert translation == expected_translation, message_error


# Проверяем поведение при пустом вводе
def test_empty_text():
    input_text = "Привет."
    translation = translator.translate_text(input_text)
    expected_translation = "Hey, how's it going?"
    message_error = (f"Ожидалось '{expected_translation}', "
                     f"но получили '{translation}'")
    assert translation == "Hey.", message_error
