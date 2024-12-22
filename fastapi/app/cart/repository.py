import datetime
from math import ceil

from loguru import logger
from sqlalchemy import delete, exc, func, insert, select, update

from app.cart.models import AddToCartRequestModel, CreateCartRequestModel
from app.cart.schema import Cart, CartItems, CartStatus
from app.database import DatabaseManager
from app.exceptions import EntityNotFoundError
from app.products.schema import Product
from app.repository import BaseRepository


class CartRepository(BaseRepository):
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

    async def _get_total_carts(self, connection, user_id: int) -> int:
        """Get total number of carts for a user."""
        count_query = select(func.count(Cart.id)).where(
            Cart.user_id == user_id
        )
        return await connection.scalar(count_query)

    async def _get_paginated_carts(
        self, connection, cart_id: int, user_id: int, offset: int, limit: int
    ) -> list[dict]:
        """Get paginated cart records."""
        carts_query = select(Cart).where(Cart.user_id == user_id)
        if cart_id:
            carts_query = carts_query.where(Cart.id == cart_id)

        carts_query = carts_query.order_by(Cart.id).offset(offset).limit(limit)
        carts_result = await connection.execute(carts_query)
        return [cart._asdict() for cart in carts_result.fetchall()]

    async def _get_cart_items(
        self, connection, cart_ids: list[int]
    ) -> list[dict]:
        """Get items for multiple carts."""
        if not cart_ids:
            return []

        items_query = select(CartItems).where(CartItems.cart_id.in_(cart_ids))
        items_result = await connection.execute(items_query)
        return [item._asdict() for item in items_result.fetchall()]

    async def _associate_items_with_carts(
        self, carts: list[dict], items: list[dict]
    ) -> list[dict]:
        """Associate items with their respective carts."""
        items_by_cart = {}
        for item in items:
            cart_id = item["cart_id"]
            if cart_id not in items_by_cart:
                items_by_cart[cart_id] = []
            items_by_cart[cart_id].append(item)

        for cart in carts:
            cart["items"] = items_by_cart.get(cart["id"], [])

        return carts

    async def get_all(
        self,
        user_id: int,
        cart_id: int = None,
        get_items: bool = True,
        page: int = 1,
        page_size: int = 10,
    ) -> dict:
        """Get paginated list of carts with their items."""
        async with self.db.engine.begin() as connection:
            try:
                total = 1
                if not cart_id:
                    total = await self._get_total_carts(connection, user_id)

                offset = (page - 1) * page_size
                carts = await self._get_paginated_carts(
                    connection, cart_id, user_id, offset, page_size
                )

                cart_ids = [cart["id"] for cart in carts]

                if get_items:
                    items = await self._get_cart_items(connection, cart_ids)
                    carts = await self._associate_items_with_carts(
                        carts, items
                    )

                for cart in carts:
                    if not cart.get("reminder_date"):
                        continue

                    try:
                        cart = await self.update_cart_status(cart)
                    except Exception as e:
                        logger.error(f"Error updating cart status: {e}")

                return {
                    "items": carts if carts else [],
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                    "total_pages": max(
                        ceil(total / page_size) if total > 0 else 1, 1
                    ),
                }

            except exc.SQLAlchemyError as e:
                logger.exception(f"Error getting carts: {e=}")
                raise e
            except Exception as e:
                logger.error(f"Error getting carts: {e=}")
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
