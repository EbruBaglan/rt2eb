#! /usr/bin/env python

## @package rt2eb
# \file mod1.py
# \brief Python script for the controller of modality 1: autonomous drive.
# \author Ebru Baglan
# \version 0.1
# \date 27/01/2022
#
# \details
#
# Subscribes to: <BR>
#	/odom
#
# Publishes to: <BR>
#	(parameter server) des_pos_x, des_pos_y
#
# Description:
#	The script is run after modality 1 is called by the user.
#	An interesting approach in this node is the usage of parameter server
#	rather than a ROS topic to transmit the information of the new goal.

import rospy
import roslaunch
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
import os
from actionlib_msgs.msg import GoalStatusArray
from datetime import datetime

##
# Global position variable
position_ = Point()


##
# \brief This function assigns position of the robot to a global variable. 
# \param msg is the message containing the position of the robot obtained from /odom.
# \param position_ is the global Point variable.
# This is a callback function to assign global position variable the position of the robot which is obtained from /odom topic.
def clbck(msg):
	global position_
	position_ = msg.pose.pose.position

##
# \brief This function launches the another node to send goal to ROS topic. 
# \param node is the mod1_send_goal.py node of the package.
# This function is to avoid a difficulty which had been faced last semester. This roundabout works by calling another node to send goal to the ROS topic.
def start_task():
    rospy.loginfo("starting...")

    package = 'rt2eb'
    executable = 'mod1_send_goal.py'
    node = roslaunch.core.Node(package, executable)

    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()

    script = launch.launch(node)
    print(script.is_alive())

##
# \brief The main function receives the (x,y) coordinate that user wants to reach, and initiates another node to reach to the target unless timeout. 
# \param x,y are the desired coordinates to reach.
# \param timeout_ is to take care of timeout.
# This function is the user interface for getting the desired coordinates, and showing user about the progress of reach. It accounts for timeout and in case of timeout_ notifies user, and asks for another goal to reach.
def main():
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
