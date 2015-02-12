#!/usr/bin/env python

import rospy
import smach
from smach import State, StateMachine
from smach_ros import SimpleActionState, IntrospectionServer
from geometry_msgs.msg import Twist
from trcp_tasks.task_setup import *
import easygui
import datetime
from collections import OrderedDict

# A list of rooms and tasks
task_list = {'living_room':['vacuum_floor'], 'kitchen':['mop_floor'], 'bathroom':['scrub_tub', 'mop_floor'], 'hallway':['vacuum_floor']}

class VacuumFloor(State):
    def __init__(self, room, timer):
        State.__init__(self, outcomes=['succeeded','aborted','preempted'])

        self.task = 'vacuum_floor'
        self.room = room
        self.timer = timer

    def execute(self, userdata):
        rospy.loginfo('Vacuuming the floor in the ' + str(self.room))
        counter = self.timer
        while counter > 0:
            if self.preempt_requested():
                self.service_preempt()
                return 'preempted'
            rospy.loginfo(counter)
            counter -= 1
            rospy.sleep(1)

        message = "Finished vacuuming the " + str(self.room) + "!"
        rospy.loginfo(message)
        easygui.msgbox(message, title="Succeeded")

        update_task_list(self.room, self.task)

        return 'succeeded'


class MopFloor(State):
    def __init__(self, room, timer):
        State.__init__(self, outcomes=['succeeded','aborted','preempted'])

        self.task = 'mop_floor'
        self.room = room
        self.timer = timer

    def execute(self, userdata):
        rospy.loginfo('Mopping the floor in the ' + str(self.room))
        counter = self.timer
        while counter > 0:
            rospy.loginfo(counter)
            counter -= 1
            rospy.sleep(1)

        message = "Done mopping the " + str(self.room) + "!"
        rospy.loginfo(message)
        easygui.msgbox(message, title="Succeeded")

        update_task_list(self.room, self.task)

        return 'succeeded'


class ScrubTub(State):
    def __init__(self, room, timer):
        State.__init__(self, outcomes=['succeeded','aborted','preempted'])

        self.task = 'scrub_tub'
        self.room = room
        self.timer = timer

    def execute(self, userdata):
        rospy.loginfo('Cleaning the tub...')
        counter = self.timer
        while counter > 0:
            rospy.loginfo(counter)
            counter -= 1
            rospy.sleep(0.2)

        message = "The tub is clean!"
        rospy.loginfo(message)
        easygui.msgbox(message, title="Succeeded")

        update_task_list(self.room, self.task)

        return 'succeeded'


def update_task_list(room, task):
    task_list[room].remove(task)
    if len(task_list[room]) == 0:
        del task_list[room]


class main():
    def __init__(self):
        rospy.init_node('clean_house', anonymous=False)

        # Set the shutdown function (stop the robot)
        rospy.on_shutdown(self.shutdown)

        # Initialize a number of parameters and variables
        setup_task_environment(self)

        # Turn the room locations into SMACH move_base action states
        nav_states = {}

        for room in self.room_locations.iterkeys():
            nav_goal = MoveBaseGoal()
            nav_goal.target_pose.header.frame_id = 'map'
            nav_goal.target_pose.pose = self.room_locations[room]
            move_base_state = SimpleActionState('move_base', MoveBaseAction, goal=nav_goal, result_cb=self.move_base_result_cb,
                                                exec_timeout=rospy.Duration(15.0),
                                                server_wait_timeout=rospy.Duration(10.0))
            nav_states[room] = move_base_state

        ''' Create individual state machines for assigning tasks to each room '''

        # Create a state machine for the living room subtask(s)
        sm_living_room = StateMachine(outcomes=['succeeded','aborted','preempted'])

        # Then add the subtask(s)
        with sm_living_room:
            StateMachine.add('VACUUM_FLOOR', VacuumFloor('living_room', 5), transitions={'succeeded':'','aborted':'','preempted':''})

        # Create a state machine for the kitchen subtask(s)
