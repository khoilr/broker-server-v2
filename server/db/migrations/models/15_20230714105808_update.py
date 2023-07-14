from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "strategies" DROP CONSTRAINT "fk_strategi_stocks_6acdc9a3";
        ALTER TABLE "strategies" DROP COLUMN "stock_id";
        CREATE TABLE "strategies_stocks" (
    "strategies_id" INT NOT NULL REFERENCES "strategies" ("id") ON DELETE CASCADE,
    "stockmodel_id" INT NOT NULL REFERENCES "stocks" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "strategies_stocks";
        ALTER TABLE "strategies" ADD "stock_id" INT NOT NULL;
        ALTER TABLE "strategies" ADD CONSTRAINT "fk_strategi_stocks_6acdc9a3" FOREIGN KEY ("stock_id") REFERENCES "stocks" ("id") ON DELETE CASCADE;"""
