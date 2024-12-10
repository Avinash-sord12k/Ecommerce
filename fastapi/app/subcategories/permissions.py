from app.permissions.models import PermissionCreateModel

PERMISSIONS = [
    PermissionCreateModel(
        name="create_subcategory",
        description="Create a subcategory",
    ),
    PermissionCreateModel(
        name="read_subcategory",
        description="Read a subcategory",
    ),
    PermissionCreateModel(
        name="delete_subcategory",
        description="Delete a subcategory",
    ),
]
