## Contributing members

- **Ahmed Moustafa** - Model (training & testing), Physical track & model, Notebook (README), Design Doc, Presentation

- **Ramiro Gonzalez** - Notebook (README), Model (reward function), Design Doc, Presentation

- **Cristopher Torres** - Ethical Considerations Worksheet, Design Doc

- **Jaydyn Odor** - Design Doc, Track
 
## Abstract

Train a 1/18th scale AWS car to race autonomously using a Reinforcement Learning model.
 
## Background

<p align="center">
<img width="600" alt="image" src="https://user-images.githubusercontent.com/90020418/181690312-b2c0686f-72c7-4f2e-bea4-51a78c9074e2.png">
</p>

#### What is **Reinforcement Learning**?
Reinforcement Learning is a subset of Machine learning yet it differs from the other 2 basic Machine Learning paradigms (Supervised & Unsupervised). A specific difference we can point to between Reinforcement Learning and Supervised Learning is the unecessary input/output labellings as RL algorithms typically use dynamic programming techniques with the goal of automatically improving through reward maximization.

The formal definition of RL is "*an area of machine learning concerned with how intelligent agents ought to take actions in an environment in order to maximize the notion of cumulative reward.*" The basis of most Reinforcement Learning algorithms is the Markov Decision Process which is an extension of Markov Chains. Below is a labelled value iteration function which is the mathematical formula that is occuring behind the scenes for how our agent determines which actions are "better" than others at any given moment. 

<p align="center">
<img width="600" alt="image" src="https://miro.medium.com/max/1400/0*PJrz4aTgVmd1f15A">
</p>

MDP and RL can get very complicated and this basic/relevant information is only the surface of those topics so if you'd like to read more about it, checkout the links under the `Resources` header. On the note of Reinforcement Learning, it's important to understand how the AWS DeepRacer works [behind the scenes](https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-how-it-works-solution-workflow.html) to apply these concepts.

- The AWS DeepRacer service initializes the simulation with a virtual track, an agent representing the vehicle, and the background. 

<p align="center">
<img width="405" alt="image" src="https://user-images.githubusercontent.com/90020418/181265419-ac886d45-a2e5-4bec-9a15-841123f5a867.png">
</p>

- The agent embodies a policy neural network that can be tuned with hyper-parameters. The agent acts (as specified with a steering angle and a speed) based on a given state (represented by an image from the front camera). 

<h4 align="center"> <b> Hyperparameters for RL Optimization Algorithm </b></h4>
<p align="center">
<img width="760" src="https://user-images.githubusercontent.com/90020418/181080222-f37fc031-cf29-4fca-9aba-dddb3daa9dfa.png">
</p>

<p align="center">
<img width="405" alt="image" src="https://user-images.githubusercontent.com/90020418/181265419-ac886d45-a2e5-4bec-9a15-841123f5a867.png">
</p>

- The simulated environment updates the agent's position based on the agent action and returns a reward and an updated camera image. 
- The experiences collected in the form of state, action, reward, and new state are used to update the neural network periodically. The updated network models are used to create more experiences.
- The AWS DeepRacer service periodically saves the neural network model to persistent storage.


## Problem Space
&emsp;With companies like Tesla and Google paving the way for autonomous driving, machine learning has only continued to make strides towards a more automated future of 
travel. The reinforcement learning model for the AWS car was built to maximize accuracy in order for the vehicle to successfully complete a track autonomously. The 
autonomous model was operated under constant conditions for its tests, however what makes autonomous driving such a convoluted task is the required adaptability of a 
model under different conditions (i.e. visibility, road conditions, objects obstructing the road). It is fundamental to get a foundational, reinforced model that can 
make normal turns like the AWS car does prior to working with bigger vehicles in more rigorous environments.
 
## Model Creation

&emsp;To begin developing the model, we had to select values for the hyperparameters, action space, and a reward function. The hyperparameters of this project are gradient 
descent batch size, entropy, discount factor, loss type, learning rate, number of experience episodes between each policy-updating iteration, and number of epochs. The 
action space defines the limits of your vehicle. We choose the limits for steering angle and speed. There are many parameters that we are allowed to use when we are 
tuning the reward function. The ones that we used for the final model are distance_from_center, track_width, speed, waypoints, closest_waypoints, progress, and steps.
<br/>

