import requests
import json
import csv
import pickle

# Need to consider jihousai and changguisai different defense level
def main():
    month_index_dict = {10:0, 11:1, 12:2, 1:3, 2:4, 3:5, 4:6, 5:7, 6:8}
    data_indices = [1, 2, 6, 26, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 28, 29, 30, 27]
    # get player id and name for later web requests use
    filename = 'player_name_id_dict'
    infile = open(filename,'rb')
    player_name_id_dict = pickle.load(infile)
    infile.close()

    # output file
    # Note: we could determine later what kinds of stats we want
    # FP: NBA_FANTASY_PTS
    headerLine = ['Date', 'Team', 'Acquired', 'Relinquised', 'Injury part', 'Descriptive Verb'] + ['##'] + ['MONTH', 'GP', 'MIN', 'PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'PF', 'FP', 'DD2', 'TD3', 'PLUS_MINUS'] + ['&&'] + ['MONTH', 'GP', 'MIN', 'PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'PF', 'FP', 'DD2', 'TD3', 'PLUS_MINUS']
    outFileName = "whole_stats.csv"
    output = open(outFileName, 'w')
    csvwriter = csv.writer(output)
    csvwriter.writerow(headerLine)
    # get info of injuried players from preprocessed csv file
    injury_database = csv.reader(open("new_data.csv",'r'))
    # each line: ['2010/10/3', 'Bulls', '', 'Carlos Boozer', 'finger/', 'fracture/']
    for line in injury_database:
        player_name = line[3]
        playerID = str(player_name_id_dict[player_name])
        print(playerID)
        print(player_name)
        date = line[0].strip().split('/')
        injuried_year = int(date[0])
        injuried_month = int(date[1])
        # injuried_day = date[2] might not be useful in our case
        year = str(injuried_year)+'-'+str(injuried_year+1)[-2:]
        # make request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }

        url = "https://stats.nba.com/stats/playerdashboardbygeneralsplits?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=" + playerID + "&PlusMinus=N&Rank=N&Season=" + year + "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&Split=general&VsConference=&VsDivision="
        print(url)
        r = requests.get(url,headers=headers)
        parsed = json.loads(r.text)
        MonthlyData_dict = parsed['resultSets'][3]
        MonthlyData_list = MonthlyData_dict['rowSet']
        cur_year = injuried_year + 1
        num = 0
        while MonthlyData_list == [] and num < 10:
            year = str(cur_year)+'-'+str(cur_year+1)[-2:]
            url = "https://stats.nba.com/stats/playerdashboardbygeneralsplits?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=" + playerID + "&PlusMinus=N&Rank=N&Season=" + year + "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&Split=general&VsConference=&VsDivision="
            r = requests.get(url,headers=headers)
            parsed = json.loads(r.text)
            # make additional request if need data from prev yaer or next year
            MonthlyData_dict = parsed['resultSets'][3]
            MonthlyData_list = MonthlyData_dict['rowSet']
            cur_year += 1
            print(num)
            num += 1

        MonthlyData_list_additional = None
        before_injury = []
        after_injury = []
        # make additional request if need data from prev year or next year
        if injuried_month == 10:
            year = str(injuried_year-1)+'-'+str(injuried_year)[-2:]
            url = "https://stats.nba.com/stats/playerdashboardbygeneralsplits?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=" + playerID + "&PlusMinus=N&Rank=N&Season=" + year + "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&Split=general&VsConference=&VsDivision="
            r = requests.get(url,headers=headers)
            parsed = json.loads(r.text)
            # make additional request if need data from prev yaer or next year
            MonthlyData_dict = parsed['resultSets'][3]
            MonthlyData_list_additional = MonthlyData_dict['rowSet']
            num = 0
            cur_year = injuried_year - 1
            while MonthlyData_list_additional == []:
                print('here')
                year = str(cur_year)+'-'+str(cur_year+1)[-2:]
                url = "https://stats.nba.com/stats/playerdashboardbygeneralsplits?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=" + playerID + "&PlusMinus=N&Rank=N&Season=" + year + "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&Split=general&VsConference=&VsDivision="
                r = requests.get(url,headers=headers)
                parsed = json.loads(r.text)
                # make additional request if need data from prev yaer or next year
                MonthlyData_dict = parsed['resultSets'][3]
                MonthlyData_list_additional = MonthlyData_dict['rowSet']
                cur_year -= 1
                print(num)
                num += 1

        if MonthlyData_list_additional == None:
            before_injury = [MonthlyData_list[month_index_dict[injuried_month-1]][index] for index in data_indices]
        else:
            before_injury = [MonthlyData_list_additional[-1][index] for index in data_indices]

        GP = MonthlyData_list[month_index_dict[injuried_month]][2]
        num_til_end = len(MonthlyData_list) - month_index_dict[injuried_month] - 1 # number of months until end of the season
        cur_year = injuried_year + 1
        month = injuried_month
        while GP == 0:
            if month != 12:
                month += 1
            else:
                month = 1
            if num_til_end == 0: # curl next year data if possible
                year = str(cur_year)+'-'+str(cur_year+1)[-2:]
                url = "https://stats.nba.com/stats/playerdashboardbygeneralsplits?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=" + playerID + "&PlusMinus=N&Rank=N&Season=" + year + "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&Split=general&VsConference=&VsDivision="
                r = requests.get(url,headers=headers)
                parsed = json.loads(r.text)
                # make additional request if need data from prev yaer or next year
                MonthlyData_dict = parsed['resultSets'][3]
                MonthlyData_list = MonthlyData_dict['rowSet']
                cur_year += 1
                month = 10

            GP = MonthlyData_list[month_index_dict[month]][2]
            num_til_end -= 1
        after_injury = [MonthlyData_list[month_index_dict[month]][index] for index in data_indices]

        csvwriter.writerow(line+['##']+before_injury+['&&']+after_injury)

    output.close()

if __name__ == "__main__":
    main()