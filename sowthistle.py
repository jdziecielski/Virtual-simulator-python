import plant

WHITE = (255, 255, 255)

class Sowthistle(plant.Plant):
    def __init__(self, age, pos_x, pos_y, world, strength=0, initiative=0):
        super(Sowthistle, self).__init__(strength, initiative, age, pos_x, pos_y, world)

    def action(self):
        for _ in range(3):
            super().action()

    def collision(self, collided_with):
        super().collision(collided_with)

    def get_text(self):
        return self.world.get_font().render('s', False, WHITE)

    def get_name(self):
        return 'Sowthistle'