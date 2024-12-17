from app.permissions.models import PermissionCreateModel

PERMISSIONS = [
    PermissionCreateModel(
        name="create_cart",
        description="Create a cart",
    ),
    PermissionCreateModel(
        name="read_cart",
        description="Read a cart",
    ),
    PermissionCreateModel(
        name="update_cart",
        description="Update a cart",
    ),
    PermissionCreateModel(
        name="delete_cart",
        description="Delete a cart",
    ),
]
