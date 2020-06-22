from kaggle_environments.envs.halite.helpers import ShipyardAction

from actors.actor import Actor
from government.flags import Flag, NotEnoughHaliteFlag


class ShipyardActor(Actor):
    def normal_mode(self, board):
        missing_halite = board.configuration.spawn_cost - board.current_player.halite
        if missing_halite > 0:
            self.raise_flag(NotEnoughHaliteFlag(missing_halite))
            return None
        return ShipyardAction.SPAWN

    def define_modes(self):
        modes = {
            'NORMAL': self.normal_mode,
        }

        default_mode = 'NORMAL'

        return modes, default_mode
