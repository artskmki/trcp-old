#! /usr/bin/env python

import rospy

from smach import StateMachine
from smach_ros import ActionServerWrapper

# Construct state machine
sm = StateMachine(outcomes=['did_something',
                            'did_something_else',
                            'aborted',
                            'preempted'])
with sm:
    ### Add states in here...

# Construct action server wrapper
asw = ActionServerWrapper(
    'my_action_server_name', MyAction,
    wrapped_container = sm,
    succeeded_outcomes = ['did_something','did_something_else'],
    aborted_outcomes = ['aborted'],
    preempted_outcomes = ['preempted'] )

# Run the server in a background thread
asw.run_server()

# Wait for control-c
rospy.spin()
