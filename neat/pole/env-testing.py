import gym


#env = gym.make("BipedalWalker-v2")
env = gym.make("CartPole-v1")

observation = env.reset()

print(observation)
print(len(observation))
print(env.action_space)

done = False
while not done:
    #observation, reward, done, info = env.step(env.action_space.sample())
    observation, reward, done, info = env.step(env.action_space.sample())
    #print(observation,"\n\n\n")
    print(env.action_space.sample())
    #print(reward)

    env.render()
    