from pydub import AudioSegment, silence
import os

def find_split_points(audio, num_splits, min_silence_len=100, silence_thresh=-40):
    # Calculate the target split duration based on total audio length and desired number of splits
    split_duration = len(audio) // num_splits

    # Detect ranges of silence within the audio
    silence_ranges = silence.detect_silence(audio, min_silence_len, silence_thresh)

    split_points = []
    for i in range(1, num_splits):
        target_split = i * split_duration
        # Find the silence range whose midpoint is closest to the target split point
        closest_silence = min(silence_ranges, key=lambda s: abs((s[0] + s[1]) // 2 - target_split))
        # Calculate the midpoint of the closest silence range
        split_point = (closest_silence[0] + closest_silence[1]) // 2
        split_points.append(split_point)

    return split_points

# Break the audio into parts
def split_audio(input_file, output_folder, num_parts=2, min_silence_len=100, silence_thresh=-40):
    audio = AudioSegment.from_mp3(input_file)
    split_points = find_split_points(audio, num_parts, min_silence_len, silence_thresh)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    prev_split = 0
    for i, split_point in enumerate(split_points + [len(audio)]):
        part = audio[prev_split:split_point]
        part.export(os.path.join(output_folder, f"part{i+1}.mp3"), format="mp3")
        prev_split = split_point