
from audio_processing.split_audio import split_audio
from faster_whisper import WhisperModel
from datetime import datetime
from audio_processing.transcribe_audio import transcribe_audio

if __name__ == "__main__":
    today_date = datetime.today().strftime("%Y-%m-%d")
    output_folder = f"{today_date}_subtitles"
    model_size = "large-v2"
    model = WhisperModel(model_size, device="cuda", compute_type="float16")
    
    source_language = "en"
    target_language = "en"

    print("Transcribing audio...")
    input_file = "transcribe_source.mp3"
    transcribe_audio(model, input_file, output_folder, source_language, target_language)
    # split_audio(input_file, output_folder)

