# Article Highlighter

## Description

The **Article Highlighter** GitHub Action fetches recent or top articles from specified RSS feeds and updates your GitHub profile README with the latest content. This action allows you to highlight articles based on views, likes, or comments and is perfect for showcasing recent and popular posts directly in your profile.

## Inputs

#### `feed_urls`

- **Description**: Comma-separated list of RSS feed URLs from which to fetch articles.
- **Required**: `true`
- **Example**: `https://example.com/rss, https://anotherexample.com/rss`

#### `article_limit`

- **Description**: Number of articles to fetch. Use `0` or a negative number to fetch recent articles only.
- **Required**: `true`
- **Default**: `5`
- **Example**: `10`

#### `article_type`

- **Description**: Type of articles to fetch: `"recent"` or `"top"`.
- **Required**: `true`
- **Default**: `recent`
- **Example**: `top`

#### `github_token`

- **Description**: GitHub token for authentication to update the profile README.
- **Required**: `true`
- **Example**: `ghp_XXXXXXXXXXXXXXXXXXXXXX`

## Usage

To use the **Article Highlighter** action, create a workflow in your GitHub repository. Follow these steps:

1. **Create a Workflow File**

   In your repository, create a file named `.github/workflows/update-profile-readme.yml`.

2. **Add the Workflow Configuration**

   Add the following configuration to the file:

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
             article_type: 'recent'
             github_token: ${{ secrets.TOKEN_GITHUB }}```

3. **Configure Secrets for Article Highlighter**

To use the **TopContentProfileUpdater** GitHub Action, you must configure a GitHub personal access token as a secret in your repository. Follow these steps to add the required secret:

* **Go to Your Repository Settings**

   - Navigate to your repository on GitHub.
   - Click on **Settings**.

* **Access Secrets Management**

   - In the left sidebar, click on **Secrets and variables**.
   - Then select **Actions**.

* **Add a New Secret**

   - Click on **New repository secret**.

* **Configure the Secret**

   - **Name** the secret `TOKEN_GITHUB`.
   - **Paste** your GitHub personal access token as the value.
   - Click **Add secret** to save.

After adding the secret, your GitHub Action can authenticate and update your profile README with the latest content.

4. **Verify and Trigger**

   - Check the Actions tab in your GitHub repository to ensure the workflow runs successfully.
   - You can also manually trigger the workflow from the Actions tab if you need to update your README immediately.
