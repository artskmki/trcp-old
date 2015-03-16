#!/usr/bin/env python
import rospy

from trcp_utils.trcp_utils import *

if __name__ == '__main__':
    try:
      setup_kobuki()
    except rospy.ROSInterruptException:
        rospy.loginfo("finished.")

