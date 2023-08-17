from typing import Union

from pydantic import BaseModel

from server.db.models.telegram import TelegramModel


class TelegramDAO(BaseModel):
    """Class for accessing telegram table."""

    async def get_or_create(
        self,
        username: str = None,
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
    ) -> TelegramModel:
        """
        Get the telegram account object, or create it if none exists.

        Args:
            username (str): Telegram user name. Defaults to None.
            first_name (Union[str, None], optional): First name. Defaults to None.
            last_name (Union[str, None], optional): Last name. Defaults to None.
            is_bot (Union[bool, None], optional): Whether the user is bot or not. Defaults to None.
            id (Union[int, None], optional): user id. Defaults to None.
            language_code (Union[str, None], optional): language code. Defaults to None.
            can_join_groups (Union[bool, None], optional): able to join new group or not. Defaults to None.
            can_read_all_group_messages (Union[bool, None], optional): able to read all group messages. Defaults to None.
            supports_inline_queries (Union[bool, None], optional): support inline queries. Defaults to None.
            is_premium (Union[bool, None], optional): is premium user. Defaults to None.
            added_to_attachment_menu (Union[bool, None], optional): added to attachment menu. Defaults to None.

        Returns:
            TelegramModel: telegram object
        """
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

    async def update_or_create(
        self,
        username: str = None,
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
    ) -> TelegramModel:
        return await TelegramModel.update_or_create(
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
