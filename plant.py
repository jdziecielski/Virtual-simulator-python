from random import randrange

from organism import Organism

class Plant(Organism):
    def __init__(self, strength, initiative, age, pos_x, pos_y, world):
        super().__init__(strength, initiative, age, pos_x, pos_y, world)

    def action(self):
        rand = randrange(10)
        if rand == 0:
            self.sow()

    def sow(self):
        if self.get_free_adjacent_point() is not None:
            (x, y) = self.get_free_adjacent_point()
            if self.was_organism_just_added is False:
                organism_type = self.world.plants_classes[self.get_name()]
                self.world.add_organism(organism_type(0, x, y, self.world))
                self.world.logs.append(self.get_name() + " is growing at " + str(self.pos_x) + " " + str(self.pos_y))


    def collision(self, collided_with):
        if collided_with.strength >= self.strength:
            self.world.logs.append(self.get_name() + " has been exterminated at " + str(self.pos_x) + " " + str(self.pos_y))
            collided_with.pos_x = self.pos_x
            collided_with.pos_y = self.pos_y
            self.world.organisms.remove(self)
