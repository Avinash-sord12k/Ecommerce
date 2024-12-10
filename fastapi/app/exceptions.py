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


class NotEnoughPermissionsError(Exception):
    def __init__(self, message: str = "Not enough permissions"):
        self.message = message
        super().__init__(self.message)
