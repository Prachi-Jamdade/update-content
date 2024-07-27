import requests
import xml.etree.ElementTree as ET
import sys
import json
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
            f.write(f"- [{article['title']}]({article['link']})\n")

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

def get_top_articles(articles, top_n=5):
    sorted_articles = sorted(articles, key=lambda x: (x['positive_reactions_count'], x['comments_count']), reverse=True)
    return sorted_articles[:top_n]

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python update_articles.py <feed_urls> <article_limit> <article_type> <github_token>")
        sys.exit(1)

    FEED_URLS = sys.argv[1].split(',')
    ARTICLE_LIMIT = int(sys.argv[2])
    ARTICLE_TYPE = sys.argv[3]
    GITHUB_TOKEN = sys.argv[4]
    ARTICLES_MD_PATH = 'README.md'

    all_articles = []
    for url in FEED_URLS:
        if 'dev.to' in url:
            username = extract_devto_username(url)
            if username:
                articles = fetch_articles_from_devto(username)
                if ARTICLE_TYPE == 'top' and ARTICLE_LIMIT > 0:
                    top_articles = get_top_articles(articles, ARTICLE_LIMIT)
                    all_articles.extend(top_articles)
                elif ARTICLE_TYPE == 'recent':
                    all_articles.extend(articles)
        else:
            feed_content = fetch_articles_from_rss(url)
            articles = parse_rss_articles(feed_content)
            all_articles.extend(articles)

    all_articles = all_articles[:ARTICLE_LIMIT]
    write_article_names(ARTICLES_MD_PATH, all_articles)

    g = Github(GITHUB_TOKEN)
    user = g.get_user()
    repo = user.get_repo(user.login)
    update_readme(repo, ARTICLES_MD_PATH)
