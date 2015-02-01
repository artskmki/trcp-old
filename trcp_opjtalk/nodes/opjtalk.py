#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wave
import os
import pyaudio
import time 
import rospy
from std_msgs.msg import String
from diagnostic_msgs.msg import *
from OpenJTalk import *

def callback(data):
    rospy.loginfo(rospy.get_name() + ": I heard %s" % data.data)

    ojt.say(data.data)

def opjtalk():
    rospy.init_node('opjtalk', anonymous=True)
    rospy.Subscriber("jtalk", String, callback)

    global ojt 
    ojt = OpenJTalk()
    ojt.say("みなさんこんにちは、")

    ojt.htsvoice(rospy.get_param("~voice","/usr/local/share/hts_voice/mei/mei_happy.htsvoice"))
    ojt.jdic(rospy.get_param("~dic","/var/lib/mecab/dic/open-jtalk/naist-jdic"))
    ojt.speed("100")
    ojt.allpass("0.3")
    ojt.wofGV("0")
    ojt.say("みなさんこんにちは、私の名前は岡田")


    rospy.spin()

if __name__ == '__main__':
    opjtalk()

