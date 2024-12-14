from loguru import logger
from sqlalchemy import insert, select, delete, update, exc

from app.database import DatabaseManager
from app.exceptions import EntityNotFoundError
from app.cart.schema import Cart, CartItems
from app.cart.models import CreateCartRequestModel, AddToCartRequestModel
from app.products.schema import Product


class CartRepository:
    def __init__(self):
        self.db = DatabaseManager._instance

    async def create(self, user_id: int, cart: CreateCartRequestModel) -> int:
        async with self.db.engine.begin() as connection:
            try:
                q = (
                    insert(Cart)
                    .values(
                        user_id=user_id,
                        name=cart.name,
                        reminder_date=cart.reminder_date,
                    )
                    .returning(Cart.id)
                )
                result = await connection.execute(q)
                cart_id = result.scalar()
                return cart_id
            except exc.SQLAlchemyError as e:
                logger.exception(f"Error creating cart: {e=}")
                raise e

    async def get(self, user_id: int, cart_id: int):
        async with self.db.engine.begin() as connection:
            try:
                q = (
                    select(Cart)
                    .where(Cart.user_id == user_id)
                    .where(Cart.id == cart_id)
                )
                result = await connection.execute(q)
                if not (cart := result.scalar()):
                    raise EntityNotFoundError(entity="Cart")

                return cart
            except exc.SQLAlchemyError as e:
                logger.exception(f"Error getting cart: {e=}")
                raise e

    async def get_all(self, user_id: int):
        async with self.db.engine.begin() as connection:
            try:
                q = select(Cart).where(Cart.user_id == user_id)
                result = await connection.execute(q)
                return result.fetchall()
            except exc.SQLAlchemyError as e:
                logger.exception(f"Error getting cart: {e=}")
                raise e

    async def delete(self, user_id: int, cart_id: int):
        async with self.db.engine.begin() as connection:
            try:
                q = (
                    delete(Cart)
                    .where(Cart.user_id == user_id)
                    .where(Cart.id == cart_id)
                )
                await connection.execute(q)
                return True
            except exc.SQLAlchemyError as e:
                logger.exception(f"Error deleting cart: {e=}")
                raise e

    async def update(
        self, user_id: int, cart_id: int, cart: CreateCartRequestModel
    ) -> int:
        async with self.db.engine.begin() as connection:
            try:
                q = (
                    update(Cart)
                    .where(Cart.user_id == user_id)
                    .where(Cart.id == cart_id)
                    .values(
                        name=cart.name,
                        reminder_date=cart.reminder_date,
                    )
                ).returning(Cart.id)
                result = await connection.execute(q)
                return result.scalar()
            except exc.SQLAlchemyError as e:
                logger.exception(f"Error updating cart: {e=}")
                raise e

    async def add_item(
        self, user_id: int, cart_id: int, item: AddToCartRequestModel
    ):
        async with self.db.engine.begin() as connection:
            try:
                q = (
                    select(Cart)
                    .where(Cart.user_id == user_id)
                    .where(Cart.id == cart_id)
                )
                result = await connection.execute(q)
                if not result.scalar():
                    logger.warning(f"Unauthorized access report: {user_id=}")
                    raise EntityNotFoundError(entity="Cart")

                q = select(Product).where(Product.id == item.product_id)
                result = await connection.execute(q)
                if not result.scalar():
                    raise EntityNotFoundError(entity="Product")

                q = (
                    insert(CartItems)
                    .values(
                        cart_id=cart_id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                    )
                    .returning(CartItems.id)
                )
                result = await connection.execute(q)
                return result.scalar()
            except exc.SQLAlchemyError as e:
                logger.exception(f"Error adding items to cart: {e=}")
                raise e