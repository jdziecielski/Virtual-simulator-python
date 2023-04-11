import pygame.display

from organism import Organism

RED = (200, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Animal(Organism):
    def __init__(self, strength, initiative, age, pos_x, pos_y, world):
        super().__init__(strength, initiative, age, pos_x, pos_y, world)

    def action(self):
        (new_x, new_y) = self.get_new_move()
        if (0 <= new_x < self.world.get_map_x()) and (0 <= new_y < self.world.get_map_y()):
            collided_with = self.world.get_organism_at_coordinates(new_x, new_y)
            if collided_with is not None:
                collided_with.collision(self)
            else:
                self.pos_x = new_x
                self.pos_y = new_y

    def attack(self, attacker):
        if attacker.strength >= self.strength:
            attacker.pos_x = self.pos_x
            attacker.pos_y = self.pos_y
            self.world.logs.append((self.get_name() + " died at: " + str(self.pos_x) + " " + str(self.pos_y)))
            self.world.organisms.remove(self)
        else:
            self.world.logs.append(attacker.get_name() + " died at: " + str(attacker.pos_x) + " " + str(attacker.pos_y))
            self.world.organisms.remove(attacker)

    def breed(self, collided_with):
        if self.get_free_adjacent_point() is not None:
            (x, y) = self.get_free_adjacent_point()
            if (self.was_organism_just_added is False) and (collided_with.was_organism_just_added is False):
                animal_type = self.world.animals_classes[self.get_name()]
                self.world.add_organism(animal_type(0, x, y, self.world))

    def collision(self, collided_with):
        if type(self) == type(collided_with):
            self.breed(collided_with)
        else:
            self.attack(collided_with)

    def get_name(self):
        pass