import pytest
from telethon.sync import TelegramClient
from telethon.tl.custom.conversation import Conversation
from telethon.tl.custom.message import Message

from . import TIMEOUT, bot_tag


@pytest.mark.asyncio
async def test_lezioni_cmd(client: TelegramClient):
    """Tests all the possible options in the /lezioni command

    Args:
        client (TelegramClient): client used to simulate the user
    """
    conv: Conversation
    async with client.conversation(bot_tag, timeout=TIMEOUT) as conv:

        await conv.send_message("/lezioni")  # send a command
        resp: Message = await conv.get_response()

        assert resp.text

        buttons = (
            "sm_lezioni_button_anno",
            "lezioni_button_anno_1 anno",
            "sm_lezioni_button_giorno",
            "lezioni_button_giorno_1 giorno",
            "sm_lezioni_button_insegnamento",
        )

        for button in buttons:
            await resp.click(data=button)  # click the button
            resp: Message = await conv.get_edit()

            assert resp.text

        await conv.send_message("nome: programmazione")  # send a message
        resp: Message = await conv.get_response()

        assert resp.text

        await resp.click(data="lezioni_button_search")  # click the "Cerca" button
        resp: Message = await conv.get_edit()

        assert resp.text
