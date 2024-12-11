from app.permissions.models import PermissionCreateModel

PERMISSIONS = [
    PermissionCreateModel(
        name="create_role",
        description="Create a role",
    ),
    PermissionCreateModel(
        name="read_role",
        description="Read a role",
    ),
    PermissionCreateModel(
        name="update_role",
        description="Update a role",
    ),
    PermissionCreateModel(
        name="delete_role",
        description="Delete a role",
    ),
]
