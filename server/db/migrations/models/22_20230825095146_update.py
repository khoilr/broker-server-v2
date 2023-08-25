from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "strategies" DROP COLUMN "notified";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "strategies" ADD "notified" BOOL;"""
