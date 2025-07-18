import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

questions = [
    "Quel est le nom de ton personnage ?",
    "Quelle est ta classe et spécialisation ?",
    "Quels sont tes jours/horaires de disponibilité ? (La guilde raid généralement le lundi et jeudi de 20h15 à 23h)",
    "Quelle est ton expérience en raid ? (Mythique/Héroïque)",
    "Des précisions à transmettre aux officiers ?"
]

@bot.event
async def on_ready():
    logger.info(f"✅ Connecté en tant que {bot.user}")

@bot.command(name="candidature")
async def candidature(ctx):
    try:
        await ctx.author.send("Salut ! On va commencer ta candidature pour le roster WoW.")
        responses = []

        def check(m):
            return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)

        for question in questions:
            await ctx.author.send(question)
            msg = await bot.wait_for("message", check=check, timeout=120)
            responses.append(msg.content)

        # Connexion à Google Sheets
        scope = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)

        sheet_name = os.getenv("SHEET_NAME")
        tab_name = os.getenv("TAB_NAME")

        sheet = client.open(sheet_name).worksheet(tab_name)
        sheet.append_row([ctx.author.name] + responses)

        await ctx.author.send("✅ Merci ! Ta candidature a bien été envoyée.")
        await ctx.send(f"{ctx.author.mention} a soumis une candidature.")
        logger.info(f"Candidature reçue de {ctx.author.name}: {responses}")

    except Exception as e:
        logger.error(f"❌ Erreur : {e}", exc_info=True)
        await ctx.send(f"{ctx.author.mention} une erreur est survenue. Contacte un officier.")

def run_bot():
    BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    if BOT_TOKEN:
        bot.run(BOT_TOKEN)
    else:
        logger.error("❌ Le token du bot Discord n'est pas défini dans les variables d'environnement.")
