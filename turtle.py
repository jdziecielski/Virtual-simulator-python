import random

import animal

WHITE = (255, 255, 255)

class Turtle(animal.Animal):
    def __init__(self, age, pos_x, pos_y, world, strength=2, initiative=1):
        super(Turtle, self).__init__(strength, initiative, age, pos_x, pos_y, world)

    def action(self):
        rand = random.randint(0, 3)
        if rand == 1:
            super().action()

    def collision(self, collided_with):
        if type(self) == type(collided_with):
            self.breed(collided_with)
        else:
            if collided_with.strength < 5:
                self.world.logs.append("Turtle reflects attack!")
            else:
                self.attack(collided_with)

    def get_text(self):
        return self.world.get_font().render('T', False, WHITE)

    def get_name(self):
        return 'Turtle'