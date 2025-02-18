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

		self.image = pygame.Surface([width, width], pygame.SRCALPHA)

		pygame.draw.circle(self.image, color, (width / 2, width / 2), width / 2)

		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = coord
		self.radius = width / 2

player = pygame.sprite.Group()
green_circles = pygame.sprite.Group()
blue_circles = pygame.sprite.Group()

# initialize player circle
player_start = Circle("red", 40, player_pos)
player.add(player_start)

# Adds a circle of a color over an interval
def circle_position(color, interval, group):
	while True:
		coords = pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
		circle = Circle(color, 40, coords)
		group.add(circle)
		time.sleep(interval)

# Adds a green circle every second
add_green_circles = Thread(target=circle_position, args=('green', 1, green_circles))
add_green_circles.start()

# Adds a blue circle every 5 seconds
add_blue_circles = Thread(target=circle_position, args=('blue', 5, blue_circles))
add_blue_circles.start()

while running:
	# poll for events
	# pygame.QUIT event means the user clicked X to close your window
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# fill the screen with a color to wipe away anything from last frame
	screen.fill(background)

	# render sprites
	player.update()
	player.draw(screen)
	green_circles.update()
	green_circles.draw(screen)
	blue_circles.update()
	blue_circles.draw(screen)

	keys = pygame.key.get_pressed()

	for sprite in player.sprites():
		# arrow keys move circle
		if keys[pygame.K_w]:
			sprite.rect.y -= 300 * dt
		if keys[pygame.K_s]:
			sprite.rect.y += 300 * dt
		if keys[pygame.K_a]:
			sprite.rect.x -= 300 * dt
		if keys[pygame.K_d]:
			sprite.rect.x += 300 * dt

		# loop circle from edges of screen
		if sprite.rect.y <= -40:
			sprite.rect.y = screen.get_height() + 30
		if sprite.rect.y >= 40 + screen.get_height():
			sprite.rect.y = -30
		if sprite.rect.x <= -40:
			sprite.rect.x = screen.get_width() + 30
		if sprite.rect.x >= 40 + screen.get_width():
			sprite.rect.x = -30

		# check contact with green circles and turn red
		for circle in green_circles.sprites():
			if pygame.sprite.collide_circle(sprite, circle):
				player.add(Circle("red", 40, (circle.rect.x, circle.rect.y)))
				circle.kill()
		
		# check contact with blue circles and turn red circles blue
		for circle in blue_circles.sprites():
			if pygame.sprite.collide_circle(sprite, circle):
				blue_circles.add(Circle("blue", 40, (sprite.rect.x, sprite.rect.y)))
				sprite.kill()
				

	# flip() the display to put your work on screen
	pygame.display.flip()

	clock.tick(60)  # limits FPS to 60

pygame.quit()