import re
import requests

DEEPL_API_KEY:str = "DeepLのAPIキーを入力してください" 

def read_srt_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        segments = re.split("\n\n", content.strip())
        srt_data = []
        for segment in segments:
            lines = segment.split("\n")
            index = lines[0]
            timestamp = lines[1]
            text = " ".join(lines[2:])
            srt_data.append((index, timestamp, text))
    return srt_data

def write_srt_file(srt_data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        for index, timestamp, text in srt_data:
            file.write(f"{index}\n{timestamp}\n{text}\n\n")

def translate_text(text, source_language, target_language):
    """
    Translates the given text from the source language to the target language using the DeepL API.

    Args:
        text (str): The text to be translated.
        source_language (str): The language code of the source language. Available languages are:
            'DE' (German)
            'EN' (English)
            'FR' (French)
            'ES' (Spanish)
            'PT' (Portuguese)
            'IT' (Italian)
            'NL' (Dutch)
            'PL' (Polish)
            'RU' (Russian)
            'JA' (Japanese)
            'ZH' (Chinese)

        target_language (str): The language code of the target language. Available languages are the same as for
            source_language.

    Returns:
        str: The translated text, or None if an error occurred.
    """
    url = f"https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "source_lang": source_language,
        "target_lang": target_language,
    }
    response = requests.post(url, data=params)
    if response.status_code == 200:
        json_response = response.json()
        translated_text = json_response["translations"][0]["text"]
        return translated_text
    else:
        print("Error:", response.status_code)
        return None

input_file_path = "2023-08-11_subtitles.srt"
output_file_path = "output.srt"

srt_data = read_srt_file(input_file_path)

translated_srt_data = []
for index, timestamp, text in srt_data:
    translated_text = translate_text(text, "EN", "JA")
    if translated_text is not None:
        translated_srt_data.append((index, timestamp, translated_text))

write_srt_file(translated_srt_data, output_file_path)

print("Mission complete!")