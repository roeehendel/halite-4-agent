class Actor:
    def __init__(self, entity):
        """
        :param entity: the entity this actor represents
        """
        self._entity = entity
        self._mode = self.initial_mode()
        self.board = None
        self._requested_resources = []

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

    @property
    def position(self):
        return self._entity.position

    @property
    def resources(self):
        return [self.get_my_resource(type(rr)) for rr in self._requested_resources]

    def initial_mode(self):
        raise NotImplementedError

    def choose_mode(self):
        raise NotImplementedError

    def reset(self):
        self._requested_resources = []

    def get_my_resource(self, resource_type):
        resources_of_type = list(filter(lambda r: type(r) == resource_type, self._requested_resources))
        my_resources_of_type = list(filter(lambda r: r.allocated_to == self, resources_of_type))
        return my_resources_of_type[0] if len(my_resources_of_type) > 0 else None

    def request_resource(self, available_resources, resource_type, **kwargs):
        resources_of_type = list(filter(lambda r: type(r) == resource_type, available_resources))
        scores = {r: r.score(self, **kwargs) for r in resources_of_type}
        resources_of_type = list(filter(lambda r: scores[r] is not None, resources_of_type))

        if len(resources_of_type) > 0:
            # resource_to_request = max(resources_of_type, key=lambda r: r.score(self, **kwargs))
            resource_to_request = max(resources_of_type, key=lambda r: scores[r])
            resource_to_request.request(self)
            return resource_to_request
        else:
            return None

    def get_resource(self, available_resources, resource_type, kwargs):
        my_resource = self.get_my_resource(resource_type)
        if my_resource is not None:
            return my_resource
        else:
            requested_resource = self.request_resource(available_resources, resource_type, **kwargs)
            if requested_resource is not None:
                self._requested_resources.append(requested_resource)
                return 1
            else:
                return 0

    def _get_resource_requests(self, available_resources):
        raise NotImplementedError

    def request_resources(self, available_resources):
        resource_requests = self._get_resource_requests(available_resources)
        for resource_request in resource_requests:
            if self.get_resource(available_resources, resource_request[0], kwargs=resource_request[1]) == 1:
                break

    def use_resources(self):
        for r in self.resources:
            if r is not None:  # TODO change it, it's probably bad
                if not r.use(self):
                    break
