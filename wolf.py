import animal

WHITE = (255, 255, 255)

class Wolf(animal.Animal):
    def __init__(self, age, pos_x, pos_y, world, strength=9, initiative=5):
        super(Wolf, self).__init__(strength, initiative, age, pos_x, pos_y, world)

    def action(self):
        super().action()

    def collision(self, collided_with):
        super().collision(collided_with)

    def get_text(self):
        return self.world.get_font().render('W', False, WHITE)

    def get_name(self):
        return 'Wolf'