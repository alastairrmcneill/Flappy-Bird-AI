"""
Author: Alastair McNeill
Recreate the Flappy Bird game within Python using pygame.
Has ability to restart after crash, pixel perfect collisions and high score tracking
"""

# Imports
import pygame
import os
import neat
from FlappyBird.Constants import WIN_HEIGHT, WIN_WIDTH, FPS, base_path
from FlappyBird.Game import Game
from FlappyBird.Bird import Bird


# Variables and constants
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Main function
def main(genomes, config):
    """
    Main game loop that handles inputs
    """
    run = True
    game = Game(WIN)

    nets = []
    ge = []
    birds = []

    for g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(WIN))
        g.fitness = 0
        ge.append(g)




    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()


        pipe_ind = 0
        if len(birds) > 0:
            if birds[0].x > game.pipes[0].right():
                pipe_ind = 0
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y,
                                      abs(bird.y - game.pipes[pipe_ind].height),
                                      abs(bird.y - game.pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        for x, bird in enumerate(birds):
            if game.check_collisions(bird):
                ge[x].fitness -= 1
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        if game.pipe_passed(birds[0]):
            for g in ge:
                g.fitness += 5

        game.update()                   # Move all the other pieces
        game.draw(birds)                     # Draw all the pieces



def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,20)




if __name__ == "__main__":
    config_path = os.path.join(base_path, "config-feedforward.txt")
    run(config_path)