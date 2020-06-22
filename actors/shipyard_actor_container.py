from actors.actor_container import ActorContainer
from actors.shipyard_actor import ShipyardActor


class ShipyardActorContainer(ActorContainer):
    def create_actor(self, entity):
        return ShipyardActor(entity)

    def get_entity_list(self):
        return self.board.current_player.shipyards

    def update(self, board, government_flags):
        return super().update(board, government_flags)
