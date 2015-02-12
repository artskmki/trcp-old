#!/usr/bin/env python

""" task_setup.py - Version 1.0 2013-12-20

    Set up a number of waypoints and a charging station for use with simulated tasks using
    SMACH and teer.

    Created for Tamagawa Robot Challenge  Project: http://okadanet.org
    Copyright (c) 2013 Hioryuki Okada.  All rights reserved.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.5
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details at:
    
    http://www.gnu.org/licenses/gpl.html
      
"""

import rospy
import actionlib
from actionlib import GoalStatus
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionFeedback
from tf.transformations import quaternion_from_euler
from visualization_msgs.msg import Marker
from math import  pi
from collections import OrderedDict

def setup_task_environment(self):
    rospy.loginfo("Waiting for ...")
    
    rospy.sleep(1)
