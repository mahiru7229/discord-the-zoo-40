from nextcord.ext import commands
from datetime import datetime
from nextcord import SlashOption
from cogs.economy import Currency
import nextcord
import os
import json

def open_bet():
    f = open(os.path.join("json", "bet","bet.json"), "r")
    info = json.loads(f.read())
    f.close()
    return info

def saving_bet(info):
    f = open(os.path.join("json", "bet","bet.json"), "w")
    
    json.dump(info, f, indent=4)
    f.close()

def open_economy():
    f = open(os.path.join("json", "economy","money.json"), "r")
    info = json.loads(f.read())
    f.close()
    return info
def saving_economy(info):
    f = open(os.path.join("json", "economy","money.json"), "w")
    
    json.dump(info, f, indent=4)
    f.close()


def open_bet_database():
    f = open(os.path.join("json", "bet","bet_data.json"), "r")
    info = json.loads(f.read())
    f.close()
    return info

def saving_bet_database(info):
    f = open(os.path.join("json", "bet","bet_data.json"), "w")
    
    json.dump(info, f, indent=4)
    f.close()

def is_match_signed(match_id:int):
    data_ = open_bet_database()
    ok = False
    for i in range(len(data_["data"]["bet_info"])):
        if match_id == data_["data"]["bet_info"][i]["id"] :
            ok = True
            break
    if ok == False:
        data_["data"]["bet_info"].append({
                "id": match_id,
                "team1":[],
                "draw": [],
                "team2": [],
                "canBet" : True,
                "betPlayer":[]
            })
    
    saving_bet_database(data_)




