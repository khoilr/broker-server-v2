from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "strategies" DROP CONSTRAINT "fk_strategi_indicato_5cea300d";
        ALTER TABLE "strategies" DROP COLUMN "indicator_id";
        CREATE TABLE IF NOT EXISTS "parameters" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "value" VARCHAR(50) NOT NULL,
    "indicator_id" INT NOT NULL REFERENCES "indicators" ("id") ON DELETE CASCADE,
    "predefined_param_id" INT NOT NULL REFERENCES "predefined_params" ("id") ON DELETE CASCADE
);;
        CREATE TABLE IF NOT EXISTS "conditions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "source" VARCHAR(50) NOT NULL,
    "change" VARCHAR(50) NOT NULL,
    "value" VARCHAR(50) NOT NULL,
    "unit" VARCHAR(50) NOT NULL,
    "indicator_id" INT NOT NULL UNIQUE REFERENCES "indicators" ("id") ON DELETE CASCADE
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "strategies" ADD "indicator_id" INT NOT NULL;
        DROP TABLE IF EXISTS "parameters";
        DROP TABLE IF EXISTS "conditions";
        ALTER TABLE "strategies" ADD CONSTRAINT "fk_strategi_indicato_5cea300d" FOREIGN KEY ("indicator_id") REFERENCES "indicators" ("id") ON DELETE CASCADE;"""
