from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "strategies" ADD "indicator_id" INT NOT NULL;
        CREATE TABLE IF NOT EXISTS "indicators" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "predefined_indicator_id" INT NOT NULL REFERENCES "predefined_indicators" ("id") ON DELETE CASCADE,
    "strategy_id" INT NOT NULL REFERENCES "strategies" ("id") ON DELETE CASCADE
);;
        ALTER TABLE "strategies" ADD CONSTRAINT "fk_strategi_indicato_5cea300d" FOREIGN KEY ("indicator_id") REFERENCES "indicators" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "strategies" DROP CONSTRAINT "fk_strategi_indicato_5cea300d";
        ALTER TABLE "strategies" DROP COLUMN "indicator_id";
        DROP TABLE IF EXISTS "indicators";"""
