def serialize(field_maps, fields_to_exclude=[]):
        for f in fields_to_exclude:
            del(field_maps[f])
        serialized = {}
        
        for f in field_maps:
            serialized[f] = field_maps[f]
            
        return serialized