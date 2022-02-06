import discord
from discord.ext import commands,tasks
from discord.commands import slash_command, Option
from discord.ui import Button, View
from datetime import *
from scrim import Scrim
import asyncio

botID = "" #Removed for privacy
guilds = [] #Removed for privacy

team_list = ["Blue","Gold"] # Can set this with database stuff perhaps

bot = commands.Bot(command_prefix="%")

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    

class EventDropDownMenu(discord.ui.View):
    def __init__(self, timeout, author:discord.User):
        super().__init__(timeout=timeout)
        self.done = False
        self.value = None
        self.author = author

    @discord.ui.select(
        placeholder="Select from list",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="League", description="View League Scheduling Options"),
            discord.SelectOption(label="Tournament", description="View Tournament Scheduling Options"),
            discord.SelectOption(label="Scrim", description="View Scrim Scheduling Options")
        ])
    async def callback(self, select, interaction: discord.Interaction): 
        if self.author != interaction.user:
            await interaction.response.send_message("Hey! This isn't your interaction!",ephemeral=True)
        
        if not self.done and self.author == interaction.user:
            self.value = select.values[0]
            self.done = True
            self.stop()

class LeagueDropdownMenu(discord.ui.View):
    def __init__(self, timeout, author:discord.User):
        super().__init__(timeout=timeout)
        self.done = False
        self.value = None
        self.author = author

    @discord.ui.select(
        placeholder="League Options",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="Add a league"),
            discord.SelectOption(label="Get league info"),
            discord.SelectOption(label="Update league")
        ])
    async def callback(self, select, interaction: discord.Interaction):
        if self.author != interaction.user:
            await interaction.response.send_message("Hey! This isn't your interaction!",ephemeral=True)
        
        if not self.done:
            self.value = select.values[0]
            self.done = True
            self.stop()

class TournamentDropdownMenu(discord.ui.View):
    def __init__(self, timeout, author:discord.User):
        super().__init__(timeout=timeout)
        self.done = False
        self.value = None
        self.author = author

    @discord.ui.select(
        placeholder="Tournament Options",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="Add a tournament"),
            discord.SelectOption(label="Get tournament info"),
            discord.SelectOption(label="Update tournament")
        ])
    async def callback(self, select, interaction: discord.Interaction):
        if self.author != interaction.user:
            await interaction.response.send_message("Hey! This isn't your interaction!",ephemeral=True)
        
        if not self.done:
            self.value = select.values[0]
            self.done = True
            self.stop()

class ScrimDropdownMenu(discord.ui.View):
    def __init__(self, timeout, author:discord.User):
        super().__init__(timeout=timeout)
        self.done = False
        self.value = None
        self.author = author

    @discord.ui.select(
        placeholder="Scrim Options",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="Add a scrim"),
            discord.SelectOption(label="Get scrim info"),
            discord.SelectOption(label="Update scrim")
        ])
    async def callback(self, select, interaction: discord.Interaction):
        if self.author != interaction.user:
            await interaction.response.send_message("Hey! This isn't your interaction!",ephemeral=True)
        
        if not self.done:
            self.value = select.values[0]
            self.done = True
            self.stop()

class ScrimButton(discord.ui.View):

    def __init__(self,ctx):
        super().__init__(timeout=60.0)
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label="Update Opponent",style=discord.ButtonStyle.blurple)
    async def opponent_callback(self, button, interaction):
        self.value = "opponent"
        for button1 in self.children:
            button1.style = discord.ButtonStyle.secondary
            button1.disabled = True
        button.style = discord.ButtonStyle.success
        button.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.button(label="Update Date",style=discord.ButtonStyle.blurple)
    async def date_callback(self, button, interaction):
        self.value = "date"
        for button1 in self.children:
            button1.style = discord.ButtonStyle.secondary
            button1.disabled = True
        button.style = discord.ButtonStyle.success
        button.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.button(label="Delete Scrim",style=discord.ButtonStyle.danger)
    async def delete_callback(self, button, interaction):
        self.value = "delete"
        for button1 in self.children:
            button1.style = discord.ButtonStyle.secondary
            button1.disabled = True
        button.style = discord.ButtonStyle.success
        button.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()

