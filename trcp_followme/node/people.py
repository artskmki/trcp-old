#!/usr/bin/env python

import rospy
import people_msgs
from people_msgs.msg import PositionMeasurementArray 

def callback(data):
    rospy.loginfo( len(data.people))
    for p in data.people:
      rospy.loginfo(p.reliability)
      if p.reliability > 0.7:
          rospy.loginfo(p.pos.x)
        


def leg():
    rospy.init_node('leg', anonymous=True)
    rospy.Subscriber("/people_tracker_measurements", PositionMeasurementArray, callback)
    rospy.spin()


if __name__ == '__main__':
    leg()


