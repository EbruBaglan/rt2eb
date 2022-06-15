Research Track 2 - Continuous Evaluation - Solutions
================================

The single assignment of the Research Track 2, requires students to

1) Properly comment (sphinx and/or doxygen) the 3rd RT1 - assignment
2) Create a jupyter notebook to interact with the simulation of the 3rd assignment able to:
	- Switch to the different modalities, and manage them
	- Plot the robot position, the laser scanner data and reached / not-reached targets
3) Perform a statistical analysis on the first assignment, considering two different implementations (a proposed one, and student's)

1 Documentation
----------------------
The result for this part can be found in **docs/index.html**. Since the repository is private, Professor's suggestion for GitHub could not be realized.

2 Jupyter Notebook
-------------------
Previously implemented solution for Research Track 1 - Assignment 3 is reimplemented to give user a Jupyter Notebook interface. Interactive elements are presented for the user to choose among 3 different modalities of the robot's movement. The interface is able to 

1) Switch to the different modalities, and manage them
2) Plot the robot position in 3D, the laser scanner data and show the number of reached/not-reached targets when returned to the main manu.

The user is required to initiate Gazebo and Rviz by typing
```bash
$ roslaunch rt2eb ere.launch
```
Then the Jupyter notebook named **'latest.ipynb'** with 2 cells can be run to control the robot and visualize it.

Improvements can be summed as:
1) If mod2 is chosen after mod3, it is not possible to control the robot.
2) Number of targets reached/unreached could have shown in a graph.
3) The closest obstacle from laser reading could have shown as suggested in the lecture.
4) In mod3, if there is an obstacle in front, turning to the sides are also sometimes not possible(depends on the distance from sides), but going back and turning later is possible.

3 Statistical Analysis
----------------------

In the statistical analysis part of the assignment, a comparison between the proposed solution by professor and the solution of the student is performed.

The average time spent to get the third silver token and leave it behind in standard map configuration is chosen to be the performance criteria.

Z-test can be applied for this purpose as the following conditions are met.
* Sample is randomly chosen from the population.
* Mean and variance of the population distribution is known.
* Sampling distribution approximately normal (as N=38>30)
	
Also, we know the **standard deviation (σ)** of the 38 samples, so Z-test seems more suitable than T-test.

For the statistical analysis, as a **level of significance** (the risk we are willing to take by rejecting the null hypothesis), 5% is deemed appropriate.

The time spent to get the third silver token and leave it behind in standard map configuration.

In a mixture of solutions, a total of 38 run (30 proposed solution, 8 EbruB’s solution) are executed on the standard map configuration which yielded **σ=46.90  with μ=9.924.** (Check Appendix)

**Null hypothesis:** EbruB’s solution is faster than the proposed solution in terms of the time spent to get the third silver token and leave it behind in standard map configuration.

Standard deviation of the samples from the population is

<img src="https://latex.codecogs.com/svg.latex?\Large&space;SE=\frac{9.924}{\sqrt{8}}=3.5087" title="\Large SE=\frac{9.924}{\sqrt{8}}=3.5087" />

Then **z** becomes

<img src="https://latex.codecogs.com/svg.latex?\Large&space;z=\frac{27.84-46.90}{3.5087}=-5.43" title="\Large z=\frac{27.84-46.90}{3.5087}=-5.43" />

Checking Z table’s column with 0.05, as that is the level of significance chosen, the last entry is seen to be z=-3.4. The values are getting closer to 0 as the values getting further, suggesting that, the probability of observing a value below -5.43 is 0, and showing that EbruB’s solution is faster than the proposed solution in terms of the time spent to get the third silver token and leave it behind in standard map configuration.

The dataset can be found in the Appendix.

Appendix
---------------------

The dataset is made of 38 samples with 30 run executed with proposed solution, last 8 run with the student’s solution.


|     #              |     Time (s)    |     #              |     Time (s)    |     #              |     Time (s)    |     #              |     Time (s)    |
|--------------------|-----------------|--------------------|-----------------|--------------------|-----------------|--------------------|-----------------|
|     Sample   1     |     50.28       |     Sample   11    |     52.79       |     Sample   21    |     52.87       |     Sample   31    |     26.43       |
|     Sample   2     |     52.6        |     Sample   12    |     51.85       |     Sample   22    |     52.01       |     Sample   32    |     26.1        |
|     Sample   3     |     50.84       |     Sample   13    |     50.54       |     Sample   23    |     52.95       |     Sample   33    |     28.92       |
|     Sample   4     |     53.8        |     Sample   14    |     51.47       |     Sample   24    |     51.41       |     Sample   34    |     27.61       |
|     Sample   5     |     49.54       |     Sample   15    |     52.46       |     Sample   25    |     52.29       |     Sample   35    |     28.38       |
|     Sample   6     |     49.06       |     Sample   16    |     52.41       |     Sample   26    |     53.74       |     Sample   36    |     28.61       |
|     Sample   7     |     52.23       |     Sample   17    |     52.96       |     Sample   27    |     55.2        |     Sample   37    |     27.7        |
|     Sample   8     |     51.08       |     Sample   18    |     50.56       |     Sample   28    |     54.22       |     Sample   38    |     28.98       |
|     Sample   9     |     50.93       |     Sample   19    |     51.39       |     Sample   29    |     51.3        |                    |                 |
|     Sample   10    |     51.54       |     Sample   20    |     52.72       |     Sample   30    |     52.48       |                    |                 |


The statistics of the dataset are as follows.

|                             |     Population    |     EbruB       |
|-----------------------------|-------------------|-----------------|
|     Average                 |     46.90132      |     27.84125    |
|     Standard   Deviation    |     9.924608      |     1.027052    |
