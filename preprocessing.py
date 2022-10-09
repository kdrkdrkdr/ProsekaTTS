import wave
import contextlib
import jaconv


# FOR /F "tokens=*" %G IN ('dir /b *.wav') DO ffmpeg -i "%G" -ar 22050 "%~nG.wav"



def determining_dataset(path_dir):
    metadata = open(f'{path_dir}/metadata2.txt', 'w', encoding='utf-8')

    with open(f'{path_dir}/metadata.txt', 'r', encoding='utf-8') as f:
        for i in f.read().split('\n'):
            fname, transcript = i.split('|')

            with contextlib.closing(wave.open(f'{path_dir}/wavs/{fname}.wav', 'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)
                
                if (2.0 < duration < 10.0) and (10 <= len(transcript) <= 40):
                    metadata.writelines(f'{i}\n')


