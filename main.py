# Example file showing a basic pygame "game loop"
import pygame
import random
from threading import Timer

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0.05

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

circles = []

def circle_position():
	circles.append(pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height())))
	add_circles = Timer(1.0, circle_position)
	add_circles.start()

add_circles = Timer(1.0, circle_position)
add_circles.start()

while running:
	# poll for events
	# pygame.QUIT event means the user clicked X to close your window
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# fill the screen with a color to wipe away anything from last frame
	screen.fill("purple")

	# RENDER YOUR GAME HERE
	pygame.draw.circle(screen, "red", player_pos, 40)

	# Render existing green circles
	for circle in circles:
		pygame.draw.circle(screen, "green", circle, 40)

	# arrow keys move circle
	keys = pygame.key.get_pressed()
	if keys[pygame.K_w]:
		player_pos.y -= 300 * dt
	if keys[pygame.K_s]:
		player_pos.y += 300 * dt
	if keys[pygame.K_a]:
		player_pos.x -= 300 * dt
	if keys[pygame.K_d]:
		player_pos.x += 300 * dt

	# loop circle from edges of screen
	if player_pos.y <= -40:
		player_pos.y = screen.get_height() + 30
	if player_pos.y >= 40 + screen.get_height():
		player_pos.y = -30
	if player_pos.x <= -40:
		player_pos.x = screen.get_width() + 30
	if player_pos.x >= 40 + screen.get_width():
		player_pos.x = -30

	# flip() the display to put your work on screen
	pygame.display.flip()

	clock.tick(60)  # limits FPS to 60

pygame.quit()