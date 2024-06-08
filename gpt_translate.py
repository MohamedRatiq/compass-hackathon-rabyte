from openai import AzureOpenAI
from string import Template
from whisper import transcribe, create_vtt

import json

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
    create_vtt(input_video, segments, language, translate=True, translated_text = new_translated_text)
    return lang