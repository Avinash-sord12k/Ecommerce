class CategoryIntegrityError(Exception):
    def __init__(self, message="Category with this name already exists."):
        self.message = message
        super().__init__(self.message)


class SubCategoryIntegrityError(Exception):
    def __init__(self, message="SubCategory with this name already exists."):
        self.message = message
        super().__init__(self.message)
