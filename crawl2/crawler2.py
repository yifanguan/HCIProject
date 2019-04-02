import requests
import json
import csv
import sys
import pickle

# selected injuried player file format: YYYY/MM/DD,playerName
def get_name_year(filename):
    player_year = {}
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            date,name = line.strip().split(',')
            year = date.strip().split('/')[0]
            player_year[name] = int(year)
    return player_year

def get_yearly_data(playerID, Year):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    YearStr = str(Year-1)+'-'+str(Year-2000)
    url = "https://stats.nba.com/stats/playerdashboardbygeneralsplits?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=" + str(playerID) + "&PlusMinus=N&Rank=N&Season=" + YearStr + "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&Split=general&VsConference=&VsDivision="
    r = requests.get(url,headers=headers)
    demo = r.text
    parsed = json.loads(r.text)
    return parsed['resultSets'][3]['rowSet']


def main():
    '''
    already_runned = ["Al Harrington","Samuel Dalembert","Josh Childress","James Anderson","David Lee","Udonis Haslem",
                      "Reggie Evans","Delonte West","Joe Johnson","Damion James","Yi Jianlian","Joakim Noah","Craig Smith","Chuck Hayes",
                      "Anderson Varejao","Brandan Wright","Danilo Gallinari","Caron Butler","Brandon Jennings","Matt Barnes","Marcus Camby",
                      "Jason Williams","Marquis Daniels","Dominique Jones","Rudy Gay","Antawn Jamison","Glen Davis","Nate Robinson","Channing Frye",
                      "Terrence Williams","Tim Duncan","Joel Przybilla","Deron Williams","Andrew Bogut","Andrew Bynum","Ramon Sessions","Samardo Samuels"]
    '''
    data_indices = [1, 2, 6, 26, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 28, 29, 30, 27]
    # get player id and name for later web requests use
    filename = 'player_name_id_dict'
    infile = open(filename,'rb')
    player_name_id_dict = pickle.load(infile)
    infile.close()

    # read player name and injuried date from file
    filename = 'selected_injuried_player.txt'
    player_year_dict = get_name_year(filename)

    headerLine = ['Player','Year','MONTH', 'GP', 'MIN', 'PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'PF', 'FP', 'DD2', 'TD3', 'PLUS_MINUS']
    outFileName = "selected_injuried_players.csv"
    output = open(outFileName,'w')
    csvwriter = csv.writer(output)
    csvwriter.writerow(headerLine)

    for player, year in player_year_dict.items():
        #if (player in already_runned):
        #    continue
        print(player)
        playerID = player_name_id_dict[player]
        year_before = get_yearly_data(playerID, year-1)
        year_injuried = get_yearly_data(playerID, year)
        year_after = get_yearly_data(playerID, year+1)
        three_year = year_before + year_injuried + year_after
        for i in range(len(three_year)):
            if i < len(year_before):
                csvwriter.writerow([player,str(year-1)]+[three_year[i][index] for index in data_indices])
            elif i < len(year_before + year_injuried):
                csvwriter.writerow([player,str(year)]+[three_year[i][index] for index in data_indices])
            else:
                csvwriter.writerow([player,str(year+1)]+[three_year[i][index] for index in data_indices])

    output.close()

if __name__ == "__main__":
    main()
