from typing import Union

from pydantic import BaseModel

from server.db.models.telegram import TelegramModel


class TelegramDAO(BaseModel):
    async def get_or_create(
        self,
        username: str,
        first_name: Union[str, None] = None,
        last_name: Union[str, None] = None,
        is_bot: Union[bool, None] = None,
        id: Union[int, None] = None,
        language_code: Union[str, None] = None,
        can_join_groups: Union[bool, None] = None,
        can_read_all_group_messages: Union[bool, None] = None,
        supports_inline_queries: Union[bool, None] = None,
        is_premium: Union[bool, None] = None,
        added_to_attachment_menu: Union[bool, None] = None,
    ):
        return await TelegramModel.get_or_create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_bot=is_bot,
            id=id,
            language_code=language_code,
            can_join_groups=can_join_groups,
            can_read_all_group_messages=can_read_all_group_messages,
            supports_inline_queries=supports_inline_queries,
            is_premium=is_premium,
            added_to_attachment_menu=added_to_attachment_menu,
        )
