import requests

def fetch_articles(username):
    url = f"https://dev.to/api/articles?username={username}&per_page=1000"
    response = requests.get(url)
    
    if response.status_code == 200:
        articles = response.json()
        return articles
    else:
        print(f"Failed to fetch articles: {response.status_code}")
        return []

def get_top_articles(articles, top_n=5):
    sorted_articles = sorted(articles, key=lambda x: (x['positive_reactions_count'], x['comments_count']), reverse=True)
    return sorted_articles[:top_n]

def print_top_articles(articles):
    for article in articles:
        title = article['title']
        url = article['url']
        likes = article['positive_reactions_count']
        comments = article['comments_count']
        print(f"Title: {title}\nURL: {url}\nLikes: {likes}\nComments: {comments}\n")

# Replace 'username' with the actual Dev.to username
username = 'tiaeastwood'
articles = fetch_articles(username)

if articles:
    top_articles = get_top_articles(articles, 10)
    print_top_articles(top_articles)
else:
    print("No articles found.")
