import discord
import requests
import re
import time
from discord.ext import commands
from bs4 import BeautifulSoup

TOKEN = ""
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True


def extract_data(text):
    pattern = r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}, \d{4} \d{1,2}:\d{2} [APM]{2}\b"
    match = re.search(pattern, text)
    return match.group(0) if match else ""


def format_loadout_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        loadouts_group = soup.find("div", class_="loadouts-list__group")
        item_box = loadouts_group.find_all("div", class_="wrap-card__content")

        messages = []
        for item in item_box:
            item_name = item.find("div", class_="gun-badge__text").get_text(strip=True)
            item_type = (
                item.find("div", class_="expand-card__el loadout-card__type")
                .get_text(strip=True)
                .replace("Warzone", "")
                .strip()
            )
            item_date = (
                item.find("div", class_="expand-card__author")
                .get_text(strip=True)
                .strip()
            )
            attachments = item.find_all("div", class_="attachment-card")

            message = f"item: {item_name}\ntipo: {item_type}\ndata: {extract_data(item_date)}\nloudout:\n"
            message += "\n".join(
                f"    - {attachment.find('span').get_text(strip=True)}: {attachment.find('div', class_='attachment-card-content__name').div.get_text(strip=True)}"
                for attachment in attachments
            )
            messages.append(message)

        return messages

    except requests.RequestException as e:
        return [f"Error fetching data from {url}: {e}"]


bot = commands.Bot(command_prefix="y!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name="y!help")
    )


bot.remove_command('help')
@bot.command(name='help')
async def custom_help(ctx):
    help_message = "Comandos disponíveis: \n"
    help_message += "---> y!meta: pega o meta do warzone cupinxa \n"
    await ctx.send(f"```{help_message}```")

@bot.command(name="meta")
async def meta(ctx):
    async with ctx.typing():
        loadout_messages = format_loadout_data("https://wzhub.gg/loadouts")
        for answer in loadout_messages:
            time.sleep(1)
            await ctx.send(f"```{answer}```")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)


bot.run(TOKEN)