&emsp;The AWS DeepRacer console allows us to choose when we want the training to stop. The range is from 5 to 1440 minutes. We usually kept this time unchanged, with the 
default being one hour. Each model was trained and evaluated on the re:Invent 2018 track. <br/>

&emsp;For our first two models, we used built-in reward functions and used the default hyperparameters and action space. In the first model, the agent is incentivized to 
follow the center line. The second model uses a reward function that penalizes crooked driving. For the third model, we increased the entropy of the second model, but 
the performance was worse, so we didn’t change the hyperparameters afterwards. We explored other reward functions and their performances in order to determine which 
parameters we may want to introduce to our own reward function. <br/>

&emsp;We added the speed parameter to the reward function, along with code to incentivize higher speed. Additionally, We changed the action space, increasing the max speed 
from 1 m/s to 2 m/s. We did not finish training this model because it was performing much worse than others. The speed incentive made it difficult for the agent to 
properly learn turning.<br/>

&emsp;In our fifth model, we added the steering_angle parameter and created a threshold variable. Using absolute steering_angle, we only incentivized speed if the 
steering_angle was below the threshold. That way, the model would hopefully learn that it should only speed up when it is not turning at a high angle (such as at a 
corner). In the next model, we increased both the maximum speed to 3.5 m/s and the minimum speed to 0.8 m/s. Also, we replaced the center-line incentive and its 
associated parameters with waypoints, closest_waypoints, and heading. We modified the speed incentive rewards and threshold. We used code from the AWS DeepRacer 
Developer Guide to incentivize the agent to point in the right direction. However, once again, the model was performing poorly, so we stopped training early. We 
readjusted the speed range to [0.5: 3] m/s. We reintroduced the center-line incentive, with a modification to the reward weights. We also changed the way we used 
waypoints and closest_waypoints. We used code from the identify_corner() method written in this Github repository to determine if the agent was approaching a corner. 
We added a threshold for difference between current direction and future direction that we would use, along with speed, to penalize high speed near a turn and reward 
slow speed near a turn. Additionally, we penalized slow speed on straight track and rewarded high speed on straight track. The results of this model's evaluation were 
poor.<br/>

&emsp;In the ninth model, we made changes to the previous model by adding the progress and speed parameters, changing the reward weights for all actions (instead of 
multiplying by different weights, we were now adding and subtracting) and we changed the way we used waypoints. We also increased the minimum speed to 0.6 m/s and 
added thresholds for speed and total steps. We learned that the agent performs roughly 15 steps per second. We learned how to incentivize the agent to make more 
progress more quickly using the Developer Guide. To do this, we checked the ratio of progress to 100% track completion and the ratio of current steps to the total 
steps threshold. The total steps threshold was just calculated by multiplying 15 by however many seconds we believed was a good average time, (20 seconds). We rewarded
the agent based on how much faster it had gotten to a certain point that it would have if it went at a 20-second pace. The faster it went, the greater the reward. 
This model had an average performance.<br/>

&emsp;For the next model, we once again changed the reward weights and reduced the average time to 18 seconds. We also added a piece 
of code that rewarded the agent every time it made it past certain points of the track. However, we realized that this could lead to overfitting, and so we stopped 
the training of this model before it was completed to remove this piece of code.<br/>

&emsp;The eleventh model was our final model. We changed the reward weights for the progress portion of the function and removed rewards for turning corners. After several 
evaluations, we determined that this is the best model. Although it doesn’t have the best evaluation or the fastest lap (the fastest lap was performed by model ten, 
though we quickly realized that this was a fluke), it is incredibly consistent, and within one second of the fastest overall evaluation. This was the model that we 
ended up using for the physical car. The values for the hyperparameters and action space for this model are shown below. <br/>

