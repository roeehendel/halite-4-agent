from actors.actor_container import ActorContainer
from actors.ship_actor import ShipActor


class ShipActorContainer(ActorContainer):
    def _create_actor(self, entity):
        return ShipActor(entity)

    def _get_entity_list(self):
        return self.board.current_player.ships

    def update(self, board):
        return super().update(board)
