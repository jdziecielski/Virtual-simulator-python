import plant

WHITE = (255, 255, 255)

class Belladonna(plant.Plant):
    def __init__(self, age, pos_x, pos_y, world, strength=99, initiative=0):
        super(Belladonna, self).__init__(strength, initiative, age, pos_x, pos_y, world)


    def action(self):
        super().action()

    def collision(self, collided_with):
        self.world.logs.append(self.get_name() + " has eaten " + collided_with.get_name() + " at " + str(collided_with.pos_x) + " " + str(collided_with.pos_y))
        self.world.organisms.remove(collided_with)

    def get_text(self):
        return self.world.get_font().render('b', False, WHITE)

    def get_name(self):
        return 'Belladonna'