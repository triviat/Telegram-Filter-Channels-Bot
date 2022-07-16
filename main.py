from telethon import TelegramClient, events, functions, types

from config import *

client = TelegramClient('user', api_id, api_hash)
output_channel = 'Filter Channels'
with open('channels.txt', encoding='UTF-8') as f:
    input_channels = (line.strip() for line in f.readlines())


async def create_channel() -> None:
    async for dialog in client.iter_dialogs():
        if dialog.name == output_channel:
            return

    await client(functions.channels.CreateChannelRequest(title=output_channel, about=''))


async def is_text_in_white_list(message: str) -> bool:
    with open('white_list.txt', encoding='UTF-8') as wl_list:
        white_list = [line.strip().lower().split(', ') for line in wl_list.readlines()]

    for line in white_list:
        is_line_in_message = True

        for word in line:
            if word in message:
                continue
            is_line_in_message = False
            break

        if is_line_in_message:
            return True

    return False


async def is_message_valid(message: str) -> bool:
    if await is_text_in_white_list(message.lower()):
        return True
    return False


async def save_message(msg: types.Message) -> None:
    await client.send_message(output_channel, msg)


@client.on(events.NewMessage(input_channels))
async def new_messages_handler(event):
    if await is_message_valid(event.message.to_dict()['message']):
        await save_message(event.message)


if __name__ == '__main__':
    with client:
        client.start()
        client.loop.run_until_complete(create_channel())
        client.run_until_disconnected()
