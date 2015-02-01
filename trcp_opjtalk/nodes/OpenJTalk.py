# -*- coding: utf-8 -*-
import wave
import os
import pyaudio

class OpenJTalk:
        def __init__(self):
    		self.voice = "/usr/local/share/hts_voice/mei/mei_happy.htsvoice"
    		self.dic = "/var/lib/mecab/dic/open-jtalk/naist-jdic"
		self.sp = "250"
		self.a  = "0.5"
		self.jf = "1.0"
		self.refreshOpts()

        def jdic(self, dic):
		self.dic = dic
		self.refreshOpts()

	def htsvoice(self, voice):
		self.voice = voice 
		self.refreshOpts()

	def speed(self, sp):
		self.sp = sp 
		self.refreshOpts()

	def allpass(self,a ):
		self.a = a 
		self.refreshOpts()

	def wofGV(self, jf):
		self.jf = jf 
		self.refreshOpts()


	def refreshOpts(self):
    		self.opts = [
            		"-x  " + self.dic ,
            		"-m  " + self.voice ,
            		"-p  " + self.sp ,
            		"-a  " + self.a ,
            		"-jf  " + self.jf ,
            		"-ow " + "out.wav",
            		]

        def say(self, sayJ):
                self.sayJ = sayJ
	        cmd = "open_jtalk "
                for row in self.opts:
                    cmd += row + " "

                cmd += "in.txt"

                f = open("in.txt",'w')
                f.write(self.sayJ)
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
