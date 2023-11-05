# Snake Game


# Imports
import pygame
from pygame.locals import *
import time
import random
import xml.etree.ElementTree as ET

# Initial variables
speed = 0.2
direction = 'right'
start = False
text_colour = 227, 47, 34


# Apple
class Apple:
    # Building initial Apple
    def __init__(self, screen):
        self.screen = screen

        # Apple image
        self.apple = pygame.image.load("game_resources/apple.jpg ").convert()

        # Apple starting position
        self.x = 240
        self.y = 240

    # Moving apple to random location on collision
    def move(self):
        self.x = random.randint(0, 14) * block_size
        self.y = random.randint(0, 14) * block_size

    # Placing objects
    def draw(self):
        # Placing Apple
        self.screen.blit(self.apple, (self.x, self.y))

        # Placing objects
        pygame.display.flip()


# Snake
block_size = 40


class Snake:
    # Building initial Snake
    def __init__(self, screen, length):
        global start

        self.screen = screen

        # Snake Block image
        self.block = pygame.image.load("game_resources/block.jpg").convert()

        # Starting direction
        self.direction = direction

        # Building snake
        self.length = length
        if start is False:
            self.x = [120, 120, 120, 120]
            self.y = [240, 240, 240, 240]
            start = True
        else:
            self.x = [block_size] * length
            self.y = [block_size] * length

    # Increase Snake length
    def increase_length(self):
        global speed

        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

        # increase speed
        speed = speed - 0.01

    # Snake movement

    # Move up direction
    def move_up(self):
        self.direction = "up"
        self.draw()

    # Move down direction
    def move_down(self):
        self.direction = "down"
        self.draw()

    # Move left direction
    def move_left(self):
        self.direction = "left"
        self.draw()

    # Move right direction
    def move_right(self):
        self.direction = "right"
        self.draw()

    # Continuous movement
    def movement(self):
        # Following blocks
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # Moving up function
        if self.direction == "up":
            self.y[0] -= block_size

        # Moving down function
        if self.direction == "down":
            self.y[0] += block_size

        # Moving left function
        if self.direction == "left":
            self.x[0] -= block_size

        # Moving right function
        if self.direction == "right":
            self.x[0] += block_size

        # Calling initial Snake position method
        self.draw()

    # Placing objects
    def draw(self):
        # Placing initial Snake
        for i in range(self.length):
            self.screen.blit(self.block, (self.x[i], self.y[i]))

        # Placing objects
        pygame.display.flip()


class Game:
    def __init__(self):
        # Loading modules

        # Pygame
        pygame.init()

        # Pygame sound module
        pygame.mixer.init()

        # Call background music method
        self.background_music()

        # Initialising surface

        # Screen size
        self.surface = pygame.display.set_mode((600, 600))

        # Placing Snake
        self.snake = Snake(self.surface, 4)  # Snake length
        self.snake.draw()

        # Placing Apple
        self.apple = Apple(self.surface)
        self.apple.draw()

    # Sounds

    # Background music
    def background_music(self):
        pygame.mixer.music.load("game_resources/snake_game_music.mp3")
        pygame.mixer.music.play(-1)

    # Collision sounds
    def collision_sounds(self, sound):
        # Loading sound
        sound = pygame.mixer.Sound(f"game_resources/{sound}.mp3")

        # Playing sound
        pygame.mixer.Sound.play(sound)

    # Rendering background image
    def render_background(self):
        background = pygame.image.load("game_resources/background.jpg")
        self.surface.blit(background, (0, 0))

    # Game functionality
    def play(self):

        # Load background image
        self.render_background()

        # Loading in Snake movement functionality
        self.snake.movement()

        # Loading in Apple functionality
        self.apple.draw()

        pygame.display.flip()

        # Collisions

        # Collision with Apple actions
        if self.snake.x[0] == self.apple.x and self.snake.y[0] == self.apple.y: # snake.x[0] and snake.y[0] is the head of the snake

            # Calling sound method for ding
            self.collision_sounds("apple_crunch")

            # Calling increase Snake length method
            self.snake.increase_length()

            # Calling Apple move method
            self.apple.move()

        # Collision with Snake body
        for i in range(2, self.snake.length):  # If snake head hits block 2 or more
            if self.snake.x[0] == self.snake.x[i] and self.snake.y[0] == self.snake.y[i]:
                # Calling sound method for crash
                self.collision_sounds("death")

                # Raising a game over
                raise "Game Over"

        # Collision with screen limit
        if self.snake.x[0] > 600 or self.snake.x[0] < 0 or self.snake.y[0] > 600 or self.snake.y[0] < 0:
            self.collision_sounds("death")

            # Raising a game over
            raise "Game Over"

    # Game over
    def game_over(self):
        # Wipe screen
        self.render_background()

        # Print game over message

        # Font and size
        game_over_font = pygame.font.SysFont('arial', 50)
        font = pygame.font.SysFont('arial', 25)

        # Building messages
        game_over_message = game_over_font.render("GAME OVER!", True, text_colour)
        score_message = font.render(f"Score: {self.snake.length-4}", True, text_colour)
        play_again = font.render("Press Enter to play again or press Esc to exit!", True, text_colour)

        # Placing messages
        self.surface.blit(game_over_message, (170, 250))
        self.surface.blit(score_message, (260, 350))
        self.surface.blit(play_again, (100, 400))
        pygame.display.flip()

        # Pausing background music
        pygame.mixer.music.pause()

    # Reset game
    def reset(self):
        global speed
        global direction
        global start

        # Read username from temp file
        file = open("temp.txt", "r")
        username = file.read()

        tree = ET.parse("Data.xml")
        root = tree.getroot()

        # Write new high score to xml file
        for user in root:
            if user.text == username:
                high_score = user.find('Score')
                score = self.snake.length - 4
                if score > int(high_score.text):
                    high_score.text = str(score)
                    tree.write('Data.xml')

        # Reset Speed
        speed = 0.2

        # Reset Direction
        direction = 'right'

        # Reset Snake position
        start = False

        # Reset Snake
        self.snake = Snake(self.surface, 4)  # Snake length

        # Reset Apple
        self.apple = Apple(self.surface)

    # Run
    def run(self):
        global speed
        global direction

        running = True
        pause = False

        while running:
            # When key is pressed
            for event in pygame.event.get():
                if event.type == KEYDOWN:

                    # Quit game through ESC key
                    if event.key == K_ESCAPE:
                        running = False

                    # Unpause game events
                    if event.key == K_RETURN:
                        pause = False

                        # Play music
                        pygame.mixer.music.unpause()

                    # Keys when running
                    if not pause:

                        # Move up
                        if event.key == K_UP and direction != 'down':
                            direction = 'up'
                            self.snake.move_up()

                        # Move down
                        if event.key == K_DOWN and direction != 'up':
                            direction = 'down'
                            self.snake.move_down()

                        # Move left
                        if event.key == K_LEFT and direction != 'right':
                            direction = 'left'
                            self.snake.move_left()

                        # Move right
                        if event.key == K_RIGHT and direction != 'left':
                            direction = 'right'
                            self.snake.move_right()

                # Quit game through closing
                elif event.type == QUIT:
                    running = False

            # Load in game
            try:
                if not pause:
                    self.play()

            # Game over event
            except:
                # Calling Game Over method
                self.game_over()

                # Pause game
                pause = True

                # Calling Reset game method
                self.reset()

            # Maximum speed
            if speed <= 0.01:
                speed = 0.01

            # Screen refresh speed
            time.sleep(speed)


# Start
game = Game()
game.run()
