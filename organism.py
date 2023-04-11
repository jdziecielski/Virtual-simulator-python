from random import randrange

WHITE = (255, 255, 255)


class Organism:
    age = 0
    strength = 0
    initiative = None
    world = None
    pos_x = None
    pos_y = None
    was_organism_just_added = True

    def __init__(self, strength, initiative, age, pos_x, pos_y, world):
        self.strength = strength
        self.initiative = initiative
        self.age = age
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.world = world

    def get_new_move(self):
        rand = randrange(4)
        if rand == 0:
            return self.pos_x, self.pos_y - 1
        elif rand == 1:  # go down
            return self.pos_x, self.pos_y + 1
        elif rand == 2:  # go left
            return self.pos_x - 1, self.pos_y
        elif rand == 3:  # go right
            return self.pos_x + 1, self.pos_y

    def get_free_adjacent_point(self):
        offsets = [(-1, 0), (0, -1), (0, 1), (1, 0)]

        for i, j in offsets:
            x = self.pos_x + i
            y = self.pos_y + j
            if (0 <= x < self.world.get_map_x()) and (0 <= y < self.world.get_map_y()) and (
                    self.world.get_organism_at_coordinates(x, y) is None):
                return x, y

        return None

    def action(self):
        pass

    def collision(self, attacker):
        pass

    def draw(self):
        pass

    def get_text(self):
        pass

    def get_name(self):
        pass
