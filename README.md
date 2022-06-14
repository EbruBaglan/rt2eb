Research Track 2 - Assignment 1 - Solution
================================

In this assignment of the Research Track 2, previously implemented solution for Assignment 3 of Research Trach 1 is reimplemented to give user a Jupyter Notebook interface. Interactive elements like buttons, boxes are presented for the user to choose among 3 different modalities of the robot's movement. The interface should be able to get the user request for modality, get additional input from user depending on the modality of choice and let the robot execute one of the following behaviors:
1) autonomously reach a x,y coordinate inserted by the user
2) let the user drive the robot with the keyboard
3) let the user drive the robot assisting them to avoid collisions.

After the initialization of the robot, the output of the laser readings are shown to user through Jupyter Notebook.

Installing and running
----------------------

After you download the workspace for the following desired mods, just hit,

Mod1: autonomously reach a x,y coordinate inserted by the user
```bash
$ roslaunch final_assignment overlord.launch opt:=mod1 des_x:=-5.0 des_y:=5.0
```

Mod2: let the user drive the robot with the keyboard
```bash
$ roslaunch final_assignment overlord.launch opt:=mod2
```

Mod3: let the user drive the robot assisting them to avoid collisions.
```bash
$ roslaunch final_assignment overlord.launch opt:=mod3
```

Structure and How it works
---------
Roslaunch file gets user input mod and starts the needed nodes for the desired mod.

Mod1 starts an initializer node, which then calls for another node through roslaunch to send user input goals to move_base/goal topic.

Mod2 calls for teleopt_twist_keyboard to take user direction inputs.

Mod3 calls for a modified version teleopt_twist_keyboard(to publish on /cmd_vel_**raw**) to take user direction inputs, and calls another node to manipulate user inputs when user feels like crashing into a wall.

Flowchart
---------
![flowchart6](https://user-images.githubusercontent.com/71343894/154901294-0254529a-75bb-448d-a042-693fac1bd328.png)


Improvements
---------
1) Cancelling a goal mid-time can be added. 
3) An option to exit a node anytime can be added.
4) rosclean command can be added if user has a huge size of .ros/log initially.



Interesting things to note:
if -.py files include rosparameter setting/getting, and if the roscore is not called, it raises an error of OSError: [Errno 99] Cannot assign requested address.
Even after if the mentioned parameter is not set yet, it raises another error during make html command.


Problems Faced and Solved
---------
1) **Rviz not showing laser-scan outputs (red-lines):** It turns out Ubuntu may have some problems with GPU, and if the package has a GPU laser sensor, the output is not read. Some hero on the Internet commented this beautiful words: "You're getting messages, so it's definitely on. Please, try the non-GPU plugin (remove gpu_ everywhere in the sensor definition)." and "the root cause is an incompatibility with the graphics card/driver; what do you have? I also seem to remember having to upgrade to a newer version of Gazebo to get a GPU plugin working correctly, but that may have been specific to a different lidar model. In any case, the choice is yours whether to further pursue the GPU version of this plugin or settle for the CPU version."
Full post is here: https://answers.ros.org/question/370627/cant-see-scan-in-rviz/

2) **Rviz not showing map (no map received error):** This answer directed me towards the idea that "I should run map_server": https://get-help.robotigniteacademy.com/t/rviz-no-map-received/4721. Then, I went here: http://wiki.ros.org/map_server, which directed me downloading the 'navigation.git' in here: https://github.com/ros-planning/navigation . After catkin_make, I received the following error

```bash
Could not find a package configuration file provided by "tf2_sensor_msgs" with any of the following names:

    tf2_sensor_msgsConfig.cmake
    tf2_sensor_msgs-config.cmake
```

Then I moved on to this answer: https://answers.ros.org/question/305640/cmake-warning-has-occurred/ , which made me think that I am lacking tf2_sensor_msgs, and I should get it using

```bash
$ sudo apt-get install ros-noetic-tf2-sensor-msgs
```
Indeed, after installing that, the problem is solved.

3) **Constant spamming on the terminal by 'Warning: TF_REPEATED_DATA ignoring data with redundant timestamp...':** This turns out to be an up-to-date issue with the ticket created on here: https://github.com/ros/geometry2/issues/467

4) **the rosdep view is empty:** call 'sudo rosdep init' and 'rosdep update'
5) **Step 4 caused missing packages, and I had to start ROS directory all over:** https://answers.ros.org/question/353082/missing-packages-after-installing-rosdep-based-on-python3-rosdep2-in-noetic/


Research Track 2 - Assignment 1 - Part2 Statistics
==================================================

In the statistical analysis part of the assignment, a comparison between the proposed solution by professor and the solution of the student is performed.

The average time spent to get the third silver token and leave it behind in standard map configuration is chosen to be the performance criteria.

Z-test can be applied for this purpose as the following conditions are met.
* Sample is randomly chosen from the population.
* Mean and variance of the population distribution is known.
* Sampling distribution approximately normal (as N=38>30)
	
Also, we know the **standard deviation (σ)** of the 38 samples, so Z-test seems more suitable than T-test.

For the statistical analysis, as a **level of significance** (the risk we are willing to take by rejecting the null hypothesis), 5% is deemed appropriate.

The time spent to get the third silver token and leave it behind in standard map configuration.

In a mixture of solutions, a total of 38 run (30 proposed solution, 8 EbruB’s solution) are executed on the standard map configuration which yielded **σ=46.90  with μ=9.924.**

**Null hypothesis:** EbruB’s solution is faster than the proposed solution in terms of the time spent to get the third silver token and leave it behind in standard map configuration.

Standard deviation of the samples from the population is

<img src="https://latex.codecogs.com/svg.latex?\Large&space;SE=\frac{9.924}{\sqrt{8}}=3.5087" title="\Large SE=\frac{9.924}{\sqrt{8}}=3.5087" />
SE=9.924/√8=3.5087

Then **z** becomes

<img src="https://latex.codecogs.com/svg.latex?\Large&space;z=\frac{27.84-46.90}{3.5087}=-5.43" title="\Large z=\frac{27.84-46.90}{3.5087}=-5.43" />
z=(27.84-46.90)/3.5087=-5.43

```math
a^2+b^2=c^2
```

<img src="https://latex.codecogs.com/svg.latex?\Large&space;x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}" title="\Large x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}" />

Checking Z table’s column with 0.05, as that is the level of significance chosen, the last entry is seen to be z=-3.4. The values are getting closer to 0 as the values getting further, suggesting that, the probability of observing a value below -5.43 is 0, and showing that EbruB’s solution is faster than the proposed solution in terms of the time spent to get the third silver token and leave it behind in standard map configuration.

The dataset can be found in the Appendix.

Appendix
---------------------
