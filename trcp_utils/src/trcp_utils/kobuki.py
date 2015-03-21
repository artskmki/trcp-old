#!/usr/bin/env python
import rospy
from kobuki_msgs.msg import ButtonEvent

button0 = { ButtonEvent.Button0:0, ButtonEvent.Button1:1, ButtonEvent.Button2:2, }
button1 = { ButtonEvent.RELEASED:'Released', ButtonEvent.PRESSED:'Pressed ', }
buttonS = [ 'Released',  'Released',  'Released', ]

def ButtonEventCallback(data):
  buttonS[button0[data.button]]=button1[data.state]

def setup_kobuki(self):
  rospy.loginfo("kobuki")
  rospy.Subscriber("/mobile_base/events/button", ButtonEvent, ButtonEventCallback )


  rospy.sleep(1)
