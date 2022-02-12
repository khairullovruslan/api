import os
import pygame
import requests

coords = ['49.106822', '55.795464']
zoom = 10
map_api_server = "http://static-maps.yandex.ru/1.x/"

map_api_params = {
    "ll": ",".join(coords),
    "z": str(zoom),
    "l": "map"
}
response = requests.get(map_api_server, params=map_api_params)
if not response:
    pass

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((500, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    response = requests.get(map_api_server, params=map_api_params)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()

os.remove(map_file)
