class Actor:
    def __init__(self, entity):
        """
        :param entity: the entity this actor represents
        """
        self._entity = entity
        self._modes, self.default_mode = self.define_modes()
        self._mode = self.default_mode
        self.flags = []

    @property
    def id(self):
        return self.entity.id

    @property
    def entity(self):
        return self._entity

    @entity.setter
    def entity(self, entity):
        self._entity = entity

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = mode

    def raise_flag(self, flag):
        self.flags.append(flag)

    def define_modes(self):
        raise NotImplementedError

    def choose_action(self, board):
        self.entity.next_action = self._modes[self.mode](board)
