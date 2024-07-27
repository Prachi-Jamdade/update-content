# Update Profile README

## Description

The **Update Profile README** GitHub Action fetches recent articles from specified RSS feeds and updates your GitHub profile README with the latest content. This is perfect for showcasing recent articles or posts directly in your profile.

## Inputs

### `feed_urls`

- **Description**: Comma-separated list of RSS feed URLs from which to fetch articles.
- **Required**: `true`
- **Example**: `https://example.com/rss, https://anotherexample.com/rss`

### `article_limit`

- **Description**: Number of articles to fetch from each RSS feed.
- **Required**: `true`
- **Default**: `5`
- **Example**: `10`

### `github_token`

- **Description**: GitHub token for authentication to update the profile README.
- **Required**: `true`
- **Example**: `ghp_XXXXXXXXXXXXXXXXXXXXXX`

## Usage

To use this action, create a workflow in your GitHub repository. Here’s a sample workflow YAML configuration:

```yaml
name: Update Profile README

on:
  schedule:
    - cron: '0 0 * * *'  # Runs daily at midnight
  workflow_dispatch: # Allows manual triggering

jobs:
  update-readme:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Update README with latest articles
        uses: Prachi-Jamdade/Prachi-Jamdade@v1.1.0
        with:
          feed_urls: 'https://example.com/rss, https://anotherexample.com/rss'
          article_limit: 5
          github_token: ${{ secrets.GITHUB_TOKEN }}
