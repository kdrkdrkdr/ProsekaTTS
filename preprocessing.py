import wave
import contextlib
import os

import jaconv



def set_sample_rate(name):
    os.chdir(f'tts_dataset/{name}/mp3s/')
    os.system('FOR /F "tokens=*" %G IN (\'dir /b *.mp3\') DO ffmpeg -i "%G" -ac 1 -ar 22050 "../wavs/%~nG.wav" ')
 

def text_replacing(text):
    text = text.strip()
    text = text.lower()
    repl_lst = list('♪『』（）/')
    for i in repl_lst:
        text = text.replace(i, '')
    text = jaconv.alphabet2kata(text)
    # text = jaconv.normalize(text)
    return text



def determining_dataset(name):
    metadata = open(f'tts_dataset/{name}/metadata2.txt', 'w', encoding='utf-8')

    with open(f'tts_dataset/{name}/metadata.txt', 'r', encoding='utf-8') as f:
        for i in f.read().split('\n'):
            fname, transcript = i.split('|')

            with contextlib.closing(wave.open(f'{fname[3:]}', 'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)
                
                transcript = text_replacing(transcript)

                if (2.0 < duration < 10.0) and (10 <= len(transcript) <= 40):
                    metadata.writelines(f'{fname}|{transcript}\n')



if __name__ == '__main__':
    import sys
    import json

    char_json = json.loads(
        open('character_code.json', 'r', encoding='utf-8').read()
    )['code'] [int(sys.argv[1])] # Speaker ID

    name = char_json['name']
    character = char_json['character'] 
    char_code = char_json['char_code']

    print(name, character, char_code)

    # set_sample_rate(name)
    # determining_dataset(name)
