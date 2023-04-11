import random

import animal

WHITE = (255, 255, 255)

class Antelope(animal.Animal):
    def __init__(self, age, pos_x, pos_y, world, strength=4, initiative=4):
        super(Antelope, self).__init__(strength, initiative, age, pos_x, pos_y, world)

    def get_new_move(self):
        rand = random.randrange(4)
        if rand == 0:
            return self.pos_x, self.pos_y - 2
        elif rand == 1:  # go down
            return self.pos_x, self.pos_y + 2
        elif rand == 2:  # go left
            return self.pos_x - 2, self.pos_y
        elif rand == 3:  # go right
            return self.pos_x + 2, self.pos_y

    def action(self):
        (new_x, new_y) = self.get_new_move()
        if (0 <= new_x < self.world.get_map_x()) and (0 <= new_y < self.world.get_map_y()):
            collided_with = self.world.get_organism_at_coordinates(new_x, new_y)
            if collided_with is not None:
                collided_with.collision(self)
            else:
                self.pos_x = new_x
                self.pos_y = new_y

    def collision(self, collided_with):
        if type(self) == type(collided_with):
            self.breed(collided_with)
        else:
            rand = random.randint(0, 1)
            if rand == 1:
                if self.get_free_adjacent_point() is not None:
                    (x, y) = self.get_free_adjacent_point()
                    self.pos_x = x
                    self.pos_y = y
                    self.world.logs.append("Antelope has has ran away!")
                else:
                    self.world.logs.append("Antelope has no free space to escape!")
            else:
                self.attack(collided_with)

    def get_text(self):
        return self.world.get_font().render('A', False, WHITE)

    def get_name(self):
        return 'Antelope'