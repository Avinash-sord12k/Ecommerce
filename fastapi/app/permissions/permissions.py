from app.permissions.models import PermissionCreateModel

PERMISSIONS = [
    PermissionCreateModel(
        name="create_permission",
        description="Create a permission",
    ),
    PermissionCreateModel(
        name="read_permission",
        description="Read a permission",
    ),
]
