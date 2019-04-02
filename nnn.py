import requests
import json
import csv
import sys
import urllib3
from urllib3 import ProxyManager, make_headers

def main():
	playerID = '201973'
	Year = '2010-11'
	headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
	}

	# Now you can use `http` as you would a normal PoolManager
	url = "https://stats.nba.com/stats/playerdashboardbygeneralsplits?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=" + playerID + "&PlusMinus=N&Rank=N&Season=" + Year + "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&Split=general&VsConference=&VsDivision="
	r = requests.get(url,headers=headers)
	#r=requests.get("https://stats.nba.com/stats/playerdashboardbygeneralsplits?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=201567&PlusMinus=N&Rank=N&Season=2017-18&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&Split=general&VsConference=&VsDivision=",headers=headers)


	demo = r.text
	# soup = BeautifulSoup(demo, "html.parser")
	# print(soup.prettify())
	parsed = json.loads(r.text)
	#print(json.dumps(parsed,indent=4,sort_keys=True))

	MonthlyData = parsed['resultSets'][3]
	headerLine = ['MONTH']+MonthlyData['headers'][2:-1]
	outFileName = playerID + "_" + Year + ".csv"
	output = open(outFileName,'w')
	csvwriter = csv.writer(output)
	csvwriter.writerow(headerLine)
	for i in range(len(MonthlyData['rowSet'])):
		csvwriter.writerow(MonthlyData['rowSet'][i][1:-1])
	output.close()

if __name__ == "__main__":
    main()