from numpy import integer
import requests
from bs4 import BeautifulSoup
import pandas
import justpy as jp

char_def = """
{
    chart: {
        type: 'columnpyramid'
    },
    title: {
        text: 'The Scoring Ranking'
    },
    colors: ['#C79D6D', '#B5927B', '#CE9B84', '#B7A58C', '#C7A58C'],
    xAxis: {
        crosshair: true,
        labels: {
            style: {
                fontSize: '14px'
            }
        },
        type: 'category'
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Score'
        }
    },
    tooltip: {
        valueSuffix: ' points'
    },
    series: [{
        name: 'Total Score',
        colorByPoint: true,
        data: [
            ['Pyramid of Khufu', 138.8],
            ['Pyramid of Khafre', 136.4],
            ['Red Pyramid', 104],
            ['Bent Pyramid', 101.1],
            ['Pyramid of the Sun', 75]
        ],
        showInLegend: false
    }]
}

"""


def createData():

    r = requests.get("http://www.espn.com/nba/history/leaders")
    c = r.content
    soup = BeautifulSoup(c, "html.parser")

    table = soup.find_all("table", {"class": "tablehead"})

    i = []
    for item in table:
        d = {}

        player_listOdd = item.find_all("tr", {"class": "oddrow"})

        counter = 0
        for num in range(len(player_listOdd)):
            for child in player_listOdd[num].children:
                if (counter % 3 == 0):
                    d["Ranking"] = child.text
                    counter = counter + 1

                elif (counter % 3 == 1):
                    d["Player"] = child.text
                    counter = counter + 1

                else:
                    key = child.text.replace(",", "")
                    d["Score"] = key
                    # print(d)
                    counter = counter + 1

            dict_copy = d.copy()
            i.append(dict_copy)

        counter = 0
        replace = 1
        player_listEven = item.find_all("tr", {"class": "evenrow"})
        for num in range(len(player_listEven)):
            for child in player_listEven[num].children:
                if (counter % 3 == 0):
                    d["Ranking"] = child.text
                    counter = counter + 1

                elif (counter % 3 == 1):
                    d["Player"] = child.text
                    counter = counter + 1

                else:
                    key = child.text.replace(",", "")
                    d["Score"] = key
                    # print(d)
                    counter = counter + 1

            dict_copy = d.copy()
            i.insert(replace, dict_copy)
            replace = replace + 2

    return i


def app():
    data = pandas.read_csv('NBA_pointsLeader.csv')

    score_list = list(data["Score"])
    integer_map = map(int, score_list)
    int_list = list(integer_map)

    name_list = list(data["Player"])

    wp = jp.QuasarPage()
    h1 = jp.QDiv(a=wp, text="The Ranking of Point Leaders in NBA through the history",
                 classes="text-center q-pt-md")
    p1 = jp.QDiv(a=wp, text="The bar charts represeting the name and score",
                 classes="text-center q-pt-md")
    hc = jp.HighCharts(a=wp, options=char_def)

    hc_data = [[v1, v2] for v1, v2 in zip(name_list, int_list)]
    hc.options.series[0].data = hc_data

    return wp


def main():
    data = createData()
    jp.justpy(app)
    # jp.justpy(app)
    # df = pandas.DataFrame(data)
    # df.to_csv("NBA_pointsLeader.csv")


main()
