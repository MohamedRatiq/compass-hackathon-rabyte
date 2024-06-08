
import ffmpeg
from faster_whisper import WhisperModel

def create_vtt(input_video, segments, language, translate=False, translated_text={}):
     # Create a WebVTT file
    vtt_content = "WEBVTT\n\n"
    # Iterate through each segment and format it for VTT
    count = 0
    for segment in segments:
        start_hours, start_remainder = divmod(segment.start, 3600)
        start_minutes, start_seconds = divmod(start_remainder, 60)
        
        end_hours, end_remainder = divmod(segment.end, 3600)
        end_minutes, end_seconds = divmod(end_remainder, 60)
        
        # Format timestamps for VTT
        start_timestamp = f"{int(start_hours):02}:{int(start_minutes):02}:{int(start_seconds):02}.{int((segment.start - int(segment.start)) * 1000):03}"
        end_timestamp = f"{int(end_hours):02}:{int(end_minutes):02}:{int(end_seconds):02}.{int((segment.end - int(segment.end)) * 1000):03}"
        
        vtt_content+= f'{count}\n'
        if translate:
            vtt_content += f"{start_timestamp} --> {end_timestamp}\n{translated_text[(segment.text).strip()].strip()}\n\n"
            num = 2
        else:
            vtt_content += f"{start_timestamp} --> {end_timestamp}\n{(segment.text).strip()}\n\n"
            num = 1

        count+=1
    # Output the VTT content to a file
    with open(f'output{num}.vtt', 'w', encoding='utf-8') as f:
        f.write(vtt_content)

def extract_audio(input_video):
    input_video_name = input_video.replace(".mp4", "")

    extracted_audio = f"audio/{input_video_name}.wav"
    open(extracted_audio, 'w')

    stream = ffmpeg.input(f'videos/{input_video}')
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, overwrite_output=True)
    return extracted_audio

def transcribe(input_video):
    # Initialize the model
    model = WhisperModel("small")
    # Transcribe the audio file
    segments, info = model.transcribe(extract_audio(input_video))
    language = info[0]
    print("Transcription language", info[0])
    segments = list(segments)
    create_vtt(input_video, segments, language)
    print("Transcription and VTT file generation completed.")
    return language, segments