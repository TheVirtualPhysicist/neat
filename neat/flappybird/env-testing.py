import gym
from flappybird import environment

#env = gym.make("BipedalWalker-v2")
#env = gym.make("LunarLander-v2")
env = environment()

observation = env.reset()

print(observation)
print(env.action_space)

done = False
while not done:
    #observation, reward, done, info = env.step(env.action_space.sample())
    observation, reward, done, info = env.step(env.sample())
    #print(observation,"\n\n\n")
    #print(env.sample())

    #env.render()
    