<p align="center">
<img width="760" src="https://user-images.githubusercontent.com/106926636/180805730-75d1d410-3614-4d55-ae27-5ac9c8bc1f97.png">
</p>

## Results

&emsp;We tested multiple models with different hyperparameters but we settled on our final model based on it's performance in the categories of both speed and consistency as both are important when transfering from a virtual to physical environment. For some additional information on our work throughout the project, ethical discussions, and results please check the `README.md`, `EthicalConsiderationsWksht.md`, and `AWS_DeepRacer_Presentation.pdf`.

<p align="center">
<img width="520" src="https://user-images.githubusercontent.com/106926636/180807406-0687d125-6b2a-4c51-a6ab-4313d2b24c7d.png">
</p>

<h4 align="center"> Evaluation Results Table </h4>
<p align="center">
<img width="500" alt="image" src="https://user-images.githubusercontent.com/90020418/181087624-b24572d1-bb97-4201-a063-41c841f00e94.png">
</p>

## Uses

&emsp;Our model is used to train the AWS car to self-drive over a miniature track. More importantly, the AWS car helps simplify the initial steps for autonomous driving. Being able to test various training models virtually and then physically allows for many advantages. Overall, this led us to a more precise car in a fraction of the time. Furthermore, our 1/18th scale model was able to perform regular turns, at average speeds, using its reinforcement learning model. Furthermore, we have seen applications of models similar to but much more complex than ours in countless companies who are on the forefront of self-driving vehicles like Tesla, Canoo, etc. 

## Improvements

### **Physical Limitations**
- The **cost** of materials for a full track and **time** to construct it with the correct angles. Trying to make a subset of the re:Invent 2018 track with poster boards and tape was difficult because we lacked the tools and space. Since our model was trained on a virtual environment with no flaws in the track, all the small issues negatively affected the performance of our robot's real-life evaluation.
- **WiFi** limitations were very frustating since it made connecting our laptop to the robot and streaming the camera's content sluggish and sometimes non-existent. The AWS DeepRacer logs also have no information on connecting to a network that is account secured like university WiFi. Our solution was to bring our own router to create a separate network that both the laptop and car could connect to.
- The **AWS DeepRacer Compute Module** caused many issues that were nearly undiagnosable without previous knowledge. Alongside WiFi limitations were the challenges that were caused by a possibly corrupt ruleset for the compute module. The webserver would not open on our computers when connected to the car even after factory resetting by installing a fresh Ubuntu OS onto it and resetting the AWS credentials. The solution was to add an "http" rule to the compute module thought that was nowhere to be found in any documentation or forums.

### **Virtual Limitations**
- Our free AWS accounts only had **10 hours for training & testing models** which made it hard to play around with all the combinations of hyperparameters as well as the fine-tuning for the reward function values which may have improved our time. Our approach to mitigate this was having each person test different models on separate accounts to get the most efficiency.

&emsp;If we had more time in the future, some goals that we would love to accomplish are the optimization of our model to be faster than 10 seconds per lap as well as testing more on other tracks to avoid overfitting to one track. With regards to the physical environment, we'd hope to create a more permanent track using EVA foam pieces so that it is collapsable/transportable. Both virtually and physically, entering a competition is something that would allow us to compare and discuss our models and training environments to others who may have more experience or understanding in the field of Reinforcement Learning and Autonomous Driving.

## Conclusion

&emsp;The tested AWS model was able to successfully run the track virtually, and a segment of the track physically. Within the parameters of this project, the scaled-down model was precise enough to safely make it through the tracks without any major crashes. Our model was not perfect however, the speed of the physical model was lackluster during its few runs. This comes to no surprise since the main limiting factor was time. Given more time we could have worked with different tracks and models to see the adaptability of our vehicle. These results would have been interesting to study since different models could have been better on certain sets. Having a foundational code for autonomous driving like the AWS car provided could be used in larger projects and studies to help further self-driving.

## Resources
- https://www.baeldung.com/cs/mdp-value-iteration
- https://towardsdatascience.com/reinforcement-learning-101-e24b50e1d292
- https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-how-it-works-action-space.html
- https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-how-it-works-solution-workflow.html


