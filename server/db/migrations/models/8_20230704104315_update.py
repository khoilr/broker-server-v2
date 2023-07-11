from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "predefined_params" ADD "label" VARCHAR(255) NOT NULL;
        ALTER TABLE "predefined_params" ADD "name" VARCHAR(255) NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "predefined_params" DROP COLUMN "label";
        ALTER TABLE "predefined_params" DROP COLUMN "name";"""
