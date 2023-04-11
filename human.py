from animal import Animal
from organism import WHITE


class Human(Animal):
    next_turn_x = None
    next_turn_y = None

    def __init__(self, age, pos_x, pos_y, world, strength=5, initiative=4):
        super().__init__(strength, initiative, age, pos_x, pos_y, world)
        self.next_turn_x = pos_x
        self.next_turn_y = pos_y

    def action(self):
        if (0 <= self.next_turn_x < self.world.get_map_x()) and (0 <= self.next_turn_y < self.world.get_map_y()):
            collided_with = self.world.get_organism_at_coordinates(self.next_turn_x, self.next_turn_y)
            if collided_with is not None:
                collided_with.collision(self)
            else:
                self.pos_x = self.next_turn_x
                self.pos_y = self.next_turn_y

    def set_move_next_for_turn(self, x, y):
        self.next_turn_x = x
        self.next_turn_y = y

    def collision(self, collided_with):
        if type(self) == type(collided_with):
            pass
        else:
            self.attack(collided_with)

    def get_text(self):
        return self.world.get_font().render("H", False, WHITE)

    def get_name(self):
        return 'Human'

    def magical_potion(self):
        self.world.original_strength = self.strength
        self.strength = 10
        self.world.is_special_ability_used = True