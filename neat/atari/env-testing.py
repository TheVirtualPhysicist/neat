import gym

#env = gym.make("BipedalWalker-v2")
env = gym.make("LunarLander-v2")

observation = env.reset()

print(observation)
print(len(observation))
print(env.action_space)

done = False
while not done:
    observation, reward, done, info = env.step(env.action_space.sample())
    
    print(env.action_space.sample())
    #print(reward)

    env.render()
    