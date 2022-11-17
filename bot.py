from datetime import date, timedelta
from nextcord.ext import commands
import os
import nextcord
from pymongo import MongoClient
import traceback

bot = commands.Bot()
client = MongoClient(os.getenv('MONGO_URL'))
db = client.cry

@bot.slash_command(description="displays possible commands")
async def help(interaction: nextcord.Interaction):
    embed = nextcord.Embed(description=f"""
━━━━━━━━━━━━━━━
Commands:
**>** **cry**: adds to your cry count
**>** **streak**: shows your current, and highest streak
Use `/help [command]` for more info on each command.
""",
                           title="Help",
                           color=216728)
    await interaction.response.send_message(embed=embed)

@bot.slash_command(description="cry another day")
async def cry(interaction: nextcord.Interaction):
    try:
        if(interaction.user == None):
            await interaction.response.send_message("Caller not found!")
            return

        crier = db.criers.find_one({ "user" : interaction.user.id})
        print(crier)
        today = date.today()
        yesterday = str(today - timedelta(days = 1))
        today = str(today)
        if(crier == None):
            total = 1
            db.criers.insert_one({"user": interaction.user.id, 'last': today, 'total': total})
            await interaction.response.send_message(f"Seems like your new here, your crying streak starts.... Now!")
            return

        if(crier['last'] == today):
            await interaction.response.send_message("You already cried today!")
            return

        if(crier['last'] == yesterday):
            total = crier['total'] + 1
            db.criers.update_one({"user": interaction.user.id}, {'last': today, 'total': total})
            await interaction.response.send_message(f"Your on a roll, youve cried for {total} days in a row!")
            return
        total = 1
        db.criers.update_one({"user": interaction.user.id}, {'last': today, 'total': total})
        await interaction.response.send_message(f"Seems like you lost your streak! New one starts.... Now!")
    except:
        error = traceback.format_exc()
        await interaction.response.send_message(error)

@bot.slash_command(description="check your longest streak")
async def streak(interaction: nextcord.Interaction):
    try:
        if(interaction.user == None):
            await interaction.response.send_message("Caller not found!")
            return
        crier = db.criers.find_one({ "user" : interaction.user.id})
        if(crier == None):
            await interaction.response.send_message("Seems like youve never cried, good shit tbh")
            return
        today = date.today()
        yesterday = str(today - timedelta(days = 1))
        today = str(today)
        if(crier['last'] == yesterday or crier['last'] == today):
            await interaction.response.send_message(f"Your current streak is {crier['total']}")
            return
        await interaction.response.send_message(f"Seems like you lost your streak, but your last one was {crier['total']}")
        return
    except:
        error = traceback.format_exc()
        await interaction.response.send_message(error)

if __name__ == "__main__":
    bot.run(os.getenv('TOKEN'))
