from deep_translator import GoogleTranslator

LANGUAGE_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es"
}

def world_translate(text, target_lang):
    try:
        target = LANGUAGE_MAP.get(target_lang, "en")

        translated = GoogleTranslator(
            source="auto",
            target=target
        ).translate(text)

        return translated

    except Exception as e:
        print(f"Translation Error: {e}")
        return text


def clone_voice(text, lang):
    """
    Placeholder function.
    Actual audio generation happens in app.py using edge-tts.
    """

    return text
