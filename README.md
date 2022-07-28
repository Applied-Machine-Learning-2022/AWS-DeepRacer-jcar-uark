[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=8127828&assignment_repo_type=AssignmentRepo)
<!--
Name of your teams' final project
-->
# AWS DeepRacer Final Project
## [National Action Council for Minorities in Engineering (NACME)](https://www.nacme.org) Google Applied Machine Learning Intensive (AMLI) at the `University of Arkansas`

<!--
List all of the members who developed the project and
link to each members respective GitHub profile
-->
Developed by: 
- [Ahmed Moustafa](https://github.com/a-mufasa) - `University of Arkansas`
- [Ramiro Gonzalez](https://github.com/ramirog034) - `University of Arkansas` 
- [Jaydyn Odor](https://github.com/Jodor101) - `University of Arkansas` 
- [Cris Torres](https://github.com/CristopherTorres1) - `Penn State University`

## Project Description
According to the "Capstone Projects" pdf, which introduced us to the possible final projects, the goal for the AWS DeepRacer Project is to "**train a 1/18th" scale car to race autonomously using Reinforcement Learning.**"

## Intro to Reinforcement Learning
Reinforcement Learning differs from the other 2 basic Machine Learning paradigms (Supervised & Unsupervised). A specific difference we can point to between Reinforcement Learning and Supervised Learning is the unecessary input/output labellings as RL algorithms typically use dynamic programming techniques with the goal of automatically improving through reward maximization. 

Reinforcement Learning differs from the other 2 basic Machine Learning paradigms (Supervised & Unsupervised). A specific difference we can point to between Reinforcement Learning and Supervised Learning is the unecessary input/output labellings as RL algorithms typically use dynamic programming techniques with the goal of automatically improving through reward maximization. 

<p align="center">
<img width="405" alt="image" src="https://user-images.githubusercontent.com/90020418/181265419-ac886d45-a2e5-4bec-9a15-841123f5a867.png">
</p>

## Dataset
The dataset our autonomous vehicle will use is the live sensor data it extracts which is used to train our model to determine the correct (highest reward) action via our reward function. This automatic *trial-and-error* process will give us a model that can respond to similar environments as our training with the same actions deemed correct by the algorithm. 

## Usage instructions
<!--
Give details on how to install fork and install your project. You can get all of the python dependencies for your project by typing `pip3 freeze requirements.txt` on the system that runs your project. Add the generated `requirements.txt` to this repo.
-->
1. Make sure you have access to the [AWS Console](https://aws.amazon.com/deepracer/getting-started/) for training & evaluating the model
2. Follow the AWS DeepRacer instruction on how to 'Create a Model' and use the default hyperparameters on the 're:Invent 2018' track.
3. Copy the code in `final_reward.py`
4. Paste the reward function code into AWS and train & evaluate the model

## Final Model: Training Configuration
<h4 align="center"> re:Invent 2018 track </h4>
<p align="center">
<img width="760" src="https://user-images.githubusercontent.com/90020418/181056919-da40df12-8db0-4f6e-9d47-897023ded8ca.png">
</p>

Training happens through an iterative process of simulation to gather experience, followed by training on the experience to update your model, followed by simulation using the new model to get new experience, followed by training on the new experience to update your model and so forth. Initially your model does not have any knowledge of which actions will lead to good outcomes. It will choose actions at random as it explores the environment. Over time it will learn which actions are better and start to exploit these. How quickly it exploits or how long it explores is a trade-off that you have to make.

<h4 align="center"> Hyperparameters for RL Optimization Algorithm </h4>
<p align="center">
<img width="760" src="https://user-images.githubusercontent.com/90020418/181080222-f37fc031-cf29-4fca-9aba-dddb3daa9dfa.png">
</p>

The screenshot below shows the training configuration for the final model. This includes the action space, which is where we set the maximum and minimum speeds for the agent, as well as the maximum and minimum steering angles. Additionally, the screenshot shows the settings for the hyperparameters, which were not altered for the final model. A separate model, using the same reward function but an increased gradient descent batch size, number of experience episodes between each policy-updating iteration, and decreased learning rate led to much more consistent training, but slower peformance upon evaluation.

<p align="center">
<img width="760" src="https://user-images.githubusercontent.com/106926636/180805730-75d1d410-3614-4d55-ae27-5ac9c8bc1f97.png">
</p>

## Elements of Reward Function

### **Initializing parameters**
<h4 align="center"> List of Variables for the Reward Function </h4>
<p align="center">
<img width="760" src="https://user-images.githubusercontent.com/90020418/181075834-6ca9f931-54c6-47ab-854c-37ad8681199e.png">
</p>

The following code block shows the first few lines for the reward function. Here, we give a brief summary of the reward function's incentives and penalties. We also read the input parameters to memory in order to use them throughout the rest of the function. After we read in the parameters, we create three variables that hold values that we will later use to incentivize staying near center line of the track. We created thresholds and initialized the reward value in the final part of this code block.

```python
# Read input parameters
distance_from_center = params['distance_from_center']
track_width = params['track_width']
speed = params['speed']
waypoints = params['waypoints']
closest_waypoints = params['closest_waypoints']
progress = params['progress']
steps = params['steps']

# Calculate 3 marks that are increasingly farther away from the center line
marker_1 = 0.1 * track_width
marker_2 = 0.25 * track_width
marker_3 = 0.5 * track_width

# initialize thresholds and reward
DIFF_HEADING_THRESHOLD = 6
SPEED_THRESHOLD = 1.8
TOTAL_STEPS = 270      # roughly 15 steps per second, 18 sec default lap
reward = 5
```
### **Progress Incentive**
After some research, we learned that the agent performs roughly 15 steps per second. The AWS DeepRacer Developer Guide (https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-reward-function-input.html) provides information regarding all of the parameters that we can modify in the reward function. The guide also provides code that shows examples of the paramaters in use. One of these examples uses the "progress" and "steps" parameters in order to code a reward function that incentivizes the agent to make more progress more quickly. To write the code block below, we used the same logic, but modified the specific numbers.

```python
############################
# Steps and progress, check every 30 steps. The less steps it takes to reach 100% progress means finished faster
############################

# reward less steps with greater progress if faster than 18 sec
if (steps % 20) == 0 and progress/100 > (steps/TOTAL_STEPS):
    reward += progress - (steps/TOTAL_STEPS)*100
```

Essentially, the "TOTAL_STEPS" variable is calculated using 15 steps per second * 18 seconds. 18 is an arbitrary value that we decided on based on the performance of the model using a default reward function. Since the agent performs 15 steps per second, it should complete 270 steps in 18 seconds. If the agent has made more progress around the track than it would have if it was driving at a constant 18 second pace, the agent is rewarded. This reward is calculated based on how much further ahead it is than it would've been if driving at an 18 second pace. We check every 20 steps.
### **Waypoints Incentive**
The waypoints parameter is an ordered list of milestones along the track center. Each track has its own unique list of waypoints. Each milestone is described as a coordinate of (xw,i, yw,i). The image below helps to visualize the manner in which waypoints are placed along a track. It is possible to retrieve the coordinates of any desired milestone at any point. This fact can be used to determine a corner in the future. 
<p align="center">
<img width="660" src="https://user-images.githubusercontent.com/106926636/180839557-41dbc386-6320-4c9e-bc54-5d0e1f0e856a.png">
</p>
In the code block below, we find the previous milestone, next milestone, and a milestone 6 points in the future. We then calculate the measure (in degrees) of the current direction we are facing, and the direction we will face 6 points in the future. We find the difference between these two variables. If this difference is greater than a certain value (stored in DIFF_HEADING_THRESHOLD), it indicates that a corner exists close ahead of the agent at the time. If the difference is greater than the threshold and the agent is going faster than the speed threshold (stored in SPEED_THRESHOLD), we penalize the agent. This works to incentivize the agent to take corners more slowly.

```python
#############################
# Waypoints: referenced code from https://github.com/MatthewSuntup/DeepRacer/blob/master/reward/reward_final.py
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
### **Centerline Incentive**
The final part of the reward function was to incentivize the agent to stay near the centerline of the track. The following code is a modified version of the first default reward function given by the AWS DeepRacer console.

```python
############################
# Center line incentives
############################

# give higher reward if the car is closer to center line and vice versa
if distance_from_center <= marker_1:
    reward += 5
elif distance_from_center <= marker_2:
    reward += 4
elif distance_from_center <= marker_3:
    reward += 3
else:
    reward -= 4
```

## Reward Graph
The reward graph shows the model's progress as it trains. It is a line graph with three lines: Average reward (training), Average percentage completion (training), and Average percentage completion (evaluating). The final reward graph is shown below.

<p align="center">
<img width="520" src="https://user-images.githubusercontent.com/106926636/180807406-0687d125-6b2a-4c51-a6ab-4313d2b24c7d.png">
</p>

## Testing Evaluation
After the training had completed, we evaluated the model using the same track that it trained on. The AWS Console allows us to perform multiple evaluations. Below, we show the result and a video of our best evaluation that we performed, where the agent drove three laps around the track during each evaluation.

<h4 align="center"> Evaluation Video </h4>
<p align="center">
    <video src="https://user-images.githubusercontent.com/90020418/181086640-ec3cd213-d36f-46be-826c-a71195dccb38.mp4">
</p>

<h4 align="center"> Evaluation Results Table </h4>
<p align="center">
<img width="500" alt="image" src="https://user-images.githubusercontent.com/90020418/181087624-b24572d1-bb97-4201-a063-41c841f00e94.png">
</p>

## Physical Testing
The entire goal of the AWS DeepRacer project is the train a Reinforcement Learning model that can be inputted into a vehicle in the real-world. To truly test our model we built the vehicle with all the necessary sensors to collect data and extract the parameters for running our trained model from earlier.

### **Building the Robot**
<h4 align="center"> Unboxed AWS DeepRacer Kit </h4>
<p align="center">
<img width="800" alt="image" src="https://user-images.githubusercontent.com/90020418/181102800-a5562416-1b2e-47a3-8898-0e74327669ab.jpeg">
</p>

<h4 align="center"> Assembled Car </h4>
<p align="center">
    <img width="500" alt="image" src="https://user-images.githubusercontent.com/90020418/181287036-b55f824a-d153-4c83-9190-ca41b82bccce.jpg">
</p>

We completed the assembly of our AWS DeepRacer Car using the instructions on [Amazon's Guide](https://aws.amazon.com/deepracer/getting-started/). After building the car we had to connect and calibrate it using a WiFi network to access the car's control panel for uploading and running our model. Below is a screenshot of the control panel for the robot.
<p align="center">
    <img width="750" alt="image" src="https://user-images.githubusercontent.com/90020418/181585081-f52a3bb5-4398-4c4b-bc74-06445f9243dc.png">
</p>


### **Building the Track**
<h4 align="center">re:Invent 2018 Track Template</h4>
<p align="center">
<img width="600" alt="image" src="https://user-images.githubusercontent.com/90020418/181532940-cc935b7f-8648-4d72-b058-ec64fc8ecd88.png">
</p>

With our time constraints and the high price and lack of availability of materials, we were not able to construct a full track but rather completed a subset of the track which was the left hand side (boxed in green above).

<h4 align="center">Final Track Subset</h4>
<p align="center">
<img width="600" alt="image" src="https://user-images.githubusercontent.com/90020418/181529698-0e6e03e5-01b6-4e67-8247-5ed24c2ce303.jpg">
</p>

### **Evaluating the Model**

## Discussion
There are a lot of things to consider... (include elements of & references to Ethical Considerations, talk about the difficult differences in virtual & physical, and provide some possible goals given more time as we were limited on time & money for a project that could take many months of fine-tuning).
