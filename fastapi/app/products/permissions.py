from app.permissions.models import PermissionCreateModel

PERMISSIONS = [
    PermissionCreateModel(
        name="create_product",
        description="Create a product",
    ),
    PermissionCreateModel(
        name="read_product",
        description="Read a product",
    ),
    PermissionCreateModel(
        name="update_product",
        description="Update a product",
    ),
    PermissionCreateModel(
        name="delete_product",
        description="Delete a product",
    ),
]
