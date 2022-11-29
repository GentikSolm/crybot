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
**>** **leaderboard**: lists hot criers in your area!
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
        today = date.today()
        yesterday = str(today - timedelta(days = 1))
        today = str(today)
        if(crier == None):
            total = 1
            db.criers.insert_one({"user": interaction.user.id, 'last': today, 'total': total, 'streak': 1})
            await interaction.response.send_message(f"Seems like you're new here, your crying streak starts.... Now!")
            return

        if(crier.get('last') == today):
            db.criers.update_one({"user": interaction.user.id}, {'$set': {'total': crier['total'] + 1} })
            await interaction.response.send_message("Rough day huh?")
            return

        if(crier.get('last') == yesterday):
            db.criers.update_one({"user": interaction.user.id}, {'$set': {
                'last': today,
                'total': crier['total'] + 1,
                'streak': crier['streak'] + 1
            }})
            await interaction.response.send_message(f"You're on a roll, you have cried for {crier['streak']} days in a row!")
            return
        db.criers.update_one({"user": interaction.user.id}, {'$set': {'last': today, 'streak': 1, 'longest': crier.get('streak')} })
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
            await interaction.response.send_message(f"Your current streak is {crier['streak']}, and you have cried a total of {crier.get('total')} times.")
            return
        longest = crier.get('longest')
        if(longest == None):
            await interaction.response.send_message(f"Seems like you lost your streak, but you have cried a total of {crier.get('total')}")
            return
        await interaction.response.send_message(f"Seems like you lost your streak, but your longest one was {longest}, and you have cried a total of {crier.get('total')} times.")
        return
    except:
        error = traceback.format_exc()
        await interaction.response.send_message(error)


@bot.slash_command(description="view hot single criers in your area")
async def leaderboard(interaction: nextcord.Interaction):
    try:
        criers = db.criers.find({"user"}, sort={'streak': 1}, limit=10)
        leaderboard = """
━━━━━━━━━━━━━━━
"""
        for index, crier in enumerate(criers):
            leaderboard += f"**{index}. {crier.get('user')}: {crier.get('streak')}**\n"
        embed = nextcord.Embed(description=leaderboard, title='Leaderboard', color=216728)
        await interaction.response.send_message(embed=embed)
        return
    except:
        error = traceback.format_exc()
        await interaction.response.send_message(error)

if __name__ == "__main__":
    bot.run(os.getenv('TOKEN'))
