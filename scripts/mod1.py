#! /usr/bin/env python

"""
.. module:: mod1
   :platform: Unix
   :synopsis: Python module for the controller of modality 1: auto drive
   
.. moduleauthor:: Ebru Baglan baglanebru@gmail.com

This node takes user input for the desired coordinates, communicates the results and account for the timeout. Due to a problem faced during the implementation of the code, the goal entered by user cannot be sent directly to the MoveAction, but rather is sent to another node to do the job. This trasmission to another node is made through the parameter server. It should be noted that, however, parameter server should be used for exhanging static data only. 

Subscribes to:
	/odom
	
Publishes to:
	(parameter server) des_pos_x, des_pos_y
"""

import rospy
import roslaunch
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
import os
from actionlib_msgs.msg import GoalStatusArray
from datetime import datetime

position_ = Point()
"""
Global position variable
"""

def clbck(msg):
"""
This function assigns the position of the robot to a global variable.

Args:
	msg(Pose): the message received from /odom, robot position
"""
	global position_
	position_ = msg.pose.pose.position


def start_task():
    """
    This function launches the another node to send user-entered goal to the ROS topic. 
    """
    rospy.loginfo("starting...")

    package = 'rt2eb'
    executable = 'mod1_send_goal.py'
    node = roslaunch.core.Node(package, executable)

    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()

    script = launch.launch(node)
    print(script.is_alive())

def main():
    """
    The main function receives the (x,y) coordinate that user wants to reach, and initiates another node to reach to the target unless timeout.
    """
    threshold = 0.6
    rospy.init_node('mod1')

    x = rospy.get_param("des_pos_x")
    y = rospy.get_param("des_pos_y")
    os.system('clear')
    print("Hi! We are reaching the first position: x = " + str(x) + ", y = " + str(y))
    start_task()

    os.system('clear')
    print("Hi! We are reaching the first position: x = " + str(x) + ", y = " + str(y))
    
    sub = rospy.Subscriber('/odom', Odometry, clbck)
    start_time = datetime.now()
    timeout_ = False

    rate = rospy.Rate(20)
    
    while not rospy.is_shutdown():    
        time_delta = datetime.now() - start_time
        if time_delta.total_seconds() > 90:
            timeout_=True
        
        if abs(x-position_.x) <= threshold and abs(y-position_.y) <= threshold and not timeout_:
            os.system('clear')
            print("Target reached! Please insert the next position")
            x = float(input('x : '))
            y = float(input('y : '))
            rospy.set_param("des_pos_x", x)
            rospy.set_param("des_pos_y", y)
            print("Thanks! Let's make arrangements for some seconds, then reach x = " + str(x) + ", y = " + str(y))
            start_task()
            os.system('clear')
            print("Thanks! Let's make arrangements for some seconds, then reach x = " + str(x) + ", y = " + str(y))
            start_time = datetime.now()

        elif timeout_:
            os.system('clear')
            print("Oh no! Timeout! Please insert another goal")
            x = float(input('x : '))
            y = float(input('y : '))
            rospy.set_param("des_pos_x", x)
            rospy.set_param("des_pos_y", y)
            print("Thanks! Let's make arrangements for some seconds, then reach x = " + str(x) + ", y = " + str(y))
            start_task()
            os.system('clear')
            print("Thanks! Let's make arrangements for some seconds, then reach x = " + str(x) + ", y = " + str(y))
            timeout_ = False
            start_time = datetime.now()

        else:
            continue
        
        rate.sleep()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
