import pytest
from telethon.sync import TelegramClient
from telethon.tl.custom.conversation import Conversation
from telethon.tl.custom.message import Message

from . import TIMEOUT, bot_tag


@pytest.mark.asyncio
async def test_help_buttons(client: TelegramClient):
    """Tests all the md buttons in the help command

    Args:
        client (TelegramClient): client used to simulate the user
    """
    conv: Conversation
    async with client.conversation(bot_tag, timeout=TIMEOUT) as conv:
        buttons = (
            "md_esami_link",
            "md_lezioni_link",
            "md_professori",
            "md_biblioteca",
            "md_gruppi",
            "md_cus",
            "md_cloud",
            "md_sdidattica",
            "md_studenti",
            "md_cea",
            "md_ersu",
            "md_ufficioersu",
            "md_urp",
            "md_drive",
            "md_gitlab",
            "md_opismanager",
            "md_contributors",
            "md_help",
            "exit_cmd",
        )

        for button in buttons:
            await conv.send_message("/help")  # send a command
            resp: Message = await conv.get_response()

            assert resp.text

            await resp.click(data=button)  # click the inline button
            resp: Message = await conv.get_edit()

            assert resp.text
