from nextcord.ext import commands
from datetime import datetime
from nextcord import SlashOption
import os
import json
import nextcord

import requests




def agent_name():
    info = requests.get('https://valorant-api.com/v1/agents').json()

    agent_name = {}
    # _["displayName"]


    for _ in info["data"]:
        agent_name[_["displayName"]] = _["displayName"]
    return agent_name
    
    
def info_req():
    info = requests.get('https://valorant-api.com/v1/agents', params={"language": "vi-VN"}).json()
    f = open(os.path.join("json", "val", "agent.json"), "w")
    json.dump(info, f, indent= 4)
    f.close()
    return info
class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @nextcord.slash_command(name="agent", description="Thông tin về Agent của VALORANT")
    
    async def _agent_info(self, inter: nextcord.Interaction, agent = SlashOption(name="agent", description="Tên Agent", choices=agent_name())):
        view = SelectView(agent)
        await inter.response.send_message(embed = self.Embed_Agent(agent), view=view)
        
    @commands.command(name="version")
    async def _version(self, ctx):
        await ctx.send(embed = self.Embed("VALORANT Patch: ", self.version())) 
    
    
    def version(self):
        try:
            info = requests.get("https://valorant-api.com/v1/version").json()
            f = open(os.path.join("json", "val", "version.json"), "w")
            json.dump(info, f, indent= 4)
            f.close()
        except Exception as e:
            print(e)
            info = json.loads(open(os.path.join("json", "val", "version.json"), "r").read())
        finally:
            return info["data"]["version"]
        
    
    
    
    # __ func for doing stuff __
    
   
    
    
    def Embed_Agent(self, agent_name = "Sova"):
        
        try:
            info = info_req()
        except Exception as e:
            print(e)
            info = json.loads(open(os.path.join("json", "val", "agent.json"), "r").read())
        finally:
            for _ in info["data"]:
                if _["displayName"] == str(agent_name):
                    embed = nextcord.Embed(title=_["displayName"],
                                description=_["description"],
                                colour=nextcord.Color.random(),
                                timestamp=datetime.now())

                    embed.set_author(name=_["role"]["displayName"],
                                    icon_url=_["role"]["displayIcon"])

                    embed.set_thumbnail(url=_["displayIcon"])

                    embed.set_footer(text=f"Patch {self.version()}")
                    return embed
            embed = nextcord.Embed(title="ERROR",
                                colour=nextcord.Color.random(),
                                timestamp=datetime.now())   
            return embed
    
    
    
class SelectAgentAblities(nextcord.ui.Select):
    def __init__(self, agent):
        self.agent = agent
        options=[
            nextcord.SelectOption(label="Chiêu thứ 1 (C)",value="1",description=f"Chiêu C của {self.agent}"),
            nextcord.SelectOption(label="Chiêu thứ 2 (Q)",value="2",description=f"Chiêu Q của {self.agent}"),
            nextcord.SelectOption(label="Chiêu thứ 3 (E)",value="3",description=f"Chiêu E của {self.agent}"),
            nextcord.SelectOption(label="Chiêu cuối",value="4",description=f"Chiêu cuối của {self.agent}")
            ]
        super().__init__(placeholder="Kĩ năng",max_values=1,min_values=1,options=options)
    async def callback(self, inter: nextcord.Interaction):
        choice_ = "Ability1"
        if self.values[0] == "1":
            choice_ = "Grenade"
        elif self.values[0] == "2":
            choice_ = "Ability1"
        elif self.values[0] == "3":
            choice_ = "Ability2"
        elif self.values[0] == "4":
            choice_ = "Ultimate"
        try:
            info = info_req()
        except Exception as e:
            print(e)
            info = json.loads(open(os.path.join("json", "val", "agent.json"), "r").read())
        finally:    
            for _ in info["data"]:
                if _["displayName"] == str(self.agent):
                    for ability in _["abilities"]:
                        if ability["slot"] == choice_:
                            embed = nextcord.Embed(title=ability["displayName"],
                                        description=ability["description"],
                                        colour=nextcord.Color.random(),
                                        timestamp=datetime.now())
           
                            embed.set_author(name=_["displayName"],
                                            icon_url=_["displayIcon"])

                            embed.set_thumbnail(url=ability["displayIcon"])
                            await inter.response.send_message(embed=embed, ephemeral=True)

class SelectView(nextcord.ui.View):
    def __init__(self, agent, *, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(SelectAgentAblities(agent))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

def setup(bot):
    bot.add_cog(Valorant(bot))
    