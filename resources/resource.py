class Resource:
    def __init__(self, board):
        self.board = board
        self.requested_by = []  # list of requesting actors
        self.allocated_to = None  # the actor that was allocated the resource

    def has_collision(self):
        return len(self.requested_by) > 1

    def resolve_collision(self):
        self.allocated_to = self._resolve_collision()
        self.requested_by = []

    def _resolve_collision(self):
        raise NotImplementedError

    def score(self, actor, **kwargs):
        raise NotImplementedError

    def request(self, actor):
        self.requested_by.append(actor)

    def use(self, actor):
        return True

    def allocate_to_single_request(self):
        self.allocated_to = self.requested_by[0]
        self.requested_by = []

    @classmethod
    def _resource_instances(cls, board):
        raise NotImplementedError

    @classmethod
    def allocate(cls, board, actors):
        resource_instances = cls._resource_instances(board)

        # This loops ends
        for i in range(10):
            # Get unsatisfied resource requests
            for actor in actors:
                actor.request_resources(resource_instances)

            collisions_occurred = False
            for resource in resource_instances:
                if resource.has_collision():
                    # if hasattr(resource, 'destination_position'):
                    #     print(resource, resource.requested_by)
                    collisions_occurred = True
                    resource.resolve_collision()
                    # if hasattr(resource, 'destination_position'):
                    #     print(resource, resource.cell.position, resource.allocated_to)

            if not collisions_occurred:
                # If not more collisions, stop
                break

            # Filter out all allocated resources
            resource_instances = list(filter(lambda r: r.allocated_to is None, resource_instances))

        # Allocate unallocated resources with one request
        resources_with_one_request = list(filter(lambda r: len(r.requested_by) == 1, resource_instances))
        for resource in resources_with_one_request:
            resource.allocate_to_single_request()
