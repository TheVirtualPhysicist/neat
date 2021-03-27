# pip3 install gym
# pip3 install neat-python

# for gym stuff: 
# apt install xvfb ffmpeg xorg-dev libsdl2-dev swig cmake
# pip3 install gym[box2d]

import multiprocessing
import os
import pickle

import neat
import numpy as np
#import cart_pole
import gym

runs_per_net = 2

# Use the NN network phenotype and the discrete actuator force function.
def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    fitnesses = []

    for runs in range(runs_per_net):
        env = gym.make("CartPole-v1")

        observation = env.reset()
        fitness = 0.0
        done = False
        while not done:

            action = net.activate(observation.flatten())
            observation, reward, done, info = env.step(np.argmax(action))#env.step(action)
            fitness += reward
            #env.render('human')

        fitnesses.append(fitness)

    return np.mean(fitnesses)


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)


def run(load=False):
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    pop = neat.Population(config)
    if load != False:
    	pop = neat.Checkpointer.restore_checkpoint(load)
    stats = neat.StatisticsReporter()
    checkpointer = neat.Checkpointer(generation_interval=10,filename_prefix='checkpoint-')
    pop.add_reporter(stats)
    pop.add_reporter(checkpointer)
    pop.add_reporter(neat.StdOutReporter(True))

    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = pop.run(pe.evaluate)

    # Save the winner.
    with open('winner', 'wb') as f:
        pickle.dump(winner, f)

    print(winner)




if __name__ == '__main__':
    run()#"checkpoint-29")