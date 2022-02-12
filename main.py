import os

import pygame
import requests

coords = ['49.106822', '55.795464']
speed = 0.005
map_types = ['map', 'sat', 'sat,skl']
scale = 5
map_api_server = "http://static-maps.yandex.ru/1.x/"
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((500, 600))
type_count = 0
map_type = 'map'


def text_writter(x, y, text):
    font = pygame.font.Font(None, 32)
    text = font.render(text, True, 'GREEN')
    screen.blit(text, (x, y))


if __name__ == '__main__':
    screen.fill((27, 27, 27), rect=(0, 450, 500, 650))
    searchname_rect = pygame.Rect(195, 530, 100, 30)
    name_rect = pygame.Rect(20, 480, 460, 35)
    active = False
    flag = False
    base_font = pygame.font.Font(None, 28)
    search_text = ''
    lon = coords[0]
    lat = coords[1]
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if name_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    active = True
                    search_text = search_text[:-1]
                else:
                    if active:
                        search_text += event.unicode
                if event.key == pygame.K_PAGEUP:
                    if scale + 1 <= 19:
                        scale += 1
                elif event.key == pygame.K_TAB:
                    type_count += 1
                    map_type = map_types[type_count % 3]

                elif event.key == pygame.K_PAGEDOWN:
                    if scale - 1 >= 2:
                        scale -= 1
                elif event.key == pygame.K_UP and float(coords[1]) < 85:
                    lat = str(float(lat) + speed)
                elif event.key == pygame.K_DOWN and float(coords[1]) > -85:
                    lat = str(float(lat) - speed)
                elif event.key == pygame.K_LEFT and float(coords[0]) < 180:
                    lon = str(float(lon) - speed)
                elif event.key == pygame.K_RIGHT and float(coords[0]) > -180:
                    lon = str(float(lon) + speed)
        screen.fill((27, 27, 27), rect=(0, 450, 500, 650))
        pygame.draw.rect(screen, (96, 96, 96), searchname_rect)
        pygame.draw.rect(screen, (96, 96, 96), name_rect)

        text_surface = base_font.render(search_text, True, (250, 250, 250))
        screen.blit(text_surface, (name_rect.x, name_rect.y))
        search_surface = base_font.render('Найти', True, (250, 250, 250))
        screen.blit(search_surface, (searchname_rect.x + 5, searchname_rect.y + 5))

        if search_text and searchname_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1:
            toponym_to_find = search_text

            geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

            geocoder_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": toponym_to_find,
                "format": "json"}

            response = requests.get(geocoder_api_server, params=geocoder_params)

            if not response:
                pass

            json_response = response.json()
            try:
                toponym = json_response["response"]["GeoObjectCollection"][
                    "featureMember"][0]["GeoObject"]
                toponym_coodrinates = toponym["Point"]["pos"]
                lon, lat = toponym_coodrinates.split(" ")
                coords = [lon, lat]
            except IndexError:
                print('Неожиданная ошибка')

        coords = [lon, lat]
        zoom = str(scale)

        map_api_params = {
            "z": zoom,
            "ll": ",".join(coords),
            "l": map_type,
            "pt": ','.join([coords[0], coords[1], 'pmwtm'])
        }
        response = requests.get(map_api_server, params=map_api_params)
        if not response:
            pass

        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
        clock.tick(160)
    os.remove(map_file)
