import animal

WHITE = (255, 255, 255)

class Fox(animal.Animal):
    def __init__(self, age, pos_x, pos_y, world, strength=3, initiative=7):
        super(Fox, self).__init__(strength, initiative, age, pos_x, pos_y, world)

    def action(self):
        (new_x, new_y) = self.get_new_move()
        if (0 <= new_x < self.world.get_map_x()) and (0 <= new_y < self.world.get_map_y()):
            collided_with = self.world.get_organism_at_coordinates(new_x, new_y)
            if collided_with is not None:
                if collided_with.get_name() != 'Fox':
                    if collided_with.strength > self.strength:
                        pass
                else:
                    collided_with.collision(self)
            else:
                self.pos_x = new_x
                self.pos_y = new_y

    def collision(self, collided_with):
        if type(self) == type(collided_with):
            self.breed(collided_with)
        else:
            self.attack(collided_with)

    def get_text(self):
        return self.world.get_font().render('F', False, WHITE)

    def get_name(self):
        return 'Fox'