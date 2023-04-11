import plant

WHITE = (255, 255, 255)

class Hogweed(plant.Plant):
    def __init__(self, age, pos_x, pos_y, world, strength=10, initiative=0):
        super(Hogweed, self).__init__(strength, initiative, age, pos_x, pos_y, world)
        self.world._is_hogweed_on_map = True

    def action(self):
        adjacent_points = [(-1, -1), (-1, 1), (1, 1), (1, -1), (-1, 0), (0, -1), (0, 1), (1, 0)]
        for i in adjacent_points:
            temp_organism = self.world.get_organism_at_coordinates(self.pos_x + i[0], self.pos_y + i[1])
            if temp_organism is not None and temp_organism.get_name() is not 'Cybersheep':
                self.world.logs.append(temp_organism.get_name() + " has died from toxic fumes at " + str(temp_organism.pos_x) + " " + str(temp_organism.pos_y))
                self.world.organisms.remove(temp_organism)

    def collision(self, collided_with):
        if collided_with.get_name() is not 'Cybersheep':
            self.world.logs.append(collided_with.get_name() + " has died from eating toxic hogweed at " + str(collided_with.pos_x) + " " + str(collided_with.pos_y))
            self.world.organisms.remove(collided_with)
        else:
            self.world.logs.append(self.get_name() + " was exterminated by " + collided_with.get_name() + " at " + str(self.pos_x) + " " + str(self.pos_y))
            collided_with.pos_x = self.pos_x
            collided_with.pos_y = self.pos_y
            self.world.organisms.remove(self)


    def get_text(self):
        return self.world.get_font().render('h', False, WHITE)

    def get_name(self):
        return 'Hogweed'