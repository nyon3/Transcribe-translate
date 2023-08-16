import os

def format_timecode(seconds):
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds %= 60
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"

def transcribe_audio(model, input_file, output_file, source_language, target_language):
    segments, info = model.transcribe(input_file, beam_size=2, language=source_language, task="translate")
    print(f"Detected language '{info.language}' with probability {info.language_probability}")

    with open(output_file, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments):
            f.write("%d\n" % (i + 1))
            f.write("%s --> %s\n" % (format_timecode(segment.start), format_timecode(segment.end)))
            f.write("%s\n\n" % segment.text)

    print(f"Transcribe done for {source_language} to {target_language}!")

