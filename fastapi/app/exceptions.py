class EntityIntegrityError(Exception):
    def __init__(
        self, entity: str, message: str = "This {} already exists"
    ) -> None:
        self.message = message.format(entity if entity else "Entity")
        super().__init__(self.message)


class EntityNotFoundError(Exception):
    def __init__(
        self, entity: str, message: str = "This {} does not exist"
    ) -> None:
        self.message = message.format(entity if entity else "Entity")
        super().__init__(self.message)
