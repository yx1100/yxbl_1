import numpy as np
import random

# Define a simple environment
class SimpleEnv:
    def __init__(self):
        self.states = 6  # Number of states
        self.actions = 4  # Number of actions (up, down, left, right)
        self.goal = 5    # Goal state
        self.current_state = 0  # Start state
        
    def step(self, action):
        # Simple grid world: 2x3 grid
        # 0 1 2
        # 3 4 5 (5 is the goal)
        
        old_state = self.current_state
        
        # Move according to action
        if action == 0:  # up
            if self.current_state >= 3:
                self.current_state -= 3
        elif action == 1:  # down
            if self.current_state < 3:
                self.current_state += 3
        elif action == 2:  # left
            if self.current_state % 3 != 0:
                self.current_state -= 1
        elif action == 3:  # right
            if self.current_state % 3 != 2:
                self.current_state += 1
                
        # Calculate reward
        reward = -1  # Small negative reward for each move
        done = False
        
        if self.current_state == self.goal:
            reward = 100  # Big reward for reaching goal
            done = True
            
        return self.current_state, reward, done
    
    def reset(self):
        self.current_state = 0
        return self.current_state

# Q-learning agent
class QLearningAgent:
    def __init__(self, states, actions, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        self.q_table = np.zeros((states, actions))
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        
    def get_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, 3)  # Explore
        return np.argmax(self.q_table[state])  # Exploit
    
    def learn(self, state, action, reward, next_state):
        old_value = self.q_table[state, action]
        next_max = np.max(self.q_table[next_state])
        new_value = (1 - self.lr) * old_value + self.lr * (reward + self.gamma * next_max)
        self.q_table[state, action] = new_value

# Training
env = SimpleEnv()
agent = QLearningAgent(states=6, actions=4)
episodes = 1000

for episode in range(episodes):
    state = env.reset()
    done = False
    total_reward = 0
    
    while not done:
        action = agent.get_action(state)
        next_state, reward, done = env.step(action)
        agent.learn(state, action, reward, next_state)
        state = next_state
        total_reward += reward
    
    if episode % 100 == 0:
        print(f"Episode {episode}, Total Reward: {total_reward}")

print("\nFinal Q-table:")
print(agent.q_table)