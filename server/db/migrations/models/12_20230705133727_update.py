from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "strategies_stocks";
        ALTER TABLE "strategies" ADD "stocks_id" INT NOT NULL;
        ALTER TABLE "strategies" ADD CONSTRAINT "fk_strategi_stocks_144787c5" FOREIGN KEY ("stocks_id") REFERENCES "stocks" ("id") ON DELETE CASCADE;
        CREATE UNIQUE INDEX "uid_predefined__name_290bd4" ON "predefined_indicators" ("name");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_predefined__name_290bd4";
        ALTER TABLE "strategies" DROP CONSTRAINT "fk_strategi_stocks_144787c5";
        ALTER TABLE "strategies" DROP COLUMN "stocks_id";
        CREATE TABLE "strategies_stocks" (
    "stockmodel_id" INT NOT NULL REFERENCES "stocks" ("id") ON DELETE CASCADE,
    "strategies_id" INT NOT NULL REFERENCES "strategies" ("id") ON DELETE CASCADE
);"""
