# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import numpy as np  
import math
from tqdm import tqdm
import random



# original_curve = 0.000833333*sin(3*x) from -1.2 to .5
# velocity_curve = -0.0025*cos(3*x) from -1.2 to .5



#Constants
MAX_POS = 0.5
MIN_POS = -1.2
MAX_VEL = 0.07
MIN_VEL = -0.07
TERMINAL_POS = MAX_POS
ACTIONS = [-1,0,1]

EPSILON = 1.0
GAMMA = 1.0
TILINGS = 8
WEIGHT_DIMENSIONALITY = 2**11

#I dont know why the scaling is needed yet. For now, Im lifting it from the source code without understanding 
POSITION_SCALE = TILINGS / (MAX_POS - MIN_POS)
VELOCITY_SCALE = TILINGS / (MAX_VEL - MIN_VEL)



class Environment:
    def __init__(self, starting_position = 0.0, starting_velocity = 0.0):
        self.pos = starting_position
        self.vel = starting_velocity

    def update(self, acceleration):
        if acceleration not in ACTIONS:
            raise ValueError("Invalid Acceleration")
        if self.pos == MAX_POS:
            return 0.0
        acc = acceleration
        self.vel = max(min(self.vel+0.001*acc-0.0025*math.cos(3*self.pos),MAX_VEL),MIN_VEL)
        self.pos = max(min(self.pos+self.vel,MAX_POS),MIN_POS)
        if self.pos == MAX_POS:
            return 0.0
        return -1.0

    def get_state(self):
        return (self.pos, self.vel)

    def get_pos(self):
        return self.pos

    def get_vel(self):
        return self.vel



#######################################################################
# Copyright (C)                                                       #
# 2016-2018 Shangtong Zhang(zhangshangtong.cpp@gmail.com)             #
# 2016 Kenta Shimada(hyperkentakun@gmail.com)                         #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################
#######################################################################
# Following are some utilities for tile coding from Rich.
# To make each file self-contained, I copied them from
# http://incompleteideas.net/tiles/tiles3.py-remove
# with some naming convention changes
#
# Tile coding starts
class IHT:
    "Structure to handle collisions"
    def __init__(self, size_val):
        self.size = size_val
        self.overfull_count = 0
        self.dictionary = {}

    def count(self):
        return len(self.dictionary)

    def full(self):
        return len(self.dictionary) >= self.size

    def get_index(self, obj, read_only=False):
        d = self.dictionary
        if obj in d:
            return d[obj]
        elif read_only:
            return None
        size = self.size
        count = self.count()
        if count >= size:
            if self.overfull_count == 0: print('IHT full, starting to allow collisions')
            self.overfull_count += 1
            return hash(obj) % self.size
        else:
            d[obj] = count
            return count

def hash_coords(coordinates, m, read_only=False):
    if isinstance(m, IHT): return m.get_index(tuple(coordinates), read_only)
    if isinstance(m, int): return hash(tuple(coordinates)) % m
    if m is None: return coordinates

