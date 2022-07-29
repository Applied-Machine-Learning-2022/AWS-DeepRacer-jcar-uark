## Contributing members

Ahmed Moustafa - Physical model, Notebook

Ramiro Gonzalez - Notebook, Design Doc

Cristopher Torres - Ethical Considerations Worksheet, Design Doc

Jaydyn Odor - Design doc, Track
 
## Abstract

Train a 1/18th scale AWS car to race autonomously using a reinforcement learning model.
 
## Background

With companies like Tesla and Google paving the way for autonomous driving, machine learning has only continued to make strides towards a more automated future of 
travel. The reinforcement learning model for the AWS car was built to maximize accuracy in order for the vehicle to successfully complete a track autonomously. The 
autonomous model was operated under constant conditions for its tests, however what makes autonomous driving such a convoluted task is the required adaptability of a 
model under different conditions (i.e. visibility, road conditions, objects obstructing the road). It is fundamental to get a foundational, reinforced model that can 
make normal turns like the AWS car does prior to working with bigger vehicles in more rigorous environments.
 
## Error Handling
…
 
## Model Creation

To begin developing the model, we had to select values for the hyperparameters, action space, and a reward function. The hyperparameters of this project are gradient 
descent batch size, entropy, discount factor, loss type, learning rate, number of experience episodes between each policy-updating iteration, and number of epochs. The 
action space defines the limits of your vehicle. We choose the limits for steering angle and speed. There are many parameters that we are allowed to use when we are 
tuning the reward function. The ones that we used for the final model are distance_from_center, track_width, speed, waypoints, closest_waypoints, progress, and steps.
<br/>
The AWS DeepRacer console allows us to choose when we want the training to stop. The range is from 5 to 1440 minutes. We usually kept this time unchanged, with the 
default being one hour. Each model was trained and evaluated on the re:Invent 2018 track. <br/>
For our first two models, we used built-in reward functions and used the default hyperparameters and action space. In the first model, the agent is incentivized to 
follow the center line. The second model uses a reward function that penalizes crooked driving. For the third model, we increased the entropy of the second model, but 
the performance was worse, so we didn’t change the hyperparameters afterwards. We explored other reward functions and their performances in order to determine which 
parameters we may want to introduce to our own reward function. <br/>
We added the speed parameter to the reward function, along with code to incentivize higher speed. Additionally, We changed the action space, increasing the max speed 
from 1 m/s to 2 m/s. We did not finish training this model because it was performing much worse than others. The speed incentive made it difficult for the agent to 
properly learn turning.<br/>
In our fifth model, we added the steering_angle parameter and created a threshold variable. Using absolute steering_angle, we only incentivized speed if the 
steering_angle was below the threshold. That way, the model would hopefully learn that it should only speed up when it is not turning at a high angle (such as at a 
corner). In the next model, we increased both the maximum speed to 3.5 m/s and the minimum speed to 0.8 m/s. Also, we replaced the center-line incentive and its 
associated parameters with waypoints, closest_waypoints, and heading. We modified the speed incentive rewards and threshold. We used code from the AWS DeepRacer 
Developer Guide to incentivize the agent to point in the right direction. However, once again, the model was performing poorly, so we stopped training early. We 
readjusted the speed range to [0.5: 3] m/s. We reintroduced the center-line incentive, with a modification to the reward weights. We also changed the way we used 
waypoints and closest_waypoints. We used code from the identify_corner() method written in this Github repository to determine if the agent was approaching a corner. 
We added a threshold for difference between current direction and future direction that we would use, along with speed, to penalize high speed near a turn and reward 
slow speed near a turn. Additionally, we penalized slow speed on straight track and rewarded high speed on straight track. The results of this model's evaluation were 
poor.<br/>
In the ninth model, we made changes to the previous model by adding the progress and speed parameters, changing the reward weights for all actions (instead of 
multiplying by different weights, we were now adding and subtracting) and we changed the way we used waypoints. We also increased the minimum speed to 0.6 m/s and 
added thresholds for speed and total steps. We learned that the agent performs roughly 15 steps per second. We learned how to incentivize the agent to make more 
progress more quickly using the Developer Guide. To do this, we checked the ratio of progress to 100% track completion and the ratio of current steps to the total 
steps threshold. The total steps threshold was just calculated by multiplying 15 by however many seconds we believed was a good average time, (20 seconds). We rewarded
the agent based on how much faster it had gotten to a certain point that it would have if it went at a 20-second pace. The faster it went, the greater the reward. 
This model had an average performance.<br/>
For the next model, we once again changed the reward weights and reduced the average time to 18 seconds. We also added a piece 
of code that rewarded the agent every time it made it past certain points of the track. However, we realized that this could lead to overfitting, and so we stopped 
the training of this model before it was completed to remove this piece of code.<br/>
The eleventh model was our final model. We changed the reward weights for the progress portion of the function and removed rewards for turning corners. After several 
evaluations, we determined that this is the best model. Although it doesn’t have the best evaluation or the fastest lap (the fastest lap was performed by model ten, 
though we quickly realized that this was a fluke), it is incredibly consistent, and within one second of the fastest overall evaluation. This was the model that we 
ended up using for the physical car. The values for the hyperparameters and action space for this model are shown below. <br/>

<p align="center">
<img width="760" src="https://user-images.githubusercontent.com/106926636/180805730-75d1d410-3614-4d55-ae27-5ac9c8bc1f97.png">
</p>

## Results

Multiple models were tested...

<p align="center">
<img width="520" src="https://user-images.githubusercontent.com/106926636/180807406-0687d125-6b2a-4c51-a6ab-4313d2b24c7d.png">
</p>

<h4 align="center"> Evaluation Results Table </h4>
<p align="center">
<img width="500" alt="image" src="https://user-images.githubusercontent.com/90020418/181087624-b24572d1-bb97-4201-a063-41c841f00e94.png">
</p>

## Uses

Our model is used to train the AWS car to self-drive over a miniature track. More importantly, the AWS car helps simplify the initial steps for autonomous driving. Being able to test various training models virtually and then physically allows for many advantages. Overall, this led us to a more precise car in a fraction of the time. Furthermore, our 1/18th scale model was able to perform regular turns, at average speeds, using its reinforcement learning model.

## Improvements

One of  the issues we had with this project was the physical car itself. Though we were able to make the virtual model to work, we had a problem getting the physical model to run. The first problem we encountered was trying to find a physical hard drive big enough to hold the model. Another problem we had was to get it connected to the internet. Since the regular Uark wifi was unavailable, we used the guest wifi as a substitute. This ended up being a mistake as the guest wifi would not allow us to work.

## Conclusion

The tested AWS model was able to successfully run the track virtually, and a segment of the track physically. Within the parameters of this project, the scaled-down model was precise enough to safely make it through the tracks without any major crashes. Our model was not perfect however, the speed of the physical model was lackluster during its few runs. This comes to no surprise since the main limiting factor was time. Given more time we could have worked with different tracks and models to see the adaptability of our vehicle. These results would have been interesting to study since different models could have been better on certain sets. Having a foundational code for autonomous driving like the AWS car provided could be used in larger projects and studies to help further self-driving.


