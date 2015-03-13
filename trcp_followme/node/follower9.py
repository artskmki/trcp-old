#!/usr/bin/env python
import rospy
from roslib import message
from sensor_msgs import point_cloud2
from sensor_msgs.msg import PointCloud2
from geometry_msgs.msg import Twist
from math import copysign
from sound_play.libsoundplay import SoundClient
import sys
import people_msgs
from people_msgs.msg import PositionMeasurementArray 

class Follower():
    def __init__(self):
        rospy.init_node("follower")

        # set shutdown function (stop the robot)
        rospy.on_shutdown(self.shutdown)

        # The goal distance (in meters) to keep between the robot and the person
        self.goal_z = rospy.get_param("~goal_z", 0.6)

        # How far away from the goal distance (in meters) before the robot reacts
        self.z_threshold = rospy.get_param("~z_threshold", 0.05)

        # How far away from being centered (x displacement) on the person
        # before the robot reacts
        self.x_threshold = rospy.get_param("~x_threshold", 0.05)

        # How much do we weight the goal distance (z) when making a movement
        self.z_scale = rospy.get_param("~z_scale", 1.0)

        # How much do we weight x-displacement of the person when making a movement
        self.x_scale = rospy.get_param("~x_scale", 2.5)

        # The maximum rotation speed in radians per second
        self.max_angular_speed = rospy.get_param("~max_angular_speed", 2.0)

        # The minimum rotation speed in radians per second
        self.min_angular_speed = rospy.get_param("~min_angular_speed", 0.0)

        # The max linear speed in meters per second
        self.max_linear_speed = rospy.get_param("~max_linear_speed", 0.3)

        # The minimum linear speed in meters per second
        self.min_linear_speed = rospy.get_param("~min_linear_speed", 0.1)

        # Slow down factor when stopping
        self.slow_down_factor = rospy.get_param("~slow_down_factor", 0.8)


        # Initialize the movement command
        self.move_cmd = Twist()
        # Publisher to control the robot's movement
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist)

        # Subscribe to the point cloud
        self.people_subscriber = rospy.Subscriber('/people_tracker_measurements', PositionMeasurementArray, self.set_cmd_vel, queue_size=1)

        rospy.loginfo("Subscribing to people...")

        # Wait for the people topic to become available
        rospy.wait_for_message('/people_tracker_measurements', PositionMeasurementArray)
        rospy.loginfo("Ready to follow!")

    def set_cmd_vel(self, data):
        x=y=z=0
        rospy.loginfo( len(data.people))
        if len(data.people):
            x=data.people[0].pos.x
            # Check our movement thresholds
            if (abs(x - self.goal_z) > self.z_threshold):
                # Compute the angular component of the movement
                linear_speed = (x- self.goal_z) * self.z_scale


                # Make sure we meet our min/max specifications
                self.move_cmd.linear.x = copysign(max(self.min_linear_speed,
                                        min(self.max_linear_speed, abs(linear_speed))), linear_speed)
            else:
                self.move_cmd.linear.x *= self.slow_down_factor

        else:
            # Stop the robot smoothly
            self.move_cmd.linear.x *= self.slow_down_factor
            self.move_cmd.angular.z *= self.slow_down_factor

        # Publish the movement command
        self.cmd_vel_pub.publish(self.move_cmd)



#        for p in data.people:
#          rospy.loginfo(p.reliability)
#          if p.reliability > 0.7:
#              rospy.loginfo(p.pos)
        
    def shutdown(self):
        rospy.loginfo("Stopping the robot...")

        # Unregister the subscriber to stop cmd_vel publishing
        self.people_subscriber.unregister()
        rospy.sleep(1)

        # Send an emtpy Twist message to stop the robot
        self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)





if __name__ == '__main__':
    try:
        Follower()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Follower node terminated.")


