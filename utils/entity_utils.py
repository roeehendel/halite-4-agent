def get_entity_by_id(entity_list, entity_id):
    return next(entity for entity in entity_list if entity.id == entity_id)
