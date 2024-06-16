from nextcord.ext import commands
import nextcord
import os



class App:
    def __init__(self) -> None:
        


        self.bot =  commands.Bot(command_prefix="!", intents=nextcord.Intents.all())


        for fn in os.listdir("./cogs"):
            if fn.endswith(".py"):
                self.bot.load_extension(f"cogs.{fn[:-3]}")
        
        @self.bot.command()
        async def load(ctx, extension):
            self.bot.load_extension(f"cogs.{extension}")
            await ctx.send("Loaded cog !")
        
        @self.bot.command()
        async def unload( ctx, extension):
            self.bot.unload_extension(f"cogs.{extension}")
            await ctx.send("Unloaded cog !")
        
        @self.bot.command()
        async def reload( ctx, extension):
            self.bot.reload_extension(f"cogs.{extension}")
            await ctx.send("Reloaded cog !")
        


        @self.bot.command(name="hi")
        async def SendMessage(ctx):
            await ctx.send("Hello")
    
    
        @self.bot.event
        async def on_ready():
            print(f"Logging in as: {self.bot.user.name}")

    
    
    

if __name__ == "__main__":
    # App().bot.run(os.environ["DISCORD_TOKEN"])
    App().bot.run(open("token.txt", "r").read())




