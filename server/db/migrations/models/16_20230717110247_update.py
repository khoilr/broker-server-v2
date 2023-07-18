from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "conditions" ALTER COLUMN "value" TYPE DOUBLE PRECISION USING "value"::DOUBLE PRECISION;
        ALTER TABLE "conditions" ALTER COLUMN "value" TYPE DOUBLE PRECISION USING "value"::DOUBLE PRECISION;
        ALTER TABLE "conditions" ALTER COLUMN "value" TYPE DOUBLE PRECISION USING "value"::DOUBLE PRECISION;
        ALTER TABLE "conditions" ALTER COLUMN "value" TYPE DOUBLE PRECISION USING "value"::DOUBLE PRECISION;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "conditions" ALTER COLUMN "value" TYPE VARCHAR(50) USING "value"::VARCHAR(50);
        ALTER TABLE "conditions" ALTER COLUMN "value" TYPE VARCHAR(50) USING "value"::VARCHAR(50);
        ALTER TABLE "conditions" ALTER COLUMN "value" TYPE VARCHAR(50) USING "value"::VARCHAR(50);
        ALTER TABLE "conditions" ALTER COLUMN "value" TYPE VARCHAR(50) USING "value"::VARCHAR(50);"""
