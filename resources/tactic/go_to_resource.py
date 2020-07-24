from abc import abstractmethod

from resources.resource import Resource


class GoToResource(Resource):
    def __init__(self, cell):
        super().__init__()
        self.cell = cell

    @classmethod
    @abstractmethod
    def cells(cls):
        pass

    @classmethod
    def instances(cls, actor_groups):
        return [cls(cell) for cell in cls.cells()]

    @classmethod
    @abstractmethod
    def score_matrix(cls, actor_groups, instances):
        pass
