#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import smach
import smach_ros
import sensor_msgs
import sensor_msgs.msg
import hokuyo_node
import math
from std_msgs.msg import *
from sensor_msgs.msg import LaserScan
from smach import State, StateMachine
from smach_ros import SimpleActionState, IntrospectionServer
from geometry_msgs.msg import *
import easygui
import datetime
from collections import OrderedDict
from trcp_basic_function.task_setup import *
#from trcp_utils.kobuki import *
from kobuki_msgs.msg import ButtonEvent
import numpy as np

ranges=[]
meanDist=0.0
maxDist=-100.0
minDist= 100.0
def scanLaser(data):
    global ranges
    ranges=data.ranges
    mid_index = len(data.ranges) // 2
    dists = [val for val in ranges[mid_index-10:mid_index+10]
           if not math.isnan(val)]
    global meanDist
    meanDist =  np.mean(dists)
    global maxDist
    maxDist = np.max(dists)
    global minDist
    minDist = np.min(dists)
    rospy.loginfo('range:min mean min >'+str(minDist)+' '+str(meanDist)+' '+str(maxDist))


# for KOBUKI hardware
btn=False
button0 = { ButtonEvent.Button0:0, ButtonEvent.Button1:1, ButtonEvent.Button2:2, }
button1 = { ButtonEvent.RELEASED:'Released', ButtonEvent.PRESSED:'Pressed ', }
buttonS = [ 'Released',  'Released',  'Released', ]
def ButtonEventCallback(data):
    buttonS[button0[data.button]]=button1[data.state]
    print "push button"
    global btn
    btn = True



class BF1Task():
    def __init__(self):
        rospy.init_node('bf3task', anonymous=True)
        rospy.on_shutdown(self.shutdown)

        # Initialize Kobuki hardware
        rospy.Subscriber("/mobile_base/events/button", ButtonEvent, ButtonEventCallback )

        # Subscribe to Laser Range 
        rospy.Subscriber("/scan",LaserScan,scanLaser, queue_size=1)

        self.say_pub = rospy.Publisher('str_in', String, queue_size=10)
        self.say_pub.publish("")
        rospy.sleep(0.1)

        # Publisher to manually control the robot (e.g. to stop it)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)

        # Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)

        # Set location
        locations = dict()
        locations['PandP'] = Pose(Point(1.4, 3.0, 0.0), Quaternion(0.000, 0.000, 0.0, 1.0))
        locations['QA'] = Pose(Point(1.4, 1.0, 0.0), Quaternion(0.000, 0.000, 0.0, 1.0))
        locations['exit'] = Pose(Point(2.4, 3.0, 0.0), Quaternion(0.000, 0.000, 0.0, 1.0))



        rospy.loginfo("Waiting for move_base action server...")

        # Wait 60 seconds for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(60))
        rospy.loginfo("Connected to move base server")

        rospy.loginfo("Setting Initial Pose")
        pub = rospy.Publisher('initialpose', PoseWithCovarianceStamped)
        p   = PoseWithCovarianceStamped();
        msg = PoseWithCovariance();
        angle = 0
        q_angle = quaternion_from_euler(0, 0, angle, 'sxyz')
        q = Quaternion(*q_angle)
        msg.pose = Pose(Point(0.0, 0.0, 0.000), q);
        msg.covariance = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853];
        p.pose = msg;
        p.header.stamp = rospy.Time.now()
        p.header.frame_id="map"
        rospy.sleep(2.0)
        rospy.loginfo("Setting Pose")
        pub.publish(p);


        # Wait Button on
        rospy.loginfo("Wait Button on" )
        while True:
          if btn == True:
            break


        # Go to Pick & Place
        rospy.loginfo("Going to Pick and Place !!")
        # Set up the goal location
        self.goal = MoveBaseGoal()
        self.goal.target_pose.pose = locations['PandP']
        self.goal.target_pose.header.frame_id = 'map'
        self.goal.target_pose.header.stamp = rospy.Time.now()

        # Start the robot toward the next location
        self.move_base.send_goal(self.goal)

        # Allow 5(3x60=180) minutes to get there
        finished_within_time = self.move_base.wait_for_result(rospy.Duration(300))
        # Check for success or failure
        if not finished_within_time:
            self.move_base.cancel_goal()
            rospy.loginfo("Timed out achieving goal")
        else:
            state = self.move_base.get_state()
            if state == GoalStatus.SUCCEEDED:
              rospy.loginfo("Goal succeeded!")
            else:
              rospy.loginfo("Goal failed")




    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        self.move_base.cancel_goal()
        rospy.sleep(2)
        self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)

if __name__ == '__main__':
    try:
        BF1Task()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("BF1 task finished.")