class Bet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.info = open_bet()
        
        
    @commands.command(name="curid")
    async def curid(self, ctx):
        await ctx.send(self.info["data"]["count"])
    
    
    
    @nextcord.slash_command(name="create_match", description="Tạo thông tin trận đấu")
    async def create_match(self, inter:nextcord.Interaction,tournament_name:str, round:str , time:str, team1_name:str, team2_name:str, bet:str):
        self.info = open_bet()
        if str(inter.user.id) == "748439531761434676":
            time_ = datetime.strptime(time, "%H:%M %d-%m-%Y")
            match_info = {
                "id" : self.info["data"]["count"],
                "tournamentName" : tournament_name,
                "round" : round,
                "time" : time_.timestamp(),
                "team1" : team1_name,
                "team2" : team2_name,
                "bet" : bet.split(","),
                "team1_score" : 0,
                "team2_score" : 0,
                "wins": 0,
                "finished" : 0
            }
            
            
            #0 =  hoa, 1 = team 1 thang, 2 = team 2 thang
            
            
            self.info["data"]["matches"].append(match_info)
            self.info["data"]["count"] +=1
            await inter.response.send_message("**Đã tạo thông tin trận đấu !**", ephemeral=True)
        else:
            await inter.response.send_message("**Bạn không có quyền để làm việc này !**", ephemeral=True)
        saving_bet(self.info)
    @nextcord.slash_command(name="edit_match", description="Sửa thông tin trận đấu")   
    async def edit_match(self, inter:nextcord.Interaction,id:int,tournament_name:str, round:str , time:str, team1_name:str, team2_name:str, bet:str, team1_score:int, team2_score:int, win:int, finished: int):
        self.info = open_bet()
        if str(inter.user.id) == "748439531761434676":
            for _ in range(len(self.info["data"]["matches"])):
                if self.info["data"]["matches"][_]["id"] == id:
                    temp = self.info["data"]["matches"][_].copy()
                    self.info["data"]["matches"][_] = {
                        "id" : temp["id"],
                        "tournamentName" : tournament_name if tournament_name != "-1" else temp["tournamentName"],
                        "round" : round if round != "-1" else temp["round"],
                        "time" : datetime.strptime(time, "%Y-%m-%d %H:%M").timestamp() if time != "-1" else temp["time"],
                        "team1" : team1_name if team1_name != "-1" else temp["team1"],
                        "team2" : team2_name if team2_name != "-1" else temp["team2"],
                        "bet" : bet.split(",") if bet != "-1" else temp["bet"],
                        "team1_score" : team1_score if team1_score != -1 else temp["team1_score"],
                        "team2_score" : team2_score if team2_score != -1 else temp["team2_score"],
                        "wins": win if win != -1 else temp["wins"],
                        "finished" : finished if finished!= -1 else temp["finished"]
                    }
                    
                    await inter.response.send_message("**Đã sửa thông tin trận đấu !**", ephemeral=True)
                    break
            
            

        else:
            await inter.response.send_message("**Bạn không có quyền để làm việc này !**", ephemeral=True)
        saving_bet(self.info)
    @nextcord.slash_command(name="match_info", description="Thông tin trận đấu")   
    async def match_info(self, inter:nextcord.Interaction,id):
        self.info = open_bet()
        for _ in self.info["data"]["matches"]:
            if int(_["id"]) == int(id):
                title = f"{_["team1"]} - {_["team2"]}" if _["finished"] == 0 else f"{_["team1"]} {_["team1_score"]} - {_["team2_score"]} {_["team2"]}"
                bet_info = f"{_["team1"]} thắng: {_["bet"][0]} | Hòa: {_["bet"][1]} | {_["team2"]} thắng: {_["bet"][2]}"
                is_finished = "Hết giờ" if _["finished"] == 1 else "Đang diễn ra hoặc chuẩn bị"
                embed = nextcord.Embed(title=title,
                      description=f"Time: {datetime.fromtimestamp(_["time"]).strftime("%H:%M %d-%m-%Y")}\nBet info: {bet_info}\nTiến độ: {is_finished}",
                      colour=0x00b0f4,
                      timestamp=datetime.now())

                embed.set_author(name=f"{_["tournamentName"]} - {_["round"]}")
                await inter.response.send_message(embed=embed)
                
                break
    @nextcord.slash_command(name="delete_match", description="Xóa thông tin trận đấu")   
    async def delete_match(self, inter:nextcord.Interaction,id):
        self.info = open_bet()
        if str(inter.user.id) == "748439531761434676":
            for _ in range(len(self.info["data"]["matches"])):
                if self.info["data"]["matches"][_]["id"] == id:
                    del self.info["data"]["matches"][_]
        else:
            await inter.response.send_message("**Bạn không có quyền để làm việc này !**", ephemeral=True)
        saving_bet(self.info)
    
    @nextcord.slash_command(name="transfer_bet_winner", description="Chuyển chuối cho người cược thắng")
    async def transfer_bet_winner(self, inter : nextcord.Interaction, user: nextcord.User, creds:int,multiply_win: float):
        self.info = open_bet()
        if str(inter.user.id) == "748439531761434676":
            info_wallet = open_economy()
            info_wallet["data"][str(user.id)]["money"] += int(creds*multiply_win)
            saving_economy(info_wallet)
            await inter.response.send_message(f"**Đã chuyển chuối cho {user.mention} phần thưởng __{int(creds*multiply_win):,}__ :banana:**")
        else:
            await inter.response.send_message("**Bạn không có quyền để làm việc này !**", ephemeral=True)
            
    @nextcord.slash_command("bet_a_match", description="Cược trận đấu")
    async def bet_a_match(self, inter:nextcord.Interaction,id:int,creds: int,team = SlashOption(name="team", description="Team bạn muốn cược", choices={
        "Hòa": "0",
        "Team 1 thắng": "1",
        "Team 2 thắng": "2"
})):
        self.info = open_bet()
        ok = True
        for _ in self.info["data"]["matches"]:
            if int(_["id"])== int(id):
                ok = False
                is_match_signed(id)
                data_ = open_bet_database()
                for i in range(len(data_["data"]["bet_info"])):
                    # print(data_["data"]["bet_info"][i])
                    isFindID = False
                    if data_["data"]["bet_info"][i]["id"] == _["id"] and data_["data"]["bet_info"][i]["canBet"]:
                        isFindID = True
                        if str(inter.user.id) not in data_["data"]["bet_info"][i]["betPlayer"]:
                            if int(team) == 0:
                                data_["data"]["bet_info"][i]["draw"].append({str(inter.user.id) : creds})
                            elif int(team) == 1:
                                data_["data"]["bet_info"][i]["team1"].append({str(inter.user.id) : creds})
                            else:
                                data_["data"]["bet_info"][i]["team2"].append({str(inter.user.id) : creds})
                            data_["data"]["bet_info"][i]["betPlayer"].append({str(inter.user.id) : creds})
                            saving_bet_database(data_)
                            
                            Currency(str(inter.user.id)).transfer("748439531761434676",int(creds))
                            
                            await inter.response.send_message("**Cược thành công !**")
                            break
                    if isFindID:
                        pass
                        print("K cược được")
                        await inter.response.send_message("**Trận đấu đã hết thời gian cược hoặc bạn đã cược trận đấu này !**", ephemeral=True)
                break
        
        if ok:
            await inter.response.send_message("**Sai ID !**", ephemeral=True)
           
    @nextcord.slash_command(name="list_bet", description="Thông tin cược")
    async def list_bet(self, inter: nextcord.Interaction, id:int):
        self.info = open_bet()
        ok = True
        for _ in self.info["data"]["matches"]:
            if int(_["id"]) == int(id):
                ok = False
                title = f"{_["team1"]} - {_["team2"]}" if _["finished"] == 0 else f"{_["team1"]} {_["team1_score"]} - {_["team2_score"]} {_["team2"]}"
                bet_info = f"{_["team1"]} thắng: {_["bet"][0]} | Hòa: {_["bet"][1]} | {_["team2"]} thắng: {_["bet"][2]}"
                is_finished = "Hết giờ" if _["finished"] == 1 else "Đang diễn ra hoặc chuẩn bị"
                embed = nextcord.Embed(title=title,
                      description=f"Time: {datetime.fromtimestamp(_["time"]).strftime("%H:%M %d-%m-%Y")}\nBet info: {bet_info}\nTiến độ: {is_finished}\n",
                      colour=0x00b0f4,
                      timestamp=datetime.now())
                embed.set_author(name=f"{_["tournamentName"]} - {_["round"]}")
                is_match_signed(id)
                data_ = open_bet_database()
                for i in range(len(data_["data"]["bet_info"])):
                    if data_["data"]["bet_info"][i]["id"] == id:
                        if len(data_["data"]["bet_info"][i]["team1"]) != 0:
                            data_team_1 = []
                            for j in data_["data"]["bet_info"][i]["team1"]:
                                for key, value in j.items():
                                    data_team_1.append(f"<@{key}> {value:,}")
                            team_1 = ", ".join(data_team_1)
                        else:
                            team_1 = "Không ai đủ can đảm để cược cho đội này ..."
                        if len(data_["data"]["bet_info"][i]["team2"]) != 0:
                            data_team_2 = []
                            for j in data_["data"]["bet_info"][i]["team2"]:
                                for key, value in j.items():
                                    data_team_2.append(f"<@{key}> {value:,}")
                            team_2 = ", ".join(data_team_2)
                        else:
                            team_2 = "Không ai đủ can đảm để cược cho đội này ..." 
                        if len(data_["data"]["bet_info"][i]["draw"]) != 0:
                            data_draw = []
                            for j in data_["data"]["bet_info"][i]["draw"]:
                                for key, value in j.items():
                                    data_draw.append(f"<@{key}> {value:,}")
                            draw_ = ", ".join(data_draw)
                        else:
                            draw_ = "Không ai đủ can đảm để cược cho đội này ..."
                embed.add_field(name=f"{_["team1"]} thắng: ", value=team_1, inline=False)
                embed.add_field(name=f"{_["team2"]} thắng: ", value=team_2, inline=False)
                embed.add_field(name="Hòa", value=draw_, inline=False)
                await inter.response.send_message(embed=embed)
                break
        if ok:
            await inter.response.send_message("Sai ID !")
                
                
    @nextcord.slash_command(name="off_bet", description="Đóng cược")
    async def off_bet(self, inter: nextcord.Interaction, id:int):    
        self.info = open_bet()
        if str(inter.user.id) == "748439531761434676":
            is_match_signed(id)
            data_ = open_bet_database()
            for i in range(len(data_["data"]["bet_info"])):
                if data_["data"]["bet_info"][i]["id"] == id:
                    data_["data"]["bet_info"][i]["canBet"] = False
                    saving_bet_database(data_)
                    await inter.response.send_message("**Đóng cược thành công !**")
        else:
            await inter.response.send_message("**Lỗi**", ephemeral=True)
                
    
    
def setup(bot):
    bot.add_cog(Bet(bot))
    