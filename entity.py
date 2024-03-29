from position import Position
from action import Action, ActionType

class EntityRecipe:
    position: Position
    team: int
    movement_range: int
    attack_range: int
    name: str
    health: int = 10
    damage: int = 1

    def __init__(self, position: Position, name: str, movement_range: int = 1, team: int = 0, attack_range: int = 1, health: int = 10, damage: int = 1):
        self.position = position
        self.name = name
        self.movement_range = movement_range

        self.team = team
        self.attack_range = attack_range
        self.health = health
        self.damage = damage

    def default():
        return EntityRecipe(Position(0, 0), "Entity")

class Entity:
    position: Position
    team: int
    movement_range: int
    attack_range: int
    name: str
    display_character: str
    health: int = 10
    damage: int = 1

    def __init__(self, entity_recipe: EntityRecipe):
        self.position = entity_recipe.position
        self.name = entity_recipe.name
        self.movement_range = entity_recipe.movement_range
        self.display_character = self.name[0]
        self.team = entity_recipe.team
        self.attack_range = entity_recipe.attack_range
        self.health = entity_recipe.health
        self.damage = entity_recipe.damage

    def llm_friendly_string(self):
        info_str = f"I am {self.name}, I am represented by {self.display_character}\n"
        info_str += f"I am on team {self.team}\n"
        info_str += f"I have {self.health} health\n"
        info_str += f"I can do {self.damage} damage\n"
        info_str += f"I can move {self.movement_range} tiles\n"
        info_str += f"My attack range is {self.attack_range} tiles\n"
        info_str += f"I am at position {self.position}\n\n"
        return info_str

    def third_person_string(self):
        # it should print in the format (Name, (Health: Amount, Damage: Amount))
        return f"{self.name}, (Health: {self.health}, Damage: {self.damage})"
    
    def calculate_valid_moves(self, game):
        # this will return a list of Actions where the action_type is MOVE and the payload is a Position
        valid_moves = []
        for x in range(-self.movement_range, self.movement_range + 1):
            for y in range(-self.movement_range, self.movement_range + 1):
                if x == 0 and y == 0:
                    continue
                new_position = Position(self.position.x + x, self.position.y + y)
                # don't allow moving off the board
                if new_position.x < 0 or new_position.x >= game.board.x_size or new_position.y < 0 or new_position.y >= game.board.y_size:
                    continue
                    
                # don't allow moving onto a tile with an entity
                if game.board.get_entity(new_position) is not None:
                    continue
                
                
                if game.board.get_tile(new_position) is not None:
                    valid_moves.append(Action(ActionType.MOVE, new_position))

        return valid_moves

    def calculate_valid_attacks(self, game):
        # this will return a list of Actions where the action_type is ATTACK and the payload is a Position
        # make sure that anyone on that tile is on the other team
        valid_attacks = []
        for x in range(-self.attack_range, self.attack_range + 1):
            for y in range(-self.attack_range, self.attack_range + 1):
                if x == 0 and y == 0:
                    continue
                new_position = Position(self.position.x + x, self.position.y + y)
                if new_position.x < 0 or new_position.x >= game.board.x_size or new_position.y < 0 or new_position.y >= game.board.y_size:
                    continue
                entity = game.board.get_entity(new_position)
                
                if entity is not None and entity.team != self.team:
                    valid_attacks.append(Action(ActionType.ATTACK, (new_position, entity.name)))
        return valid_attacks