from abc import abstractmethod

from resources.resource import Resource


class ActionResource(Resource):
    @abstractmethod
    def use(self, actor):
        pass
