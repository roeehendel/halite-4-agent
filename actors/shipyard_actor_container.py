from actors.actor_container import ActorContainer
from actors.shipyard_actor import ShipyardActor


class ShipyardActorContainer(ActorContainer):
    def _create_actor(self, entity):
        return ShipyardActor(entity)

    def _get_entity_list(self):
        return self.board.current_player.shipyards

    def update(self, board):
        return super().update(board)
