class NotFoundError(Exception):
    def __init__(self, entity: str, entity_id: int | str):
        self.entity = entity
        self.entity_id = entity_id
        self.detail = f"{entity} with id {entity_id} not found"
        super().__init__(self.detail)


class BusinessLogicError(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.detail)


class ExternalAPIError(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.detail)
