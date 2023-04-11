import animal

WHITE = (255, 255, 255)

class Cybersheep(animal.Animal):
    def __init__(self, age, pos_x, pos_y, world, strength=11, initiative=4):
        super(Cybersheep, self).__init__(strength, initiative, age, pos_x, pos_y, world)

    def find_nearest_hogweed(self):
        hogweed_x = None
        hogweed_y = None
        distance_to_hogweed = self.world.get_map_x() + self.world.get_map_y()
        for o in self.world.organisms:
            if o.get_name() == 'Hogweed':
                temp_x = o.pos_x
                temp_y = o.pos_y
                distance_temp = abs(self.pos_x - temp_x) + abs(self.pos_y - temp_y)
                if distance_temp < distance_to_hogweed:
                    distance_to_hogweed = distance_temp
                    hogweed_x = temp_x
                    hogweed_y = temp_y

        if hogweed_x is not None and hogweed_y is not None:
            return hogweed_x, hogweed_y
        else:
            return None

    def action(self):
        hogweed_coordinates = self.find_nearest_hogweed()
        if self.world.get_is_hogweed_on_map() and hogweed_coordinates is not None:
            x_diff = hogweed_coordinates[0] - self.pos_x
            y_diff = hogweed_coordinates[1] - self.pos_y
            new_x = self.pos_x
            new_y = self.pos_y
            if x_diff != 0:
                if x_diff < 0:
                    new_x = self.pos_x - 1
                elif x_diff > 0:
                    new_x = self.pos_x + 1
            elif y_diff != 0:
                if y_diff < 0:
                    new_y = self.pos_y - 1
                elif y_diff > 0:
                    new_y = self.pos_y + 1

            temp_organism = self.world.get_organism_at_coordinates(new_x, new_y)
            if temp_organism is not None:
                temp_organism.collision(self)
            else:
                self.pos_x = new_x
                self.pos_y = new_y
        else:
            super().action()

    def collision(self, collided_with):
        super().collision(collided_with)

    def get_text(self):
        return self.world.get_font().render('C', False, WHITE)

    def get_name(self):
        return 'Cybersheep'