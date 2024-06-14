from nextcord.ext import commands
import nextcord
import json
import os

def open_economy():
    f = open(os.path.join("json", "economy","money.json"), "r")
    info = json.loads(f.read())
    f.close()
    return info
def saving_economy(info):
    f = open(os.path.join("json", "economy","money.json"), "w")
    
    json.dump(info, f, indent=4)
    f.close()

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @nextcord.slash_command(name="cash", description="Số chuối còn lại trong túi của bạn")
    async def cash_(self, inter: nextcord.Interaction):
        info = Currency(str(inter.user.id))
        await inter.response.send_message(f"Số chuối trong túi của bạn hiện tại đang có là **__{(info.get_money()):,}__** :banana: ")

    @nextcord.slash_command(name="transfer", description="Chuyển chuối cho ai đó")
    async def transfer(self, inter: nextcord.Interaction, id_sent: nextcord.User, creds : int):
        info = Currency(str(inter.user.id))
        isSuccess = info.transfer(id_sent.id, creds)
        if isSuccess == True:
            await inter.response.send_message(f"Đã chuyển **__{creds:,}__** :banana: cho {id_sent.mention}")
        elif isSuccess != True:
            await inter.response.send_message(f"Lỗi hệ thống: {isSuccess["error.Economy.Transfer"]["message"]}")
            



class Currency:
    def __init__(self, id_mem):
        self.id = id_mem
        self.data = open_economy()
    def is_signed(self, id_mem):
        if str(id_mem) not in self.data["data"]:
            self.data["data"][str(id_mem)] = {}
            self.data["data"][str(id_mem)]["money"] = 0
            saving_economy(self.data)
            return True
        return False
    def get_money(self):
        self.is_signed(self.id)
        return self.data["data"][str(self.id)]["money"]
        


    def transfer(self, id_sent, creds:int):
        self.is_signed(self.id)
        self.is_signed(id_sent)
        if int(self.data["data"][str(self.id)]["money"]) - int(creds) < 0:
            return {"error.Economy.Transfer": {"type": 1, "message":"Không đủ tiền để chuyển."}}
        elif int(creds) <= 0:
            return {"error.Economy.Transfer": {"type": 2, "message":"Số tiền phải lớn hơn 0."}}

        
        your_creds = int(self.data["data"][str(self.id)]["money"])
        their_creds = int(self.data["data"][str(id_sent)]["money"])
        
        your_creds -=int(creds)
        their_creds +=int(creds)
        
        self.data["data"][str(self.id)]["money"] = your_creds
        self.data["data"][str(id_sent)]["money"] = their_creds
        saving_economy(self.data)
        return True
            

    def game_bet(self, creds: int):
        self.is_signed(self.id)
        if int(self.data["data"][str(self.id)]["money"]) - int(creds) < 0:
            return {"error.Economy.Game_Bet": {"type": 1, "message":"Không đủ tiền để chơi"}}
        elif int(creds) <= 0:
            return {"error.Economy.Game_Bet": {"type": 2, "message":"Số tiền phải lớn hơn 0."}}
        
    
    





def setup(bot):
    bot.add_cog(Economy(bot))
    