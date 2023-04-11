import sys

import pygame
from human import Human
from wolf import Wolf
from sheep import Sheep
from Fox import Fox
from turtle import Turtle
from antelope import Antelope
from cybersheep import Cybersheep
from grass import Grass
from sowthistle import Sowthistle
from guarana import Guarana
from belladonna import Belladonna
from hogweed import Hogweed

RED = (200, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SQUARE_SIZE = 50


class World:
    def __init__(self, window_size, map_x, map_y):
        pygame.init()
        self._my_font = pygame.font.SysFont('Arial', 20)
        self._font_organisms = pygame.font.SysFont('Arial', 25)
        self._window_size = window_size
        self._window_x = window_size[0]
        self._window_y = window_size[1]
        self._map_x = map_x
        self._map_y = map_y
        self._textbox_surface = pygame.Surface((500, 250))
        self._board_surface = pygame.Surface((500, 500))
        self._content_surface = pygame.Surface(self._window_size)
        self._screen = pygame.display.set_mode(self._window_size)
        self._menu_surface = pygame.Surface((500, 50))
        self.organisms = []
        self.animals_classes = {'Wolf': Wolf, 'Sheep': Sheep, 'Fox': Fox, 'Turtle': Turtle, 'Antelope': Antelope, 'Cybersheep': Cybersheep, 'Human': Human}
        self.plants_classes = {'Grass': Grass, 'Sowthistle': Sowthistle, 'Guarana': Guarana, 'Belladonna': Belladonna, 'Hogweed': Hogweed}
        self._were_organisms_added = False
        self._is_hogweed_on_map = False
        self.is_special_ability_used = False
        self.special_ability_cooldown = 0
        self.original_strength = 0
        self.new_organism_coordinates = None
        self.was_mouse_pressed = False
        self.is_human_alive = True
        self.animals_textboxes_dict = {}
        self.plants_textboxes_dict = {}
        self.logs = []
        self.loaded_data_from_file = []

        self.human = None
        self.game()

    def get_is_hogweed_on_map(self):
        return self._is_hogweed_on_map

    def get_font(self):
        return self._my_font

    def get_map_x(self):
        return self._map_x

    def get_map_y(self):
        return self._map_y
    #
    # def get_organisms_classes(self):
    #     return self.get_organisms_classes()

    def sort_organisms(self):
        self.organisms.sort(key=lambda o: (o.initiative, o.age), reverse=True)
        for org in self.organisms:
            org.was_organism_just_added = False

    def init_organisms(self):
        self.human = Human(0, 1, 8, self)
        self.organisms.append(self.human)
        self.organisms.append(Wolf(0, 4, 8, self))
        self.organisms.append(Wolf(0, 6, 8, self))
        self.organisms.append(Antelope(0, 3, 2, self))
        self.organisms.append(Antelope(0, 1, 2, self))
        self.organisms.append(Fox(0, 7, 2, self))
        self.organisms.append(Fox(0, 5, 2, self))
        self.organisms.append(Turtle(0, 3, 7, self))
        self.organisms.append(Turtle(0, 5, 7, self))
        self.organisms.append(Cybersheep(0, 0, 0, self))

        self.organisms.append(Grass(0, 9, 9, self))
        self.organisms.append(Sowthistle(0, 2, 9, self))
        self.organisms.append(Guarana(0, 2, 7, self))
        self.organisms.append(Belladonna(0, 5, 5, self))
        self.organisms.append(Belladonna(0, 4, 5, self))
        self.organisms.append(Hogweed(0, 8, 1, self))
        self.organisms.append(Hogweed(0, 8, 8, self))

        self.sort_organisms()

    def init_board(self):
        pygame.display.set_caption("Project 3")
        self._textbox_surface.fill(BLACK)
        self._menu_surface.fill(BLACK)
        self.restart_board()

        for x in range(4):
            if x != 0:
                pygame.draw.line(self._menu_surface, RED, (x * 125, 0), (x * 125, 800), 3)

        self._content_surface.blit(self._board_surface, (0, 0))
        self._content_surface.blit(self._textbox_surface, (0, 500))
        self._content_surface.blit(self._menu_surface, (0, 750))
        self._screen.blit(self._content_surface, (0, 0))

    def add_text(self, x, y, text, text_color):
        h = self._font_organisms.render(text, True, text_color, RED).get_height()
        w = self._font_organisms.render(text, True, text_color, RED).get_width()
        if text in self.animals_classes:
            self.animals_textboxes_dict.update({text: (w, h)})
        elif text in self.plants_classes:
            self.plants_textboxes_dict.update({text: (w, h)})

        self._screen.blit(self._font_organisms.render(text, True, BLACK, RED), (x, y))
        pygame.display.update()

    def open_organism_menu(self, x, y):
        if (0 <= x < self._map_x) and (0 <= y < self._map_y):
            if self.get_organism_at_coordinates(x, y) is None:
                text_x = 10
                text_y = 510
                self._textbox_surface.fill(BLACK)
                self.update_board()
                for a in self.animals_classes:
                    if a is not 'Human':
                        self.add_text(text_x, text_y, a, BLACK)
                        text_y += 40

                self.add_text(120, 520, "Choose organism to add!", BLACK)
                self.add_text(200, 600, "x:" + str(x) + " " + "y:" + str(y), BLACK)
                self.add_text(200, 700, 'Human', BLACK)
                self.new_organism_coordinates = (x, y)
                text_x = 380
                text_y = 510
                for p in self.plants_classes:
                    self.add_text(text_x, text_y, p, BLACK)
                    text_y += 40

    def check_if_hogweed_is_on_map(self):
        self._is_hogweed_on_map = any(isinstance(x, Hogweed) for x in self.organisms)

    def get_organism_at_coordinates(self, x, y):
        for o in self.organisms:
            if o.pos_x == x and o.pos_y == y:
                return o

        return None

    def add_organism(self, organism):
        organism.was_organism_just_added = True
        self._were_organisms_added = True
        self.organisms.append(organism)

    def restart_board(self):
        self._board_surface.fill(BLACK)
        for x in range(self._map_x):
            pygame.draw.line(self._board_surface, RED, (x * SQUARE_SIZE, 0), (x * SQUARE_SIZE, 500), 2)
        for y in range(self._map_y):
            pygame.draw.line(self._board_surface, RED, (0, y * (500 // self._map_y)), (500, y * (500 // self._map_y)), 2)

    def update_board(self):
        self.restart_board()
        for x in range(self._map_x):
            pygame.draw.line(self._board_surface, RED, (x * SQUARE_SIZE, 0), (x * SQUARE_SIZE, 500), 2)

        for y in range(self._map_y):
            for x in range(self._map_x):
                organism = self.get_organism_at_coordinates(x, y)
                if organism is not None:
                    self._board_surface.blit(organism.get_text(), (x * SQUARE_SIZE + 20, y * SQUARE_SIZE + 15))

        self._content_surface.blit(self._board_surface, (0, 0))
        self._content_surface.blit(self._textbox_surface, (0, 500))
        self._content_surface.blit(self._menu_surface, (0, 750))
        self._screen.blit(self._content_surface, (0, 0))
        self.add_text(25, 755, "START", WHITE)
        self.add_text(160, 755, "SAVE", WHITE)
        self.add_text(290, 755, "LOAD", WHITE)
        self.add_text(410, 755, "EXIT", WHITE)
        pygame.display.update()

    def print_logs(self):
        log_x = 0
        log_y = 500
        for l in self.logs:
            self.add_text(log_x, log_y, l, BLACK)
            log_y += 30

    def make_turn(self):
        self.check_if_hogweed_is_on_map()
        for o in self.organisms:
            if o.was_organism_just_added is False:
                o.action()
                o.age += 1

        if self.special_ability_cooldown > 0:
            self.special_ability_cooldown -= 1

        if self.is_special_ability_used:
            self.human.strength -= 1
            if self.human.strength == self.original_strength:
                self.is_special_ability_used = False
                self.special_ability_cooldown = 5
                self.human.strength = self.original_strength
            self.logs.append("Human's strength in next turn: " + str(self.human.strength) + "")
            info = self.human.strength - self.original_strength
            self.logs.append("The effect will last for " + str(info) + " more turns...")

        self.update_board()
        self.print_logs()
        self.logs.clear()

    def check_if_human_is_alive(self):
        if any(isinstance(o, Human) for o in self.organisms):
            return True
        else:
            return False

    def add_organism_by_mouse(self, mouse_x, mouse_y):
        count = 0
        key_list_animals = list(self.animals_textboxes_dict.keys())
        key_list_plants = list(self.plants_textboxes_dict.keys())
        organism_name = None
        if_add_plant = False
        if_add_animal = False

        if (10 <= mouse_x <= 120) and (510 <= mouse_y <= 750):
            for a in self.animals_textboxes_dict.values():
                if (10 <= mouse_x <= a[0] + 10) and (40 * count + 510 <= mouse_y <= 40 * count + 510 + a[1]):
                    organism_name = key_list_animals[count]
                    if_add_animal = True
                    break
                count += 1
        elif (380 <= mouse_x <= 480) and (510 <= mouse_y <= 750):
            for p in self.plants_textboxes_dict.values():
                if (380 <= mouse_x <= p[0] + 380) and (40 * count + 510 <= mouse_y <= 40 * count + 510 + p[1]):
                    organism_name = key_list_plants[count]
                    if_add_plant = True
                    break
                count += 1
        elif (200 <= mouse_x <= 265) and (700 <= mouse_y <= 730):
            if self.check_if_human_is_alive() is False:
                self.human = Human(0, self.new_organism_coordinates[0], self.new_organism_coordinates[1], self)
                self.add_organism(self.human)
                self.sort_organisms()
                self.logs.append("Added Human " + " at " + str(self.new_organism_coordinates[0]) + " " + str(self.new_organism_coordinates[1]))
                self.update_board()
            else:
                self.logs.append("You can't have 2 humans in one game!")

        if if_add_plant is True or if_add_animal is True:
            if if_add_animal is True:
                self.add_organism(self.animals_classes[organism_name](0, self.new_organism_coordinates[0],
                                                                       self.new_organism_coordinates[1], self))
            else:
                self.add_organism(self.plants_classes[organism_name](0, self.new_organism_coordinates[0],
                                                                      self.new_organism_coordinates[1], self))

            self.logs.append("Added " + organism_name + " at " + str(self.new_organism_coordinates[0]) + " " + str(self.new_organism_coordinates[1]))
            self.sort_organisms()
            self.update_board()

    def load_game_from_file(self):
        file = open('C:\\Users\\jdzie\\Desktop\\docs\\university\\2nd semester\\oop\\aaaa\\saves\\save1', 'r')
        for line in file:
            self.loaded_data_from_file.append(line[0:-1])
        file.close()

        self.organisms.clear()
        for i in range(len(self.loaded_data_from_file) - 1):
            org_name = self.loaded_data_from_file[i].split()[0]
            org_age = int(self.loaded_data_from_file[i].split()[1])
            org_x = int(self.loaded_data_from_file[i].split()[2])
            org_y = int(self.loaded_data_from_file[i].split()[3])

            if org_name in self.animals_classes:
                if org_name == 'Human':
                    self.human = None
                    self.human = self.animals_classes[org_name](org_age, org_x, org_y, self)
                    self.add_organism(self.human)
                    continue
                self.add_organism(self.animals_classes[org_name](org_age, org_x, org_y, self))
            elif org_name in self.plants_classes:
                self.add_organism(self.plants_classes[org_name](org_age, org_x, org_y, self))

        if self.loaded_data_from_file[-1].split()[0] == 'False':
            self.is_special_ability_used = False
            self.special_ability_cooldown = int(self.loaded_data_from_file[-1].split()[1])
        elif self.loaded_data_from_file[-1].split()[0] == 'True':
            self.is_special_ability_used = True
            self.special_ability_cooldown = int(self.loaded_data_from_file[-1].split()[1])
            self.original_strength = int(self.loaded_data_from_file[-1].split()[2])
            self.human.strength = int(self.loaded_data_from_file[-1].split()[3])

        self.sort_organisms()
        self.make_turn()

    def save_to_file(self):
        with open('saves/save1', 'w') as file:
            for i in self.organisms:
                file.write(i.get_name() + " " + str(i.age) + " " + str(i.pos_x) + " " + str(i.pos_y) + '\n')
            file.write(str(self.is_special_ability_used) + " " + str(self.special_ability_cooldown) + " " + str(self.original_strength) + " " + str(self.human.strength) + '\n')

    def game(self):
        running = True
        self.init_organisms()
        self.init_board()
        self.update_board()
        while running:
            pygame.event.wait()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.human.set_move_next_for_turn(self.human.pos_x - 1, self.human.pos_y)
                self.make_turn()
            elif keys[pygame.K_RIGHT]:
                self.human.set_move_next_for_turn(self.human.pos_x + 1, self.human.pos_y)
                self.make_turn()
            elif keys[pygame.K_UP]:
                self.human.set_move_next_for_turn(self.human.pos_x, self.human.pos_y - 1)
                self.make_turn()
            elif keys[pygame.K_DOWN]:
                self.human.set_move_next_for_turn(self.human.pos_x, self.human.pos_y + 1)
                self.make_turn()
            elif keys[pygame.K_ESCAPE]:
                running = False
            elif keys[pygame.K_LCTRL]:
                if self.human.strength >= 10:
                    self.logs.append("Human's strength is bigger than 10, using magical potion will decrease it!")
                else:
                    if self.special_ability_cooldown == 0:
                        self.human.magical_potion()
                        self.logs.append("SPECIAL ABILITY WAS USED!!!!")
                        self.logs.append(self.human.get_name() + " strength is " + str(self.human.strength) + " now!")
                    else:
                        self.logs.append("Special ability is on cooldown for " + str(self.special_ability_cooldown) + " more turns")
            elif pygame.mouse.get_pressed()[0]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                x = mouse_x // SQUARE_SIZE
                y = mouse_y // SQUARE_SIZE
                self.open_organism_menu(x, y)
                if (0 <= mouse_x <= 500) and (500 <= mouse_y <= 750):
                    self.add_organism_by_mouse(mouse_x, mouse_y)
                if (0 <= mouse_x <= 500) and (750 <= mouse_y <= 800):
                    if 0 <= mouse_x < 125:
                        print("start")
                    elif 125 <= mouse_x < 250:
                        self.save_to_file()
                    elif 250 <= mouse_x < 375:
                        self.load_game_from_file()
                    elif 375 <= mouse_x < 500:
                        running = False

            if self._were_organisms_added:
                self.sort_organisms()
                self._were_organisms_added = False

            if self.check_if_human_is_alive() is False:
                self.is_human_alive = False
                self.special_ability_cooldown = 0
                self.is_special_ability_used = False

        pygame.quit()
        sys.exit()