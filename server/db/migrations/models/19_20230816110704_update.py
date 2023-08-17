from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "telegrams" ALTER COLUMN "id" TYPE VARCHAR(200) USING "id"::VARCHAR(200);
        ALTER TABLE "telegrams" ALTER COLUMN "id" TYPE VARCHAR(200) USING "id"::VARCHAR(200);
        ALTER TABLE "telegrams" ALTER COLUMN "id" TYPE VARCHAR(200) USING "id"::VARCHAR(200);
        ALTER TABLE "telegrams" ALTER COLUMN "id" TYPE VARCHAR(200) USING "id"::VARCHAR(200);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "telegrams" ALTER COLUMN "id" TYPE INT USING "id"::INT;
        ALTER TABLE "telegrams" ALTER COLUMN "id" TYPE INT USING "id"::INT;
        ALTER TABLE "telegrams" ALTER COLUMN "id" TYPE INT USING "id"::INT;
        ALTER TABLE "telegrams" ALTER COLUMN "id" TYPE INT USING "id"::INT;"""
