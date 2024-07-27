import requests

def fetch_top_articles(username, limit=10):
    url = "https://api.hashnode.com/"

    query = """
    query GetUserArticles($username: String!, $limit: Int!) {
        user(username: $username) {
            publication {
                posts(page: 0) {
                    title
                    brief
                    slug
                    cuid
                    coverImage
                    dateAdded
                    responseCount
                    totalReactions
                }
            }
        }
    }
    """

    variables = {
        "username": username,
        "limit": limit
    }

    headers = {
        "Content-Type": "application/json",
        "X-User-Agent": "Hashnode-Client"
    }

    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "errors" in data:
            print("Errors:", data["errors"])
        else:
            posts = data["data"]["user"]["publication"]["posts"]
            # Sort posts based on responseCount and totalReactions
            sorted_posts = sorted(posts, key=lambda x: (x["responseCount"], x["totalReactions"]), reverse=True)
            return sorted_posts[:limit]
    else:
        print(f"Failed to fetch articles: {response.status_code}")
        print(response.text)  # To get more details on the error
        return []

# Example usage
username = "CodessPrachi"
top_articles = fetch_top_articles(username)
for article in top_articles:
    print(f"Title: {article['title']}, Comments: {article['responseCount']}, Likes: {article['totalReactions']}")
