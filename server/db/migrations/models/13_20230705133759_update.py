from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "strategies" DROP CONSTRAINT "fk_strategi_stocks_144787c5";
        ALTER TABLE "strategies" RENAME COLUMN "stocks_id" TO "stock_id";
        ALTER TABLE "strategies" ADD CONSTRAINT "fk_strategi_stocks_6acdc9a3" FOREIGN KEY ("stock_id") REFERENCES "stocks" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "strategies" DROP CONSTRAINT "fk_strategi_stocks_6acdc9a3";
        ALTER TABLE "strategies" RENAME COLUMN "stock_id" TO "stocks_id";
        ALTER TABLE "strategies" ADD CONSTRAINT "fk_strategi_stocks_144787c5" FOREIGN KEY ("stocks_id") REFERENCES "stocks" ("id") ON DELETE CASCADE;"""
