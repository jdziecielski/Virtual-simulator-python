import plant

WHITE = (255, 255, 255)

class Guarana(plant.Plant):
    def __init__(self, age, pos_x, pos_y, world, strength=0, initiative=0):
        super(Guarana, self).__init__(strength, initiative, age, pos_x, pos_y, world)

    def action(self):
        super().action()

    def collision(self, collided_with):
        if collided_with.strength >= self.strength:
            self.world.logs.append(self.get_name() + " has been eaten at " + str(self.pos_x) + " " + str(self.pos_y))
            collided_with.pos_x = self.pos_x
            collided_with.pos_y = self.pos_y
            collided_with.strength += 3
            self.world.logs.append(collided_with.get_name() + " strength is " + str(collided_with.strength) + " now!")
            self.world.organisms.remove(self)

    def get_text(self):
        return self.world.get_font().render('gu', False, WHITE)

    def get_name(self):
        return 'Guarana'