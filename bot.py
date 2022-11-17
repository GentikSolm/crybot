from nextcord.ext import commands
import os
import nextcord
from pymongo import MongoClient

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

if __name__ == "__main__":
    bot.run(os.getenv('TOKEN'))
