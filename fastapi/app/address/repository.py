from sqlalchemy import insert, exc, select, delete, update, func
from loguru import logger

from app.config import MAXIMUM_ADDRESS_CREATION_LIMIT_PER_USER
from app.exceptions import EntityNotFoundError
from app.address.models import AddressCreateModel
from app.address.schema import Address
from app.database import DatabaseManager
from app.address.exceptions import MaximumAddressLimitReachedError


class AddressRepository:
    def __init__(self):
        self.db = DatabaseManager._instance

    async def address_limit_reached(self, user_id: int):
        async with self.db.engine.begin() as connection:
            try:
                q = select(func.count(Address.id)).where(
                    Address.user_id == user_id
                )
                result = await connection.execute(q)
                return (
                    result.scalar() >= MAXIMUM_ADDRESS_CREATION_LIMIT_PER_USER
                )
            except exc.SQLAlchemyError as e:
                logger.exception(f"Error getting address: {e}")
                raise e
            except Exception as e:
                logger.error(f"Error getting address: {e}")
                raise e

    async def create(self, user_id: int, address: AddressCreateModel) -> int:
        async with self.db.engine.begin() as connection:
            try:
                if await self.address_limit_reached(user_id):
                    raise MaximumAddressLimitReachedError()

                q = (
                    insert(Address)
                    .values(
                        name=address.name,
                        address=address.address,
                        city=address.city,
                        state=address.state,
                        zip_code=address.pincode,
                        country=address.country,
                        user_id=user_id,
                    )
                    .returning(Address.id)
                )
                result = await connection.execute(q)
                address_id = result.scalar()
                return address_id
            except exc.SQLAlchemyError as e:
                logger.exception(f"Error creating address: {e}")
                raise e
            except Exception as e:
                logger.error(f"Error creating address: {e}")
                raise e

    async def get(self, user_id: int, address_id: int) -> dict:
        async with self.db.engine.begin() as connection:
            try:
                q = (
                    select(Address)
                    .where(Address.id == address_id)
                    .where(Address.user_id == user_id)
                )
                result = await connection.execute(q)
                if not (address := result.fetchone()):
                    raise EntityNotFoundError(entity="Address")

                return address._asdict()
            except exc.SQLAlchemyError as e:
                logger.exception(f"Error getting address: {e}")
                raise e
            except Exception as e:
                logger.error(f"Error getting address: {e}")
                raise e

    async def get_all(self, user_id: int):
        async with self.db.engine.begin() as connection:
            try:
                q = select(Address).where(Address.user_id == user_id)
                result = await connection.execute(q)
                all_addresses = [
                    address._asdict() for address in result.fetchall()
                ]
                return all_addresses
            except exc.SQLAlchemyError as e:
                logger.exception(f"Error getting address: {e}")
                raise e
            except Exception as e:
                logger.error(f"Error getting address: {e}")
                raise e

    async def update(
        self, user_id: int, address_id: int, address: AddressCreateModel
    ):
        async with self.db.engine.begin() as connection:
            try:
                q = (
                    select(Address)
                    .where(Address.id == address_id)
                    .where(Address.user_id == user_id)
                )
                result = await connection.execute(q)
                if not result.scalar():
                    raise EntityNotFoundError(entity="Address")

                q = (
                    update(Address)
                    .where(Address.user_id == user_id)
                    .where(Address.id == address_id)
                    .values(
                        name=address.name,
                        address=address.address,
                        city=address.city,
                        state=address.state,
                        zip_code=address.pincode,
                        country=address.country,
                    )
                )
                await connection.execute(q)
                return address_id
            except exc.SQLAlchemyError as e:
                logger.exception(f"Error updating address: {e}")
                raise e
            except Exception as e:
                logger.error(f"Error updating address: {e}")
                raise e

    async def delete(self, user_id: int, address_id: int):
        async with self.db.engine.begin() as connection:
            try:
                q = (
                    select(Address)
                    .where(Address.id == address_id)
                    .where(Address.user_id == user_id)
                )
                result = await connection.execute(q)
                if not result.scalar():
                    logger.warning(f"Unauthorized access report: {user_id=}")
                    raise EntityNotFoundError(entity="Address")

                q = (
                    delete(Address)
                    .where(Address.user_id == user_id)
                    .where(Address.id == address_id)
                )
                await connection.execute(q)
                return address_id
            except exc.SQLAlchemyError as e:
                logger.exception(f"Error deleting address: {e}")
                raise e
            except Exception as e:
                logger.error(f"Error deleting address: {e}")
                raise e
