from app.permissions.models import PermissionCreateModel

PERMISSIONS = [
    PermissionCreateModel(
        name="create_address",
        description="Create an address",
    ),
    PermissionCreateModel(
        name="read_address",
        description="Read an address",
    ),
    PermissionCreateModel(
        name="update_address",
        description="Update an address",
    ),
    PermissionCreateModel(
        name="delete_address",
        description="Delete an address",
    ),
]