class DeleteConfirm(discord.ui.View):
    def __init__(self,ctx):
        super().__init__(timeout=60.0)
        self.ctx = ctx
        self.value = None
    
    @discord.ui.button(label="Confirm",style=discord.ButtonStyle.success)
    async def confirm_callback(self, button, interaction):
        self.value = "confirm"
        for x in self.children:
            x.style = discord.ButtonStyle.secondary
            x.disabled = True
        button.style = discord.ButtonStyle.success
        button.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.button(label="Cancel",style=discord.ButtonStyle.danger)
    async def cancel_callback(self, button, interaction):
        self.value = "cancel"
        for x in self.children:
            x.style = discord.ButtonStyle.secondary
            x.disabled = True
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await self.ctx.send("Cancelled.")
        self.stop()



@bot.slash_command(
    name="schedule",
    description="Scheduling menu",
    guild_ids=guilds
)
async def schedule(
    ctx: discord.ApplicationContext,
    team: Option(str, "What team do you want to access?", choices=team_list)
):
    now = datetime.now()
    color = ""
    if team == "Blue":
        color = discord.Color.blue()
    elif team == "Gold":
        color = discord.Color.gold()
    author = ctx.author
    menu = EventDropDownMenu(timeout=60.0,author=author)
    await ctx.respond(f"You chose {team}. Choose what event you want to access",view=menu)
    await menu.wait()
    #Interaction start
    if menu.value is None:
        await ctx.send("Interaction timed out. Please restart")
    elif menu.value == "League":
        view = LeagueDropdownMenu(timeout=15.0,author=author)
        await ctx.send("League options",view=view)
        await view.wait()

        if view.value is None:
            await ctx.send("Interaction timed out. Please restart")
        elif view.value =="Add a league":
            await ctx.send("Still working on this!")
        elif view.value =="Get league info":
            await ctx.send("Still working on this!")
        elif view.value =="Update league":
            await ctx.send("Still working on this!")
    elif menu.value == "Tournament":
        view = TournamentDropdownMenu(timeout=15.0,author=author)
        await ctx.send("Tournament options",view=view)
        await view.wait()

        if view.value is None:
            await ctx.send("Interaction timed out. Please restart")
        elif view.value =="Add a tournament":
            await ctx.send("Still working on this!")
        elif view.value =="Get tournament info":
            await ctx.send("Still working on this!")
        elif view.value =="Update tournament":
            await ctx.send("Still working on this!")
    elif menu.value == "Scrim":
        view = ScrimDropdownMenu(timeout=60.0,author=author)
        await ctx.send("Choose from scrim options",view=view)
        await view.wait()
        if view.value is None:
            await ctx.send("Interaction timed out. Please restart")
        elif view.value =="Add a scrim":
            await ctx.send("Sent dm with further instructions")
            dm = await bot.create_dm(author)
            await dm.send("**__STEP 1__**")
            await dm.send("What is the scrim team's name?")
            def check(m):
                return m.content is not None and m.author == author
            try:
                opponent = await bot.wait_for("message",timeout=60.0,check=check)
            except asyncio.TimeoutError:
                await dm.send("No response. Stopping interaction.")
            else:
                await dm.send("**__STEP 2__**")
            
            def check(m):
                try:
                    datetime.strptime(m.content,"%d/%m/%y %I:%M %p")
                except ValueError:
                    return False
                else:
                    return True
            try:
                await dm.send("Enter the date info for the scrim. Format should be ```mm/dd/yy hh:mm PM/AM``` (ex: 05/12/22 07:00 PM)")
                event_date = await bot.wait_for("message",timeout=60.0,check=check)
            except asyncio.TimeoutError:
                await dm.send("Seems like you need more time to think this through. It's ok! I'll be here for ya next time :D")
            else:
                event = Scrim(opponent.content,datetime.strptime(event_date.content,"%m/%d/%y %I:%M %p"),team)
                event.confirm_entry()
                await dm.send("Scrim added!")
        elif view.value =="Get scrim info":
            now = now.strftime("%#d %B, %Y, %#I:%M %p")
            scrims = Scrim.get_scrims(team=team)
            if scrims is not None:
                embed = discord.Embed(title=f"__Upcoming scrims for SJSU {team}__",color=color)
                for x in scrims:
                    embed.add_field(name=f"Scrim vs {x[0]}",value=f"**Date:** {x[1]}\n**Time:** {x[2]}\n\n",inline=False)
                embed.set_footer(text=f"Updated as of {now}")
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"There are no scrims at the moment for SJSU {team}!")
        elif view.value =="Update scrim":
            now = datetime.now().strftime("%#d %B, %Y, %#I:%M %p")
            scrims = Scrim.get_scrims(team=team)
            if scrims is not None:
                await ctx.send("Sent dm")
                dm = await bot.create_dm(author)
                embed = discord.Embed(title=f"__Scrim List for SJSU {team}__",color=color)
                count = 1
                scrim_list = []
                for x in scrims:
                    scrim_list.append([team,x[0],x[1],x[2]])
                    embed.add_field(name=f"`[#{count}]` Scrim vs {x[0]}",value=f"**Date:** {x[1]}\n**Time:** {x[2]}\n\n",inline=False)
                    count+=1
                embed.set_footer(text=f"Updated as of {now}")
                button = ScrimButton(dm)
                await dm.send(embed=embed,view=button)
                await button.wait()
                if button.value is None:
                    await dm.send("Interaction timed out. Please start again.")
                elif button.value == "opponent":
                    await dm.send("Which scrim would you like to edit opponent's name? Enter number:")
                    def check(m):
                        return m.content is not None and m.content.isnumeric() and (int(m.content) <= len(scrim_list)) and (int(m.content) > 0)
                    try:
                        num = await bot.wait_for("message",timeout=60.0,check=check)
                    except asyncio.TimeoutError:
                        await dm.send("No response recorded in proper format. Ending interaction.")
                    else:
                        await dm.send(f"What would you like to update opponent `{scrim_list[int(num.content)-1][1]}` to?")
                        def check(m):
                            return m.content is not None
                        try:
                            name = await bot.wait_for("message",timeout=60.0,check=check)
                        except asyncio.TimeoutError:
                            await dm.send("No response recorded in proper format. Ending interaction.")
                        else:
                            Scrim.update_opponent(team,scrim_list[int(num.content)-1][1],name.content)
                            await dm.send(f"Updated opponent's name to {name.content}")
                elif button.value == "date":
                    await dm.send("For which scrim would you like to change the date? Enter number:")
                    def check(m):
                        return m.content is not None and m.content.isnumeric() and (int(m.content) <= len(scrim_list)) and (int(m.content) > 0)
                    try:
                        num = await bot.wait_for("message",timeout=60.0,check=check)
                    except asyncio.TimeoutError:
                        await dm.send("No response recorded in proper format. Ending interaction.")
                    else:
                        await dm.send(f"What would you like to update date `{scrim_list[int(num.content)-1][2]}` to?")
                        await dm.send("Make sure to follow the format ```mm/dd/yy hh:mm PM/AM``` (ex: 05/12/22 07:00 PM)")
                        def check(m):
                            try:
                                datetime.strptime(m.content,"%d/%m/%y %I:%M %p")
                            except ValueError:
                                return False
                            else:
                                return True
                        try:
                            new_date = await bot.wait_for("message",timeout=60.0,check=check)
                        except asyncio.TimeoutError:
                            await dm.send("No response recorded in proper format. Ending interaction.")
                        else:
                            raw_date = datetime.strptime(new_date.content,"%m/%d/%y %I:%M %p")
                            new_day = raw_date.strftime("%#d %B, %Y")
                            new_time = raw_date.strftime("%#I:%M %p")
                            Scrim.update_date(team,scrim_list[int(num.content)-1][2],raw_date)
                            await dm.send(f"Scrim date updated to {new_day} at {new_time}")
                elif button.value == "delete":
                    await dm.send("Which scrim would you like to delete? Enter scrim number:")
                    def check(m):
                        return m.content is not None and m.content.isnumeric() and (int(m.content) <= len(scrim_list)) and (int(m.content) > 0)
                    try:
                        num = await bot.wait_for("message",timeout=60.0,check=check)
                    except asyncio.TimeoutError:
                        await dm.send("No response recorded in proper format. Ending interaction.")
                    else:
                        embed = discord.Embed(title="Delete scrim?", color=color)
                        embed.add_field(name=f"**Opponent:** {scrim_list[int(num.content)-1][1]}",value=f"**Date:** {scrim_list[int(num.content)-1][2]}\n**Time:** {scrim_list[int(num.content)-1][3]}")
                        button = DeleteConfirm(dm)
                        await dm.send(embed=embed,view=button)
                        await button.wait()
                        if button.value is None:
                            await dm.send("Interaction timed out. Please start again.")
                        elif button.value == "confirm":
                            Scrim.delete_scrim(team,scrim_list[int(num.content)-1][1],scrim_list[int(num.content)-1][2])
                            await dm.send("Scrim deleted!")
                        elif button.value == "cancel":
                            await dm.send("Cancelled.")
                else:
                    await ctx.send("No scrims exist!")


from config import TOKEN
bot.run(TOKEN)
