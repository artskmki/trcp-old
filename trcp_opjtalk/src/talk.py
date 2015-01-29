# -*- coding: utf-8 -*- 
import wave
import os
import pyaudio

if __name__ == "__main__":

    voice = '/usr/local/share/hts_voice/mei/'
    dic   = '/var/lib/mecab/dic/open-jtalk/'    
    text = "皆さんこんにちはー。私の名前はイレイサーです。"
 
    opts = [
            "-x  " + dic + "naist-jdic",
            "-m  " + voice + "mei_happy.htsvoice",
            "-ow " + "out.wav",
            ]

    cmd = "open_jtalk "
    for row in opts:
        cmd += row + " "
    cmd += "in.txt"

    f = open("in.txt",'w')
    f.write(text)
    f.close()

    os.system(cmd)

    wf = wave.open("out.wav", "r")

    # ストリームを開く
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # チャンク単位でストリームに出力し音声を再生
    chunk = 1024
    data = wf.readframes(chunk)
    while data != '':
        stream.write(data)
        data = wf.readframes(chunk)
    stream.close()
    p.terminate()
