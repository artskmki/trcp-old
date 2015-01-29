#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wave
import os
import pyaudio
import rospy
from std_msgs.msg import String
from diagnostic_msgs.msg import *


def callback(data):
    rospy.loginfo(rospy.get_name() + ": I heard %s" % data.data)
    cmd = "open_jtalk "
    for row in opts:
        cmd += row + " "

    cmd += "in.txt"

    f = open("in.txt",'w')
    f.write(data.data)
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




def opjtalk():
    rospy.init_node('opjtalk', anonymous=True)
    rospy.Subscriber("jtalk", String, callback)

    voice = rospy.get_param("~voice","/usr/local/share/hts_voice/mei/mei_happy.htsvoice")
    print voice
    dic = rospy.get_param("~dic","/var/lib/mecab/dic/open-jtalk/naist-jdic")
    print dic 
    global opts
    opts = [
            "-x  " + dic ,
            "-m  " + voice ,
            "-ow " + "out.wav",
            ]

    rospy.spin()


if __name__ == '__main__':
    opjtalk()

