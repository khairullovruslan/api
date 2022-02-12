import os

import pygame
import requests

coords = ['49.106822', '55.795464']
zoom = 10
map_types = ['map', 'sat', 'sat,skl']

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
speed = 0.05
screen.blit(pygame.image.load(map_file), (0, 0))
scale = 5
lon = coords[0]
lat = coords[1]
map_type = 'map'
type_count = 0
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if scale + 1 <= 19:
                    scale += 1
            if event.key == pygame.K_PAGEDOWN:
                if scale - 1 >= 2:
                    scale -= 1
            if event.key == pygame.K_UP and float(coords[1]) < 85:
                lat = str(float(lat) + speed)
            if event.key == pygame.K_DOWN and float(coords[1]) > -85:
                lat = str(float(lat) - speed)
            if event.key == pygame.K_LEFT and float(coords[0]) < 180:
                lon = str(float(lon) - speed)
            if event.key == pygame.K_RIGHT and float(coords[0]) > -180:
                lon = str(float(lon) + speed)
            if event.key == pygame.K_TAB:
                type_count += 1
                map_type = map_types[type_count % 3]

    zoom = str(scale)
    coords = [lon, lat]
    map_api_params = {
        "ll": ",".join(coords),
        "z": zoom,
        "l": map_type
    }
    response = requests.get(map_api_server, params=map_api_params)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
os.remove(map_file)
