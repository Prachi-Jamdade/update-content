import requests
import json
import xml.etree.ElementTree as ET
import re
from github import Github

def fetch_articles_from_rss(feed_url):
    response = requests.get(feed_url)
    response.raise_for_status()
    return response.content

def parse_rss_articles(feed_content):
    root = ET.fromstring(feed_content)
    articles = []
    for item in root.findall('./channel/item'):
        title = item.find('title').text
        link = item.find('link').text
        articles.append({'title': title, 'link': link})
    return articles

def fetch_articles_from_devto(username):
    api_url = f"https://dev.to/api/articles?username={username}"
    response = requests.get(api_url)
    response.raise_for_status()
    articles = response.json()
    return [{'title': article['title'], 'link': article['url'], 'positive_reactions_count': article['positive_reactions_count'], 'comments_count': article['comments_count']} for article in articles]

def extract_devto_username(profile_url):
    match = re.search(r'dev\.to\/@?([\w\d]+)', profile_url)
    if match:
        return match.group(1)
    return None

def write_article_names(file_path, articles):
    with open(file_path, 'w') as f:
        f.write('## Articles\n\n')
        for article in articles:
            link = article.get('link')
            url = article.get('url', '#')  
            if link is None:
                f.write(f"- [{article['title']}]({url})\n")
            else:
                f.write(f"- [{article['title']}]({link})\n")

def update_readme(repo, articles_md_path):
    readme = repo.get_readme()
    readme_content = readme.decoded_content.decode()

    start_marker = '<!-- ARTICLES -->'
    end_marker = '<!-- /ARTICLES -->'

    start_idx = readme_content.find(start_marker) + len(start_marker)
    end_idx = readme_content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        raise ValueError("Markers not found in README file")

    with open(articles_md_path, 'r') as ra:
        recent_articles = ra.read()

    updated_content = (readme_content[:start_idx].strip() + "\n\n" +
                       recent_articles.strip() + "\n" +
                       readme_content[end_idx:].strip())

    repo.update_file(readme.path, 'Update articles', updated_content, readme.sha)

def sort_devto_blogs(articles, top_n=5):
    sorted_articles = sorted(articles, key=lambda x: (x['positive_reactions_count'], x['comments_count']), reverse=True)
    return sorted_articles[:top_n]

def fetch_articles_from_hashnode(token):
    url = "https://gql.hashnode.com"
    
    query = """
    query {
        me {
            posts(pageSize: 20, page: 1) {
                nodes {
                    id
                    title
                    url
                    views
                    reactionCount
                    replyCount
                    responseCount
                }
            }
        }
    } 
    """
    
    data = {'query': query}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(data)
    )
    
    if response.status_code == 200:
        response_data = response.json()
        posts = response_data.get('data', {}).get('me', {}).get('posts', {}).get('nodes', [])
        return posts
    else:
        print(f"Query failed to run with a {response.status_code}. Error: {response.text}")
        return []

def sort_hashnode_blogs(articles, top_n=5):
    sorted_articles = sorted(articles, key=lambda x: (x.get('views', 0), x.get('reactionCount', 0)), reverse=True)
    return sorted_articles[:top_n]

def get_github_repo(github_token):
    g = Github(github_token)
    user = g.get_user()
    return user.get_repo(user.login)