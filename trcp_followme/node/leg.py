#!/usr/bin/env python

import rospy
import people_msgs
from people_msgs.msg import PositionMeasurementArray 

def callback(data):
    rospy.loginfo(data.people[0].pos)


def leg():
    rospy.init_node('leg', anonymous=True)
    rospy.Subscriber("/leg_tracker_measurements", PositionMeasurementArray, callback)
    rospy.spin()


if __name__ == '__main__':
    leg()


