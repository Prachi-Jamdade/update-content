import sys
from utils import (
    fetch_articles_from_rss,
    parse_rss_articles,
    fetch_articles_from_devto,
    fetch_articles_from_hashnode,
    extract_devto_username,
    write_article_names,
    update_readme,
    sort_devto_blogs,
    sort_hashnode_blogs,
    get_github_repo
)

def main(feed_urls, article_limit, article_type, github_token, hashnode_token):
    all_articles = []
    for url in feed_urls:
        if 'dev.to' in url:
            username = extract_devto_username(url)
            if username:
                articles = fetch_articles_from_devto(username)
                if article_type == 'top' and article_limit > 0:
                    top_articles = sort_devto_blogs(articles, article_limit)
                    all_articles.extend(top_articles)
                elif article_type == 'recent':
                    all_articles.extend(articles)
        elif 'hashnode' in url:
            articles = fetch_articles_from_hashnode(hashnode_token)
            if article_type == 'top' and article_limit > 0:
                top_articles = sort_hashnode_blogs(articles, article_limit)
                all_articles.extend(top_articles)
            elif article_type == 'recent':
                all_articles.extend(articles)
        else:
            feed_content = fetch_articles_from_rss(url)
            articles = parse_rss_articles(feed_content)
            all_articles.extend(articles)

    all_articles = all_articles[:article_limit]
    print(all_articles)
    articles_md_path = 'articles.md'
    write_article_names(articles_md_path, all_articles)

    repo = get_github_repo(github_token)
    update_readme(repo, articles_md_path)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python3 update_articles.py <feed_urls> <article_limit> <article_type> <github_token> <hashnode_token>")
        sys.exit(1)

    FEED_URLS = sys.argv[1].split(',')
    ARTICLE_LIMIT = int(sys.argv[2])
    ARTICLE_TYPE = sys.argv[3]
    GITHUB_TOKEN = sys.argv[4]
    HASHNODE_TOKEN = sys.argv[5]

    main(FEED_URLS, ARTICLE_LIMIT, ARTICLE_TYPE, GITHUB_TOKEN, HASHNODE_TOKEN)