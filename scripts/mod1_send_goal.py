#! /usr/bin/env python

"""
.. module:: mod1_send_goal
   :platform: Unix
   :synopsis: Additional Python module necessary for the controller of modality 1: auto drive
   
.. moduleauthor:: Ebru Baglan baglanebru@gmail.com

The script is run upon mod1.py is initiated. Due to the problems faced, user interface and actual sending goal part of the mod1 are seperated like this. Upon receiving desired location to reach from parameter server, this node sends the coordinates to move_base/goal topic

Subscribes to:
	(parameter server) des_pos_x, des_pos_y
	
Publishes to:
	move_base/goal
"""

import rospy
from geometry_msgs.msg import Point
from move_base_msgs.msg import MoveBaseActionGoal

desired_position_ = Point()
desired_position_.x = rospy.get_param('des_pos_x')
desired_position_.y = rospy.get_param('des_pos_y')

move_msg = MoveBaseActionGoal()

move_msg.goal.target_pose.header.frame_id = 'map'
move_msg.goal.target_pose.pose.orientation.w = 1

def main():
    """
    This function is the node that sends the desired coordinate to the move_base/goal topic. It does not prints out anything, only publishes to the mentioned topic. frame_id and orientation.w are important parameters which should not be forgotten to set.
    """
    global pub, active_, desired_position_, move_msg
    i = 0

    rospy.init_node('mod1_send_goal')
    
    pub = rospy.Publisher('move_base/goal', MoveBaseActionGoal, queue_size=1)

    desired_position_.x = rospy.get_param('des_pos_x')
    desired_position_.y = rospy.get_param('des_pos_y')

    move_msg.goal.target_pose.pose.position.x = desired_position_.x
    move_msg.goal.target_pose.pose.position.y = desired_position_.y
    move_msg.goal.target_pose.header.frame_id = 'map'
    move_msg.goal.target_pose.pose.orientation.w = 1

    rate = rospy.Rate(20)  
    while not rospy.is_shutdown():
        if i < 100:
            pub.publish(move_msg)
            i= i+1
        else:
            exit()
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
