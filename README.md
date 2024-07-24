# Update README with Recent Articles

This GitHub Action fetches recent articles from specified RSS feeds and dev.to profiles and updates the README file with these articles.

## Inputs

- `feed_urls`: A comma-separated list of RSS feed URLs and dev.to profile URLs.
- `article_limit`: The number of articles to include.
- `github_token`: GitHub Token for accessing the repository.

## Example Usage

```yaml
uses: yourusername/your-repo@v1
with:
  feed_urls: 'https://rss_feed_url,https://dev.to/@username'
  article_limit: 5
  github_token: ${{ secrets.GITHUB_TOKEN }}
