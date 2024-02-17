import asyncio, datetime, discord, requests
from dotenv import load_dotenv, dotenv_values

config = dotenv_values("config.env")

intents = discord.Intents.default()
intents.message_content = False
client = discord.Client(intents=intents)
data = ""
day_to_check = ""


@client.event
async def on_ready():
    print('Client Connected')
    await timer_message()


async def timer_message():
    while True:
        global day_to_check
        day_to_check = str(datetime.datetime.today()).split(" ")[0].replace("-", "")
        global data

        if day_to_check != data:
            data = day_to_check
            await send_message()
        else:
            print("Same Data, wait for next check")

        await asyncio.sleep(3600)


async def send_message():
    user = client.get_channel(int(config["CHANNEL_ID"]))
    response, path = await get_pdf()
    paycheck = str(datetime.datetime.today()).split(" ")[0]

    if response:
        await user.send(f"<@{config['DISCORD_ID']}> Cambio Tariffe del {paycheck}", file=discord.File(path))
    else:
        print("File Assente")


async def get_pdf():
    global day_to_check
    path = f'Modificato_{day_to_check}.pdf'
    url = f'https://www.tabaccai.it/images/PDF/{day_to_check}/{path}'
    response = requests.get(url)

    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)

        await asyncio.sleep(10)
        return True, path

    return False, ""


client.run(config["TOKEN"])
