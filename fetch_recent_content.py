import requests
import xml.etree.ElementTree as ET
import sys
import json

def fetch_articles_from_rss(feed_url):
    response = requests.get(feed_url)
    response.raise_for_status()
    return response.content

def fetch_articles_from_api(api_url):
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()

def parse_rss_articles(feed_content):
    root = ET.fromstring(feed_content)
    articles = []
    for item in root.findall('./channel/item'):
        title = item.find('title').text
        link = item.find('link').text
        articles.append({'title': title, 'link': link})
    return articles

def parse_api_articles(api_response):
    articles = []
    for item in api_response:
        title = item['title']
        link = item['url']
        articles.append({'title': title, 'link': link})
    return articles

def write_article_names(file_path, articles):
    with open(file_path, 'w') as f:
        f.write('## Recent Articles\n\n')
        for article in articles:
            f.write(f"- [{article['title']}]({article['link']})\n")

def update_readme(readme_path, articles_md_path):
    with open(articles_md_path, 'r') as ra:
        recent_articles = ra.read()

    with open(readme_path, 'r') as readme:
        readme_content = readme.read()

    start_marker = '<!-- ARTICLES -->'
    end_marker = '<!-- /ARTICLES -->'

    start_idx = readme_content.find(start_marker) + len(start_marker)
    end_idx = readme_content.find(end_marker)

    updated_content = (readme_content[:start_idx] + "\n" + 
                       recent_articles + "\n" + 
                       readme_content[end_idx:])

    with open(readme_path, 'w') as readme:
        readme.write(updated_content)

if __name__ == "__main__":
    API_URLS = sys.argv[1].split(',')
    README_PATH = sys.argv[2]
    ARTICLES_MD_PATH = 'recent_articles.md'
    ARTICLE_LIMIT = int(sys.argv[3])

    all_articles = []
    for url in API_URLS:
        if 'feed' in url: 
            feed_content = fetch_articles_from_rss(url)
            articles = parse_rss_articles(feed_content)
        else:
            api_response = fetch_articles_from_api(url)
            articles = parse_api_articles(api_response)
        
        all_articles.extend(articles)

    all_articles = all_articles[:ARTICLE_LIMIT]

    write_article_names(ARTICLES_MD_PATH, all_articles)
    update_readme(README_PATH, ARTICLES_MD_PATH)
