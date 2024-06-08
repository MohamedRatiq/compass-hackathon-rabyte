from openai import AzureOpenAI
from string import Template
from whisper import transcribe, create_vtt
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
from elevenlabs import play, save, stream, Voice, VoiceSettings
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, vfx
from dotenv import load_dotenv
import os
import json

load_dotenv()

p = Template("""\
RESPOND IN JSON!!!!!!!
You are a polyglot who is fluent in multiple languages. Your job is to provide context aware translation for the provided texts in the dictionary as values. \
Try to match the length of the input text and the output text. Return the filled in json!

The text dictionary: $text

profanity_flag: $flag 
             If yes, replace bad words with BLEEP
             If no, leave as is.
             
Translate to: $language \
             
""")

client = AzureOpenAI(
    api_key=os.getenv('api_key'),
    api_version=os.getenv('api_version'),
    azure_endpoint=os.getenv('azure_endpoint')
)

ElevenLabsclient = ElevenLabs(
  api_key=os.environ['ELEVEN_LABS_API_KEY'],
)

def respond(q, model="gpt-4-0125", n=1):
    response = client.chat.completions.create(
        model=model, n=n,
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user",   "content": q},
        ],
    )

    input_tokens, output_tokens = response.usage.prompt_tokens, response.usage.completion_tokens
    return [response.choices[x].message.content for x in range(n)], input_tokens, output_tokens

def text_to_speech(texts):
    audio = ElevenLabsclient.generate(
        text=" ".join(texts.values()),
        voice="Rachel",
        model="eleven_multilingual_v2"
    )

    save(audio, "audio/translated_speech.mp3")


def speed_change(sound, speed=1.0):
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def exchange_audio(input_file, input_audio):
    video = VideoFileClip(input_file)
    audio = AudioFileClip(input_audio)

    video_duration = video.duration
    
    slow_mp3_obj = AudioSegment.from_file(input_audio)
    print(video.duration, audio.duration)
    print(audio.duration / video.duration)
    speed_update = speed_change(slow_mp3_obj, audio.duration / video.duration)
    speed_update.export(input_audio, format="mp3")

    audio = AudioFileClip(input_audio)
    if audio.duration > video.duration:
        audio = audio.subclip(0, video.duration)
    print(video.duration, audio.duration)

    video = video.set_audio(audio)
    open('videos/output.mp4', 'w')
    video.write_videofile('videos/output.mp4')

def translate(input_video,flagVal, language):
    lang, segments = transcribe(input_video)
    translated_text = respond(p.substitute(text=str({(segment.text).strip(): '' for segment in segments}),flag= flagVal, language=language))[0][0]
    
    if '`' in translated_text:
        translated_text = translated_text.strip('`')
        translated_text = translated_text.replace("json\n", "")

    translated_text = json.loads(translated_text)
    new_translated_text = {}
    i = 0
    for text in translated_text:
        new_translated_text[segments[i].text.strip()] = translated_text[text]
        i += 1

    print(new_translated_text)
  
    text_to_speech(new_translated_text)
    exchange_audio(f'videos/{input_video}', "audio/translated_speech.mp3")

    #os.system(f'ffmpeg -i videos/{input_video} -s 320x240 -b:v 16k -b:a 8k videos/{input_video}')
  
    create_vtt(input_video, segments, language, translate=True, translated_text = new_translated_text)
    return lang
