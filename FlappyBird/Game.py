"""
The main game class for the flappy bird game. Stores all the game logic and functionality
"""

import pygame
from FlappyBird.Constants import bg_img
from FlappyBird.Base import Base
from FlappyBird.Pipe import Pipe
from FlappyBird.Constants import WIN_WIDTH, WIN_HEIGHT, FPS, BLACK, mediumFont, largeFont, file_path

class Game:
    def __init__(self, win):
        """
        Class holds the main game functionality for full game

        Arguments:
            win {surface} -- The surface everything will be drawn on to
        """
        self.win = win
        self.reset()

    def reset(self):
        """
        Method sets or resets all the class information to reset the game
        """
        self.bg_img = bg_img
        self.base = Base(self.win)
        self.pipes = []
        self.pipes.append(Pipe(self.win))
        self.tick_count = 0
        self.score = 0

    def add_pipes(self):
        """
        Method adds pipes every 80 frames
        """
        self.tick_count += 1

        if self.tick_count == 70:
            self.pipes.append(Pipe(self.win))
            self.tick_count = 0

    def pipe_passed(self, bird):
        """
        Adds one to the score if the pipe has been passed
        """
        if not self.pipes[0].passed and bird.x > self.pipes[0].right():
            self.score += 1
            self.pipes[0].passed = True
            return True

        return False


    def update(self):
        """
        Method moves all pipes, bird and base
        """
        if self.pipes[0].off_screen():
            self.pipes.pop(0)

        self.base.move()

        self.add_pipes()
        for pipe in self.pipes:
            pipe.move()

    def check_collisions(self, bird):
        """
        Method checks if collision between bird and base, ceiling or pipes
        """
        return bird.y < 0 or bird.collide(self.pipes[0], self.base)


    def draw(self, birds, gen, alive):
        """
        Method draws the bird, base, pipes and score to the screen
        """
        self.win.blit(self.bg_img, (0,0))

        for bird in birds:
            bird.draw()

        for pipe in self.pipes:
            pipe.draw()

        self.base.draw()

        score_text = largeFont.render("Score: " + str(self.score), True, BLACK)
        gen_text = mediumFont.render("Gen: " + str(gen), True, BLACK)
        alive_text = mediumFont.render("Alive: " + str(alive), True, BLACK)
        self.win.blit(score_text, (10,10))
        self.win.blit(gen_text, (10, 50))
        self.win.blit(alive_text, (10, 70))


        pygame.display.update()
