import os
from time import sleep

import aiohttp
from aiotg import Bot

CLEVERBOT = "https://www.cleverbot.com/getreply?key={key}&input={q}"
APERTIUM = 'http://batisteo.eu:2737/translate?markUnknown=no&q={q}&langpair={pair}'
CLEVERBOT_TOKEN = os.environ['CLEVERBOT_TOKEN']

bot = Bot(api_token=os.environ['BOT_TOKEN'])


@bot.command(r"(.+)")
async def babili(chat, match):
    q = match.group(1) if match.group(1) else ''
    in_en = await trans(q, 'epo|eng')
    url = CLEVERBOT.format(key=CLEVERBOT_TOKEN, q=in_en)
    async with aiohttp.get(url) as s:
        response = await s.json()
        out = response["output"]
        await chat.send_chat_action('typing')
        sleep(len(out) / 10)
        in_eo = await trans(out, 'eng|epo')
        await chat.send_text(in_eo)


async def trans(q, pair):
    url = APERTIUM.format(q=q, pair=pair)
    async with aiohttp.get(url) as s:
        response = await s.json()
        return response['responseData']['translatedText']


bot.run()
