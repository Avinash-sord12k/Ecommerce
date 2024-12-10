from app.permissions.models import PermissionCreateModel

PERMISSIONS = [
    PermissionCreateModel(
        name="create_category",
        description="Create a category",
    ),
    PermissionCreateModel(
        name="read_category",
        description="Read a category",
    ),
    PermissionCreateModel(
        name="delete_category",
        description="Delete a category",
    ),
]
