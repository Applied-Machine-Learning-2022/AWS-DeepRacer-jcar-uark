import math

'''
    Reward function that incentivizes more progress at a fast pace,
    penalizes fast driving at corners, incentivizes staying near
    center line of track, and penalizes driving away from center line
'''

def reward_function(params):

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

    ############################
    # Steps and progress, check every 30 steps. The less steps it takes to reach 100% progress means finished faster
    ############################
    
    # reward less steps with greater progress if faster than 18 sec
    if (steps % 20) == 0 and progress/100 > (steps/TOTAL_STEPS):
        reward += progress - (steps/TOTAL_STEPS)*100

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
    
    return float(reward)