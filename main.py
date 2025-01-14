# Example file showing a basic pygame "game loop"
import pygame
import random
from threading import Thread
import time

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0.05

background = 'purple'

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

class Circle(pygame.sprite.Sprite):
	def __init__(self, color, width, coord):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface([width, width])
		self.image.fill(background)
		self.image.set_colorkey(background)

		pygame.draw.circle(self.image, color, (width / 2, width / 2), width / 2)

		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = coord

sprites = pygame.sprite.Group()

# initialize player circle
player = Circle("red", 40, player_pos)
sprites.add(player)

# Adds a green circle every second
def circle_position():
	while True:
		coords = pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
		green_circle = Circle("green", 40, coords)
		sprites.add(green_circle)
		time.sleep(1)

add_circles = Thread(target=circle_position)
add_circles.start()

while running:
	# poll for events
	# pygame.QUIT event means the user clicked X to close your window
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# fill the screen with a color to wipe away anything from last frame
	screen.fill(background)

	# render sprites
	sprites.update()
	sprites.draw(screen)

	# arrow keys move circle
	keys = pygame.key.get_pressed()
	if keys[pygame.K_w]:
		player.rect.y -= 300 * dt
	if keys[pygame.K_s]:
		player.rect.y += 300 * dt
	if keys[pygame.K_a]:
		player.rect.x -= 300 * dt
	if keys[pygame.K_d]:
		player.rect.x += 300 * dt

	# loop circle from edges of screen
	if player.rect.y <= -40:
		player.rect.y = screen.get_height() + 30
	if player.rect.y >= 40 + screen.get_height():
		player.rect.y = -30
	if player.rect.x <= -40:
		player.rect.x = screen.get_width() + 30
	if player.rect.x >= 40 + screen.get_width():
		player.rect.x = -30

	# flip() the display to put your work on screen
	pygame.display.flip()

	clock.tick(60)  # limits FPS to 60

pygame.quit()