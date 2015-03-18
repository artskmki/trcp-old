#!/usr/bin/env python

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
    # How long do we have to get to each waypoint?
    self.move_base_timeout = rospy.get_param("~move_base_timeout", 10) #seconds

    # Subscribe to the move_base action server
    self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)

    rospy.loginfo("Waiting for move_base action server...")

    # Wait up to 60 seconds for the action server to become available
    self.move_base.wait_for_server(rospy.Duration(60))

    rospy.loginfo("Connected to move_base action server")
    
    # create a list to hold the target quaternions (orientations)
    quaternions = list()

    # First define the corner orientations as Euler angles
    euler_angles = (pi/2, pi, 3*pi/2, 0)

    # Then convert the angles to quaternions
    for angle in euler_angles:
        q_angle = quaternion_from_euler(0, 0, angle, axes='sxyz')
        q = Quaternion(*q_angle)
        quaternions.append(q)

    # Create a list to hold the waypoint poses
    self.waypoints = list()

    # Append each of the four waypoints to the list.  Each waypoint
    # is a pose consisting of a position and orientation in the map frame.
    self.waypoints.append(Pose(Point(0.0, -1.0, 0.0), quaternions[0]))
    self.waypoints.append(Pose(Point(0.0, 0.0, 0.0), quaternions[0]))
    self.waypoints.append(Pose(Point(2.5, -1.5, 0.0), quaternions[0]))
    self.waypoints.append(Pose(Point(4.8, -1.0, 0.0), quaternions[0]))
    self.waypoints.append(Pose(Point(4.0, 1.7, 0.0), quaternions[0]))
    self.waypoints.append(Pose(Point(3.0, 3.0, 0.0), quaternions[0]))


    # Create a mapping of room names to waypoint locations
    room_locations = (('ready_pos', self.waypoints[0]),
                      ('enter_pos', self.waypoints[1]),
                      ('pp_room', self.waypoints[2]),
                      ('at_room', self.waypoints[3]),
                      ('wdys_room', self.waypoints[4]),
                      ('leaving_arena', self.waypoints[5]))

    # Store the mapping as an ordered dictionary 
    # so we can visit the rooms in sequence
    self.room_locations = OrderedDict(room_locations)

    # Initialize the waypoint visualization markers for RViz
    init_waypoint_markers(self)

    # Set a visualization marker at each waypoint
    for waypoint in self.waypoints:
        p = Point()
        p = waypoint.position
        self.waypoint_markers.points.append(p)


    # Publisher to manually control the robot (e.g. to stop it)
    self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)

    rospy.loginfo("Starting Tasks")

    # Publish the waypoint markers
    self.marker_pub.publish(self.waypoint_markers)
    rospy.sleep(1)
    self.marker_pub.publish(self.waypoint_markers)
    
    rospy.sleep(1)

def init_waypoint_markers(self):
    # Set up our waypoint markers
    marker_scale = 0.2
    marker_lifetime = 0 # 0 is forever
    marker_ns = 'waypoints'
    marker_id = 0
    marker_color = {'r': 1.0, 'g': 0.7, 'b': 1.0, 'a': 1.0}

    # Define a marker publisher.
    self.marker_pub = rospy.Publisher('waypoint_markers', Marker)

    # Initialize the marker points list.
    self.waypoint_markers = Marker()
    self.waypoint_markers.ns = marker_ns
    self.waypoint_markers.id = marker_id
    self.waypoint_markers.type = Marker.CUBE_LIST
    self.waypoint_markers.action = Marker.ADD
    self.waypoint_markers.lifetime = rospy.Duration(marker_lifetime)
    self.waypoint_markers.scale.x = marker_scale
    self.waypoint_markers.scale.y = marker_scale
    self.waypoint_markers.color.r = marker_color['r']
    self.waypoint_markers.color.g = marker_color['g']
    self.waypoint_markers.color.b = marker_color['b']
    self.waypoint_markers.color.a = marker_color['a']

    self.waypoint_markers.header.frame_id = 'odom'
    self.waypoint_markers.header.stamp = rospy.Time.now()
    self.waypoint_markers.points = list()

