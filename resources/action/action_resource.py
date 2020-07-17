from resources.resource import Resource


class ActionResource(Resource):
    def use(self, actor):
        raise NotImplementedError
