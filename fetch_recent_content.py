import requests
import xml.etree.ElementTree as ET
import sys
import json
import os
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

def write_article_names(file_path, articles):
    with open(file_path, 'w') as f:
        f.write('## Recent Articles\n\n')
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

    repo.update_file(readme.path, 'Update recent articles', updated_content, readme.sha)

if __name__ == "__main__":
    FEED_URLS = sys.argv[1].split(',')
    ARTICLE_LIMIT = int(sys.argv[2])
    GITHUB_TOKEN = sys.argv[3]
    ARTICLES_MD_PATH = 'recent_articles.md'

    all_articles = []
    for url in FEED_URLS:
        feed_content = fetch_articles_from_rss(url)
        articles = parse_rss_articles(feed_content)
        all_articles.extend(articles)

    all_articles = all_articles[:ARTICLE_LIMIT]
    write_article_names(ARTICLES_MD_PATH, all_articles)

    g = Github(GITHUB_TOKEN)
    user = g.get_user()
    repo = user.get_repo(user.login)
    update_readme(repo, ARTICLES_MD_PATH)
