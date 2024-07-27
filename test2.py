import requests

def fetch_medium_top_articles(username, api_key, top_n=5):
    url = f"https://medium2.p.rapidapi.com/user/{username}/articles"
    
    headers = {
        'X-RapidAPI-Host': 'medium2.p.rapidapi.com',
        'X-RapidAPI-Key': '0ec3d96c07msh59c1108528c884dp1b3746jsne5cfd62fff5a'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        return articles[:top_n]
    else:
        print(f"Failed to fetch articles: {response.status_code}")
        return []

def print_top_articles(articles):
    for article in articles:
        title = article['title']
        url = article['link']
        claps = article.get('claps', 0)
        comments = article.get('responses_count', 0)
        print(f"Title: {title}\nURL: {url}\nClaps: {claps}\nComments: {comments}\n")

# Replace 'your_username' with the actual Medium username and 'your_api_key' with your RapidAPI key
username = 'Prachi-Jamdade'
api_key = 'your_api_key'
top_n = 5

articles = fetch_medium_top_articles(username, api_key, top_n)

if articles:
    print_top_articles(articles)
else:
    print("No articles found.")
