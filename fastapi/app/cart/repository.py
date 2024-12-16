import datetime
from loguru import logger
from sqlalchemy import insert, select, delete, update, exc

from app.database import DatabaseManager
from app.exceptions import EntityNotFoundError
from app.cart.schema import Cart, CartItems, CartStatus
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
            except Exception as e:
                logger.error(f"Error creating cart: {e=}")
                raise e

    async def update_cart_status(self, cart: dict) -> dict:
        def reminder_date_is_passed(
            reminder_date: datetime.datetime, by: int = 0
        ):
            reminder_date_timezone = reminder_date.tzinfo
            reminder_date += datetime.timedelta(days=by)
            if reminder_date < datetime.datetime.now(
                tz=reminder_date_timezone
            ):
                return True

            return False

        async with self.db.engine.begin() as connection:
            if reminder_date_is_passed(cart["reminder_date"], by=3):
                q = (
                    update(Cart)
                    .where(Cart.id == cart["id"])
                    .values(reminder_date=None, status=CartStatus.ABANDONED)
                ).returning(Cart)

                result = await connection.execute(q)
                cart = result.fetchone()
                return cart._asdict()

            return cart

    async def get(self, user_id: int, cart_id: int) -> dict:
        async with self.db.engine.begin() as connection:
            try:
                q = (
                    select(Cart)
                    .where(Cart.user_id == user_id)
                    .where(Cart.id == cart_id)
                )
                result = await connection.execute(q)
                if not (cart := result.fetchone()):
                    raise EntityNotFoundError(entity="Cart")

                cart = await self.update_cart_status(cart._asdict())

                q = select(CartItems).where(CartItems.cart_id == cart["id"])
                result = await connection.execute(q)

                cart["items"] = [item._asdict() for item in result.fetchall()]
                return cart
            except exc.SQLAlchemyError as e:
                logger.exception(f"Error getting cart: {e=}")
                raise e
            except Exception as e:
                logger.error(f"Error getting cart: {e=}")
                raise e

    async def get_all(self, user_id: int):
        async with self.db.engine.begin() as connection:
            try:
                q = select(Cart).where(Cart.user_id == user_id)
                result = await connection.execute(q)
                all_carts = [
                    await self.update_cart_status(cart._asdict())
                    for cart in result.fetchall()
                ]
                return all_carts
            except exc.SQLAlchemyError as e:
                logger.exception(f"Error getting cart: {e=}")
                raise e
            except Exception as e:
                logger.error(f"Error getting cart: {e=}")
                raise e

    async def delete(self, user_id: int, cart_id: int):
        async with self.db.engine.begin() as connection:
            try:
                q = (
                    select(Cart)
                    .where(Cart.id == cart_id)
                    .where(Cart.user_id == user_id)
                )
                result = await connection.execute(q)
                if not result.scalar():
                    logger.warning(f"Unauthorized access report: {user_id=}")
                    raise EntityNotFoundError(entity="Cart")

                q = (
                    delete(Cart)
                    .where(Cart.user_id == user_id)
                    .where(Cart.id == cart_id)
                )
                await connection.execute(q)
                return cart_id
            except exc.SQLAlchemyError as e:
                logger.exception(f"Error deleting cart: {e=}")
                raise e
            except Exception as e:
                logger.error(f"Error deleting cart: {e=}")
                raise e

    async def update(
        self, user_id: int, cart_id: int, cart: CreateCartRequestModel
    ) -> int:
        async with self.db.engine.begin() as connection:
            try:
                q = (
                    select(Cart)
                    .where(Cart.id == cart_id)
                    .where(Cart.user_id == user_id)
                )
                result = await connection.execute(q)
                if not result.scalar():
                    logger.warning(f"Unauthorized access report: {user_id=}")
                    raise EntityNotFoundError(entity="Cart")

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
            except Exception as e:
                logger.error(f"Error updating cart: {e=}")
                raise e

    async def add_item(self, user_id: int, item: AddToCartRequestModel):
        async with self.db.engine.begin() as connection:
            try:
                q = (
                    select(Cart)
                    .where(Cart.user_id == user_id)
                    .where(Cart.id == item.cart_id)
                )
                result = await connection.execute(q)
                if not result.scalar():
                    logger.warning(f"Unauthorized access report: {user_id=}")
                    raise EntityNotFoundError(entity="Cart")

                q = select(Product).where(Product.id == item.product_id)
                result = await connection.execute(q)
                if not result.scalar():
                    logger.warning(f"Product not found: {item.product_id=}")
                    raise EntityNotFoundError(entity="Product")

                q = (
                    insert(CartItems)
                    .values(
                        cart_id=item.cart_id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                    )
                    .returning(CartItems.id)
                )
                result = await connection.execute(q)
                return result.fetchone()[0]
            except exc.SQLAlchemyError as e:
                logger.exception(f"Error adding items to cart: {e=}")
                raise e
            except Exception as e:
                logger.error(f"Error adding items to cart: {e=}")
                raise e

    async def remove_item(self, user_id: int, cart_id: int, product_id: int):
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

                q = (
                    select(CartItems)
                    .where(CartItems.cart_id == cart_id)
                    .where(CartItems.product_id == product_id)
                )
                result = await connection.execute(q)
                if not result.scalar():
                    raise EntityNotFoundError(entity="Item")

                q = delete(CartItems).where(CartItems.cart_id == cart_id)
                await connection.execute(q)
                return cart_id
            except exc.SQLAlchemyError as e:
                logger.exception(f"Error removing items from cart: {e=}")
                raise e
            except Exception as e:
                logger.error(f"Error removing items from cart: {e=}")
                raise e