def tiles(iht_or_size, num_tilings, floats, ints=None, read_only=False):
    """returns num-tilings tile indices corresponding to the floats and ints"""
    if ints is None:
        ints = []
    qfloats = [math.floor(f * num_tilings) for f in floats]
    tiles = []
    for tiling in range(num_tilings):
        tilingX2 = tiling * 2
        coords = [tiling]
        b = tiling
        for q in qfloats:
            coords.append((q + b) // num_tilings)
            b += tilingX2
        coords.extend(ints)
        tiles.append(hash_coords(coords, iht_or_size, read_only))
    return tiles
# Tile coding ends
#######################################################################



class Value_function():
    def __init__(self,alpha: float):
        self.hashmap = IHT(WEIGHT_DIMENSIONALITY)
        self.weights_vector = np.zeros(WEIGHT_DIMENSIONALITY)
        self.adjusted_alpha = alpha / TILINGS

        self.seen_states = set()

    def get_active_tiles(self,position: float, velocity: float, action: int):
        self.seen_states.add((position, velocity))

        p = position * POSITION_SCALE 
        v = velocity * VELOCITY_SCALE
        return tiles(self.hashmap, TILINGS, (p,v), [action])

    def get_value_estimate(self,position: float, velocity: float, action: int):
        active_tiles = self.get_active_tiles(position,velocity,action)
        current_value_estimate = np.sum(self.weights_vector[active_tiles])
        return current_value_estimate

    def update_weights(self,position: float, velocity: float, action: int, target: float):
        active_tiles = self.get_active_tiles(position,velocity,action)
        current_value_estimate = np.sum(self.weights_vector[active_tiles]) 
        #This is allowed because-for a tile-just being included in 'active_tiles' means that its associated weight is active
        #the 'gradient' on q is just telling us which weights to update
        for active_tile in active_tiles:
            self.weights_vector[active_tile] += self.adjusted_alpha*(target - current_value_estimate)

    def cost_to_go(self,position,velocity):
        values = []
        for action in ACTIONS:
            values.append(self.get_value_estimate(position,velocity,action))
        return -1 * max(values)



def get_action(position, velocity, value_function: Value_function):
    if random.random() > EPSILON:
        return random.choice(ACTIONS)
    else:
        values = []
        for action in ACTIONS:
            values.append(value_function.get_value_estimate(position,velocity,action))
        return np.random.choice([action_ for action_,value_ in enumerate(values) if value_ == np.max(values)]) - 1 
        #This minus one is here because we are indexing from 0 but our actions start at -1



#This is for one episode. Call this multiple times with the same value function
def episodic_semi_gradient_sarsa(value_function: Value_function, vis_step = -1, ax = None):
    position = float(random.randrange(-60, -40))/100 #between -.6 and -.4 with one extra sigfig
    position = -0.6
    velocity = 0.0
    action = get_action(position, velocity, value_function)
    environment = Environment(position,velocity)
    steps = 0
    while(True):

        reward = environment.update(action)
        next_position = environment.get_pos()
        next_velocity = environment.get_vel()

        if ((vis_step == 0 and next_position == TERMINAL_POS) or (vis_step > 0 and steps == vis_step)):
            positions = []
            velocities = []
            costs_to_go = []
            for seen_state in value_function.seen_states:
                position, velocity = seen_state[0], seen_state[1]
                positions.append(position)
                velocities.append(velocity)
                costs_to_go.append(value_function.cost_to_go(position,velocity))
            ax.scatter(positions,velocities,2)

        if next_position == TERMINAL_POS:
            value_function.update_weights(position,velocity,action,reward)
            return value_function, steps

        steps += 1
        
        next_action = get_action(next_position, next_velocity, value_function)
        target = (reward + GAMMA * value_function.get_value_estimate(next_position, next_velocity, next_action))
        value_function.update_weights(position, velocity, action, target)

        position = next_position
        velocity = next_velocity
        action = next_action



def mountain_car_example_ten_one():
    plt.figure(figsize=(10,10))

    RUNS = 10
    EPISODES = 100
    ALPHAS = [0.1,0.2,0.5]
    
    for alpha in ALPHAS:
        print(alpha)
        steps_per_episodes_per_runs = []
        for run in range(RUNS):
            print(run)
            value_function = Value_function(alpha)
            steps_per_episodes = []
            for episode in range(EPISODES):
                value_function,steps = episodic_semi_gradient_sarsa(value_function)
                steps_per_episodes.append(steps)
            steps_per_episodes_per_runs.append(steps_per_episodes)
        steps_per_episodes_averaged = np.mean(np.array(steps_per_episodes_per_runs),axis=0)
        plt.plot(steps_per_episodes_averaged,label=alpha)
    plt.legend()
    plt.show()




def test2():
    print("hello")
    fig = plt.figure(figsize=(10,10))
    vis_steps = [428,0,0]
    vis_episodes = [0,100,1000]
    episodes = 1
    value_function = Value_function(0.1)
    count = 0
    for episode in range(episodes):
        print("hello")
        if episode == vis_episodes[count]:
            ax = fig.add_subplot(1,2,count+1,projection="3d")
            value_function, steps = episodic_semi_gradient_sarsa(value_function,vis_steps[count],ax)
            count += 1
        else:
            value_function, steps = episodic_semi_gradient_sarsa(value_function)
    plt.show()



test2()



env = Environment(-0.84,0.0)
min_pos = 10000.0
max_pos = -10000.0
x = 0
while(x < 100):
    if env.update(1.0) == True:
        print("we did it")
        break
    max_pos = max(env.get_pos(),max_pos)
    min_pos = min(env.get_pos(),min_pos)

    x+=1

print(max_pos)
print(min_pos)
print((max_pos + min_pos)/2.0)




