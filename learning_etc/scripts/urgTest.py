#!/usr/bin/env python
import rospy
import smach
import smach_ros
import dynamic_reconfigure.client

from sensor_msgs.msg import LaserScan 

valores=[]
valores_total=[]

def callback(header):
  global valores
  global flag
  valores=header.ranges
#  print valores
  a= len(valores)
  print a

  print "angle_min:%f angle_max:%f" % (header.angle_min ,header.angle_max) 
  print "range_min:%f range_max:%f" % (header.range_min ,header.range_max) 

def urgTest():
  rospy.init_node('urgTest', anonymous=True)
  rospy.Subscriber("/scan", LaserScan, callback)
  rospy.spin()

if __name__== '__main__':
  urgTest()
