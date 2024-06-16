from nextcord.ext import commands
from nextcord import SlashOption
import nextcord
import json
import os
from datetime import datetime
import random
import asyncio


def open_economy():
    f = open(os.path.join("json", "economy","money.json"), "r")
    info = json.loads(f.read())
    f.close()
    return info
def saving_economy(info):
    f = open(os.path.join("json", "economy","money.json"), "w")
    
    json.dump(info, f, indent=4)
    f.close()

def open_code():
    f = open(os.path.join("json", "redeem_code","redeem.json"), "r")
    info = json.loads(f.read())
    f.close()
    return info
def saving_code(info):
    f = open(os.path.join("json", "redeem_code","redeem.json"), "w")
    
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
            
    @nextcord.slash_command(name="bet", description="Cược đi chờ chi ...")
    async def bet(self, inter: nextcord.Interaction, creds:int, mat_dong_xu = SlashOption(name="mat_dong_xu", description="Mặt đồng xu", choices={
        "Mặt ngửa": "0",
        "Mặt sấp": "1"
    })):
        info = Currency(str(inter.user.id))
        mat_dx = "mặt ngửa" if mat_dong_xu == "0" else "mặt sấp"
        if str(info.id) != "748439531761434676":
            if int(creds) <= 100000:
                msg = await inter.response.send_message(f"**Bạn cược __{creds:,}__ :banana: cho __{mat_dx}__**")
                await asyncio.sleep(3)
                isWin = info.game_bet(creds, int(mat_dong_xu))
                if isWin == True:
                    await msg.edit(f"**Bạn thắng __{int(creds*2):,}__ :banana: !!!**")
                elif isWin == False:
                    await msg.edit(f"**Bạn thua __{int(creds):,}__ :banana: :(**")
                else:
                    await msg.edit(f"Lỗi hệ thống: {isWin["error.Economy.Game_Bet"]["message"]}")
            else:
                await inter.response.send_message(f"**No, 100k là đủ rồi em ơi.**")
        else:
            msg = await inter.response.send_message(f"**Bạn cược __{creds:,}__ :banana: cho __{mat_dx}__**")
            await asyncio.sleep(3)
            isWin = info.game_bet(creds, int(mat_dong_xu))
            if isWin == True:
                await msg.edit(f"**Bạn thắng __{int(creds*2):,}__ :banana: !!!**")
            elif isWin == False:
                await msg.edit(f"**Bạn thua __{int(creds):,}__ :banana: :(**")
            else:
                await msg.edit(f"Lỗi hệ thống: {isWin["error.Economy.Game_Bet"]["message"]}")
    @nextcord.slash_command(name="redeem", description="Redeem code")
    async def redeem(self, inter: nextcord.Interaction, code: str):
        info = Currency(str(inter.user.id))
        isSuccess = info.redeem_code(code)
        if isSuccess== True:
            await inter.response.send_message(f"**Redeem code thành công**")
        else:
            await inter.response.send_message(f"**Lỗi hệ thống: {isSuccess['error.Economy.Redeem_Code']['message']}**", ephemeral=True)
            
    @nextcord.slash_command(name="add_code", description="Tạo code mới")
    async def add_code(self, inter: nextcord.Interaction, code: str, creds: int):
        info = Currency(str(inter.user.id))
        isSuccess = info.add_code(code,creds)
        if isSuccess == True:
            await inter.response.send_message(f"**Tạo code thành công**", ephemeral=True)
        else:
            await inter.response.send_message(f"**Lỗi hệ thống: {isSuccess['error.Economy.Redeem_Code']['message']}**", ephemeral=True)
    
    @nextcord.slash_command(name="deactive_code", description="Disable code")
    async def deactive_code(self, inter: nextcord.Interaction, code: str):
        info = Currency(str(inter.user.id))
        isSuccess = info.deactive_code(code)
        if isSuccess == True:
            await inter.response.send_message(f"**Disable code thành công**", ephemeral=True)
        else:
            await inter.response.send_message(f"**Lỗi hệ thống: {isSuccess['error.Economy.Redeem_Code']['message']}**", ephemeral=True)
    @nextcord.slash_command(name="active_code", description="Enable code")
    async def deactive_code(self, inter: nextcord.Interaction, code: str):
        info = Currency(str(inter.user.id))
        isSuccess = info.active_code(code)
        if isSuccess == True:
            await inter.response.send_message(f"**Enable code thành công**", ephemeral=True)
        else:
            await inter.response.send_message(f"**Lỗi hệ thống: {isSuccess['error.Economy.Redeem_Code']['message']}**", ephemeral=True)

    @nextcord.slash_command(name="dashboard", description="BXH số lượng chuối (Trong top 10)")
    async def dashboard(self, inter:nextcord.Interaction):
        info = open_economy()["data"]
        sorted_data = sorted(info.items(), key=lambda item: item[1]["money"], reverse=True)
        embed = nextcord.Embed(title="Dashboard", description="BXH số chuối của The Zoo", color = nextcord.Color.random(), timestamp=datetime.now())
        count = 1
        for user_id, info in sorted_data:
            if count > 10:
                break
            if user_id != "748439531761434676":
                if info['money'] < 0:
                    embed.add_field(name=f"#{count}", value=f"<@{user_id}>:  Banned", inline=False)
                    count +=1
                else:
                    embed.add_field(name=f"#{count}", value=f"<@{user_id}>:  {int(info['money']):,}", inline=False)
                    count +=1
        await inter.response.send_message(embed=embed)
        
        



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
            

    def game_bet(self, creds: int, mat_dong_xu: int):
        self.is_signed(self.id)
        if str(self.id) != "748439531761434676":
            if int(creds) <= 0:
                return {"error.Economy.Game_Bet": {"type": 2, "message":"Số tiền phải lớn hơn 0."}}
            elif int(self.data["data"][str(self.id)]["money"]) - int(creds) < 0:
                return {"error.Economy.Game_Bet": {"type": 1, "message":"Không đủ tiền để chơi"}}
            
            elif int(creds) > 100000:
                return {"error.Economy.Game_Bet": {"type": 3, "message":"Số tiền phải nhỏ hơn 100,000"}}
            
            num = random.randint(0,1)
            your_creds = int(self.data["data"][str(self.id)]["money"]) - int(creds)
            if num == mat_dong_xu:
                
                your_creds += int(creds*2)

                self.data["data"][str(self.id)]["money"] = int(your_creds)
                saving_economy(self.data)
                return True
            else:
                self.data["data"][str(self.id)]["money"] = int(your_creds)
                saving_economy(self.data)
                return False
        else:
            your_creds = int(self.data["data"][str(self.id)]["money"]) - int(creds)

                
            your_creds += int(creds*2)

            self.data["data"][str(self.id)]["money"] = int(your_creds)
            saving_economy(self.data)
            return True
            
            
    def redeem_code(self, code:str):
        self.is_signed(self.id)
        code_data = open_code()
        eco_data = open_economy()
        for _ in range(len(code_data["data"]["code"])):
            if (code_data["data"]["code"][_]["codeName"] == code) and (code_data["data"]["code"][_]["isActive"] and str(self.id) not in code_data["data"]["code"][_]["redeemtionPlayer"]) :
                your_money = int(eco_data["data"][str(self.id)]["money"])
                your_money += int(code_data["data"]["code"][_]["creds"])
                eco_data["data"][str(self.id)]["money"] = your_money
                code_data["data"]["code"][_]["redeemtionPlayer"].append(str(self.id))
                
                saving_economy(eco_data)
                saving_code(code_data)
                return True 
        return {"error.Economy.Redeem_Code": {"type": 1, "message":"Mã code không tồn tại hoặc bạn đã sử dụng."}}
    
    def add_code(self, code:str ,creds:int):
        if str(self.id) == "748439531761434676":
            self.is_signed(self.id)
            code_data = open_code()
            for _ in range(len(code_data["data"]["code"])):
                if code_data["data"]["code"][_]["codeName"] == code:
                    return {"error.Economy.Add_Code": {"type": 1, "message":"Mã code đã tồn tại."}}
            code_data["data"]["code"].append({"codeName": code, "isActive": True, "creds": creds,"redeemtionPlayer": []})
            saving_code(code_data)
            return True
        else:
            return {"error.Economy.Add_Code": {"type": 1, "message":"Bạn không có quyền."}}
    def deactive_code(self, code):
        if str(self.id) == "748439531761434676":
            self.is_signed(self.id)
            code_data = open_code()
            for _ in range(len(code_data["data"]["code"])):
                if code_data["data"]["code"][_]["codeName"] == code:
                    code_data["data"]["code"][_]["isActive"] = False
                    saving_code(code_data)
                    return True
            return {"error.Economy.Deactive_Code": {"type": 1, "message":"Mã code không tồn tại hoặc đã được sử dụng."}}
        else:
            return {"error.Economy.Deactive_Code": {"type": 1, "message":"Bạn không có quyền."}}
    
    def active_code(self, code):
        if str(self.id) == "748439531761434676":
            self.is_signed(self.id)
            code_data = open_code()
            for _ in range(len(code_data["data"]["code"])):
                if code_data["data"]["code"][_]["codeName"] == code:
                    code_data["data"]["code"][_]["isActive"] = True
                    saving_code(code_data)
                    return True
            return {"error.Economy.Active_Code": {"type": 1, "message":"Mã code không tồn tại hoặc đã được sử dụng."}}
        else:
            return {"error.Economy.Active_Code": {"type": 1, "message":"Bạn không có quyền."}}

def setup(bot):
    bot.add_cog(Economy(bot))
    