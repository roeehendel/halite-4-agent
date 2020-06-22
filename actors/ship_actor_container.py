from actors.actor_container import ActorContainer
from actors.ship_actor import ShipActor


class ShipActorContainer(ActorContainer):
    def create_actor(self, entity):
        return ShipActor(entity)

    def get_entity_list(self):
        return self.board.current_player.ships

    def update(self, board, government_flags):
        return super().update(board, government_flags)
