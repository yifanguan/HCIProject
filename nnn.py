import requests
import json
import csv
import sys
import pickle

def main():
    data_indices = [1, 2, 6, 26, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 28, 29, 30, 27]
    # get player id and name for later web requests use
    filename = 'player_name_id_dict'
    infile = open(filename,'rb')
    player_name_id_dict = pickle.load(infile)
    infile.close()

    # somehow get id from player_name_id_dict
    playerID = '201973'
    Year = '2009-10'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    url = "https://stats.nba.com/stats/playerdashboardbygeneralsplits?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=" + playerID + "&PlusMinus=N&Rank=N&Season=" + Year + "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&Split=general&VsConference=&VsDivision="
    r = requests.get(url,headers=headers)


    demo = r.text
    parsed = json.loads(r.text)

    MonthlyData = parsed['resultSets'][3]
    headerLine = ['MONTH', 'GP', 'MIN', 'PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'PF', 'FP', 'DD2', 'TD3', 'PLUS_MINUS']
    outFileName = playerID + "_" + Year + ".csv"
    output = open(outFileName,'w')
    csvwriter = csv.writer(output)
    csvwriter.writerow(headerLine)
    for i in range(len(MonthlyData['rowSet'])):
        csvwriter.writerow([MonthlyData['rowSet'][i][index] for index in data_indices])
    output.close()

if __name__ == "__main__":
    main()