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
<!--
Give a short description on what your project accomplishes and what tools is uses. In addition, you can drop screenshots directly into your README file to add them to your README. Take these from your presentations.
-->

## Usage instructions
<!--
Give details on how to install fork and install your project. You can get all of the python dependencies for your project by typing `pip3 freeze requirements.txt` on the system that runs your project. Add the generated `requirements.txt` to this repo.
-->
1. Fork this repo
2. Change directories into your project
3. On the command line, type `pip3 install requirements.txt`
4. ....

## Training Configuration
The screenshot below shows the training configuration for the final model. This includes the action space, which is where we set the maximum and minimum speeds for the agent, as well as the maximum and minimum steering angles. Additionally, the screenshot shows the settings for the hyperparameters, which were not altered for the final model.

<p align="center">
<img width="760" src="https://user-images.githubusercontent.com/106926636/180805730-75d1d410-3614-4d55-ae27-5ac9c8bc1f97.png">
</p>

## Reward Graph
The reward graph shows the model's progress as it trains. It is a line grpah with three lines: Average reward (training), Average percentage completion (training), and Average percentage completion (evaluating). The final reward graph is shown below.

<p align="center">
<img width="460" src="https://user-images.githubusercontent.com/106926636/180807406-0687d125-6b2a-4c51-a6ab-4313d2b24c7d.png">
</p>

## Post-training evaluation
After the training had completed, we evaluated the model using the same track that it trained on. The AWS Console allows us to perform multiple evaluations. Below, we show two evaluations that we performed, where the agent drove three laps around the track during each evaluation.

<p align="center">
<img width="460" src="https://user-images.githubusercontent.com/106926636/180807992-a0d72a01-a773-45d8-84d8-1a3f62a2698f.png">
</p>

<p align="center">
<img width="460" src="https://user-images.githubusercontent.com/106926636/180808030-ccb2eee6-9186-4bfb-9d8a-09e56a7c4e0c.png">
</p>


