[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=8127828&assignment_repo_type=AssignmentRepo)
<!--
Name of your teams' final project
-->
# AWS DeepRacer Final Project
## [National Action Council for Minorities in Engineering(NACME)](https://www.nacme.org) Google Applied Machine Learning Intensive (AMLI) at the `University of Arkansas`

<!--
List all of the members who developed the project and
link to each members respective GitHub profile
-->
Developed by: 
- [Ahmed Moustafa](https://github.com/a-mufasa) - `University of Arkansas`
- [Ramiro Gonzalez](https://github.com/ramirog034) - `University of Arkansas` 
- [Jaydyn Odor](https://github.com/Jodor101) - `University of Arkansas` 
- [Cris Torres](https://github.com/CristopherTorres1) - `Penn State University`

## Description
According to the "Capstone Projects" pdf, the goal for this project is to train "1/18th" scale car to race autonomously using reinforcement learning."

### Dataset
Reinforcement learning differs from the other two branches of ...

## Usage instructions
<!--
Give details on how to install fork and install your project. You can get all of the python dependencies for your project by typing `pip3 freeze requirements.txt` on the system that runs your project. Add the generated `requirements.txt` to this repo.
-->
1. Fork this repo
2. Change directories into your project
3. On the command line, type `pip3 install requirements.txt`
4. ....

## Final Model: Training Configuration
The screenshot below shows the training configuration for the final model. This includes the action space, which is where we set the maximum and minimum speeds for the agent, as well as the maximum and minimum steering angles. Additionally, the screenshot shows the settings for the hyperparameters, which were not altered for the final model.

<p align="center">
<img width="760" src="https://user-images.githubusercontent.com/106926636/180805730-75d1d410-3614-4d55-ae27-5ac9c8bc1f97.png">
</p>

## Elements of Reward Function
### Initializing parameters
The following code block shows the first few lines for the reward function. Here, we give a brief summary of the reward function's incentives and penalties. We also read the input parameters to memory in order to use them throughout the rest of the function. After we read in the parameters, we create three variables that hold values that we will later use to incentivize staying near center line of the track. We created thresholds and initialized the reward value in the final part of this code block.
```python
  '''
  Reward function that incentivizes more progress at a fast pace,
  penalizes fast driving at corners, incentivizes staying near
  center line of track, and penalizes driving away from center line
  '''
  
  # Read input parameters
  distance_from_center = params['distance_from_center']
  track_width = params['track_width']
  speed = params['speed']
  waypoints = params['waypoints']
  closest_waypoints = params['closest_waypoints']
  progress = params['progress']
  steps = params['steps']
  
  # Calculate 3 marks that are farther and father away from the center line
  marker_1 = 0.1 * track_width
  marker_2 = 0.25 * track_width
  marker_3 = 0.5 * track_width

  # Initialize thresholds and reward
  DIFF_HEADING_THRESHOLD = 6
  SPEED_THRESHOLD = 1.8
  TOTAL_STEPS = 270      # roughly 15 steps per second, 18 sec default lap
  reward = 5
```
### Progress Incentive
After some research, we learned that the agent performs roughly 15 steps per second. The AWS DeepRacer Developer Guide (https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-reward-function-input.html) provides information regarding all of the parameters that we can modify in the reward function. The guide also provides code that shows examples of the paramaters in use. One of these examples uses the "progress" and "steps" parameters in order to code a reward function that incentivizes the agent to make more progress more quickly. To write the code block below, we used the same logic, but modified the specific numbers.

```python
############################
# steps and progress, check every 30 steps. the less steps it takes to reach 100% progress means finished faster
############################
    # reward less steps with greater progress if faster than 18 sec
    if (steps % 20) == 0 and progress/100 > (steps/TOTAL_STEPS):
        reward += progress - (steps/TOTAL_STEPS)*100
```

Essentially, the "TOTAL_STEPS" variable is calculated using 15 steps per second * 18 seconds. 18 is an arbitrary value that we decided on based on the performance of the model using a default reward function. Since the agent performs 15 steps per second, it should complete 270 steps in 18 seconds. If the agent has made more progress around the track than it would have if it was driving at a constant 18 second pace, the agent is rewarded. This reward is calculated based on how much further ahead it is than it would've been if driving at an 18 second pace. We check every 20 steps.

### Waypoints Incentive
The waypoints parameter is an ordered list of milestones along the track center. Each track has its own unique list of waypoints. Each milestone is described as a coordinate of (xw,i, yw,i). The image below helps to visualize the manner in which waypoints are placed along a track.
<p align="center">
<img width="660" src="https://user-images.githubusercontent.com/106926636/180839557-41dbc386-6320-4c9e-bc54-5d0e1f0e856a.png">
</p>
It is possible to retrieve the coordinates of any desired milestone at any point. This fact can be used to determine a corner in the future. The following code block makes heavy use of code from the following github file: https://github.com/MatthewSuntup/DeepRacer/blob/master/reward/reward_final.py .
```python
#############################
# waypoints, heavy use of code from https://github.com/MatthewSuntup/DeepRacer/blob/master/reward/reward_final.py
#############################
# finding previous point, next point, and future point
prev_point = waypoints[closest_waypoints[0]]
next_point = waypoints[closest_waypoints[1]]
future_point = waypoints[min(len(waypoints) - 1, closest_waypoints[1]+6)]
    
# calculate headings to waypoints
heading_current = math.degrees(math.atan2(prev_point[1]-next_point[1], prev_point[0]-next_point[0]))
heading_future = math.degrees(math.atan2(prev_point[1]-future_point[1], prev_point[0]-future_point[0]))
    
# calculate difference between headings
# check we didn't choose reflex angle
diff_heading = abs(heading_current-heading_future)
if diff_heading > 180:
    diff_heading = 360 - diff_heading
    
# if diff_heading > than threshold indicates turn
# so when a turn is ahead (high diff_heading)
# penalize high speed, reward slow speed
if (diff_heading > DIFF_HEADING_THRESHOLD) and speed >= SPEED_THRESHOLD:
    reward -= 4
```
In the code block above, we find the previous milestone, next milestone, and a milestone 6 points in the future. We then calculate the measure (in degrees) of the current direction we are facing, and the direction we will face 6 points in the future. We find the difference between these two variables. If this difference is greater than a certain value (stored in DIFF_HEADING_THRESHOLD), it indicates that a corner exists close ahead of the agent at the time. If the difference is greater than the threshold and the agent is going faster than the speed threshold (stored in SPEED_THRESHOLD), we penalize the agent. This works to incentivize the agent to take corners more slowly.

## Reward Graph
The reward graph shows the model's progress as it trains. It is a line grpah with three lines: Average reward (training), Average percentage completion (training), and Average percentage completion (evaluating). The final reward graph is shown below.

<p align="center">
<img width="520" src="https://user-images.githubusercontent.com/106926636/180807406-0687d125-6b2a-4c51-a6ab-4313d2b24c7d.png">
</p>

## Post-training evaluation
After the training had completed, we evaluated the model using the same track that it trained on. The AWS Console allows us to perform multiple evaluations. Below, we show two evaluations that we performed, where the agent drove three laps around the track during each evaluation.
#### First Evaluation
<p align="center">
<img width="460" src="https://user-images.githubusercontent.com/106926636/180807992-a0d72a01-a773-45d8-84d8-1a3f62a2698f.png">
</p>

#### Second Evaluation
<p align="center">
<img width="460" src="https://user-images.githubusercontent.com/106926636/180808030-ccb2eee6-9186-4bfb-9d8a-09e56a7c4e0c.png">
</p>

