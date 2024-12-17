class MaximumAddressLimitReachedError(Exception):
    def __init__(self, message="Maximum address limit reached"):
        self.message = message
        super().__init__(self.message)
