from nextcord.ext import commands
from datetime import datetime
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



class Bet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.info = open_bet()
    @nextcord.slash_command(name="create_match", description="Tạo thông tin trận đấu")
    async def create_match(self, inter:nextcord.Interaction,tournament_name:str, round:str , time:str, team1_name:str, team2_name:str, bet:str):
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
        if str(inter.user.id) == "748439531761434676":
            for _ in range(len(self.info["data"]["matches"])):
                if self.info["data"]["matches"][_]["id"] == id:
                    del self.info["data"]["matches"][_]
        else:
            await inter.response.send_message("**Bạn không có quyền để làm việc này !**", ephemeral=True)
        saving_bet(self.info)
    
    @nextcord.slash_command(name="transfer_bet_winner", description="Chuyển chuối cho người cược thắng")
    async def transfer_bet_winner(self, inter : nextcord.Interaction, user: nextcord.User, creds:int,multiply_win: float):
        if str(inter.user.id) == "748439531761434676":
            info_wallet = open_economy()
            info_wallet["data"][str(user.id)]["money"] += creds*multiply_win
            saving_economy(info_wallet)
            await inter.response.send_message(f"**Đã chuyển chuối cho {user.mention} phần thưởng __{creds*multiply_win}__ :banana:**")
        else:
            await inter.response.send_message("**Bạn không có quyền để làm việc này !**", ephemeral=True)
def setup(bot):
    bot.add_cog(Bet(bot))
    