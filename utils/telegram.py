import telegram

async def send_message_telegram(token, id, message):
    try:
        telegram_notify = telegram.Bot(token)
        await telegram_notify.send_message(
            chat_id = id, 
            text = message, 
            parse_mode = "Markdown"
        )
    except Exception as ex:
        print(ex)


# asyncio.run(send_message_telegram(token_telegram, id_telegram, message))