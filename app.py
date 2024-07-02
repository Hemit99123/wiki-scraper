from flask import Flask
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Gets the top 10 earning companies in US from Wiki page

@app.route('/')
def home():
    url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'

    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html')

    table = soup.find_all('table', class_ = 'wikitable sortable')[2] 

    table_data = table.find_all('td')


    name_ranking = []
    profit_ranking = []



    for html in table_data:
        anchor_element = html.find('a')

        
        if html.get('style') == 'text-align:center;':
            profit = html.text.strip()
            profit_ranking.append(profit)

        if anchor_element:
            name = anchor_element.text.strip()
            name_ranking.append(name)

    response_data = [{'name': name, 'profit': profit} for name, profit in zip(name_ranking, profit_ranking)]

    return response_data

# Gets the references used by Wiki 

@app.route('/references')
def references():

    url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'

    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html')
    
    references_response = []

    references_list = soup.find_all('cite')

    for list_item in references_list:

        anchor_element = list_item.find('a')
        
        link = anchor_element['href']

        references_response.append(link)
    
    return references_response

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)