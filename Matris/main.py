import matris
import learning
import pygame

pygame.init()
matris.screen = pygame.display.set_mode((matris.WIDTH, matris.HEIGHT))
pygame.display.set_caption("MaTris")
session = matris.Game()
session.main(matris.screen)
print("test")

while True:
	print(session.requestupdate())
