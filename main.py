import os
from pprint import pprint

import pygame
import requests

coords = ['49.106822', '55.795464']
speed = 0.005
map_types = ['map', 'sat', 'sat,skl']
scale = 5
map_api_server = "http://static-maps.yandex.ru/1.x/"
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((500, 750))
type_count = 0
map_type = 'map'
first_coord = coords


def text_writter(x, y, text):
    font = pygame.font.Font(None, 32)
    text = font.render(text, True, 'GREEN')
    screen.blit(text, (x, y))


if __name__ == '__main__':
    screen.fill((27, 27, 27), rect=(0, 450, 500, 650))
    searchname_rect = pygame.Rect(295, 530, 100, 30)
    reset_rect = pygame.Rect(105, 530, 100, 30)
    name_rect = pygame.Rect(20, 480, 460, 35)
    active = False
    flag = False
    base_font = pygame.font.Font(None, 28)
    address_font = pygame.font.Font(None, 20)
    search_text = ''
    lon = coords[0]
    lat = coords[1]
    reset_check = False
    running = True
    address = ''
    index = ''
    index_flag = True
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
                elif event.key == pygame.K_LSHIFT:
                    index_flag = False if index_flag else True

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
        pygame.draw.rect(screen, (96, 96, 96), reset_rect)
        pygame.draw.rect(screen, (96, 96, 96), name_rect)

        text_surface = base_font.render(search_text, True, (250, 250, 250))
        screen.blit(text_surface, (name_rect.x, name_rect.y))
        text_surface = pygame.font.Font(None, 18).render('Адрес:', True, (245, 245, 245))
        screen.blit(text_surface, (name_rect.x, 570))
        text_surface = address_font.render(address, True, (245, 0, 0))
        screen.blit(text_surface, ((name_rect.x, 590)))
        search_surface = base_font.render('Найти', True, (250, 250, 250))
        screen.blit(search_surface, (searchname_rect.x + 5, searchname_rect.y + 5))
        reset_surface = base_font.render('Сброс', True, (250, 250, 250))
        screen.blit(reset_surface, (reset_rect.x + 5, reset_rect.y + 5))

        if index_flag:

            text_surface = pygame.font.Font(None, 18).render('Индекс(вкл)', True, (245, 250, 250))
            screen.blit(text_surface, (name_rect.x, 620))
            text_surface = pygame.font.Font(None, 20).render(index, True, (245, 0, 0))
            screen.blit(text_surface, (name_rect.x, 640))
        else:
            text_surface = pygame.font.Font(None, 18).render('Индекс(выкл)', True, (245, 250, 250))
            screen.blit(text_surface, (name_rect.x, 620))

        if reset_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1:
            reset_check = True
            address = ''

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
                reset_check = False
                toponym = json_response["response"]["GeoObjectCollection"][
                    "featureMember"][0]["GeoObject"]
                address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
                pprint(json_response)
                try:
                    index = \
                        toponym["metaDataProperty"]["GeocoderMetaData"]['AddressDetails']['Country'][
                            'AdministrativeArea'][
                            'Locality']['Thoroughfare']['Premise']['PostalCode']['PostalCodeNumber']
                except Exception:
                    index = 'Индекс не найден!'
                if len(address) > 56:
                    address_font = pygame.font.Font(None, 14)
                if len(address) > 80:
                    address_font = pygame.font.Font(None, 12)
                toponym_coodrinates = toponym["Point"]["pos"]
                lon, lat = toponym_coodrinates.split(" ")
                coords = [lon, lat]
                first_coord = coords

            except IndexError:
                print('Неожиданная ошибка')

        coords = [lon, lat]
        zoom = str(scale)
        pwtm = None
        if not reset_check:
            pwtm = ','.join([first_coord[0], first_coord[1], 'pmwtm'])

        map_api_params = {
            "z": zoom,
            "ll": ",".join(coords),
            "l": map_type,
            "pt": pwtm
        }
        response = requests.get(map_api_server, params=map_api_params)

        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
        clock.tick(160)
    os.remove(map_file)
