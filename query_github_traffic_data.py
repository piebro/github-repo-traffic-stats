import os
import requests
import csv
from datetime import datetime, timedelta

BASE_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GH_TOKEN")
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_github_data(endpoint):
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
    response.raise_for_status()
    return response.json()

def append_to_csv(filename, data):
    file_exists = os.path.isfile(filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(data.keys())
        writer.writerow(data.values())

def save_views_clones_data(data, filename):
    yesterday = (datetime.now() - timedelta(days=1)).date()
    for item in data:
        item_date = datetime.strptime(item['timestamp'][:10], '%Y-%m-%d').date()
        if item_date == yesterday:
            csv_data = {
                'date': item_date.strftime('%Y-%m-%d'),
                'count': item['count'],
                'uniques': item['uniques']
            }
            append_to_csv(filename, csv_data)
            break

def save_referrers_paths_data(data, filename, data_type):
    today = datetime.now().date().strftime('%Y-%m-%d')
    csv_data = {'date': today}

    # If data is empty, don't write anything
    if not data:
        return

    # Ensure we always have 10 items, pad with empty data if necessary
    padded_data = data[:10] + [{'path': '', 'referrer': '', 'count': '', 'uniques': ''}] * (10 - len(data))

    for i, item in enumerate(padded_data, 1):
        csv_data[f'{data_type}_{i}'] = item['path'] if data_type == 'path' else item['referrer']
        csv_data[f'{data_type}_{i}_count'] = item['count']
        csv_data[f'{data_type}_{i}_uniques'] = item['uniques']

    file_exists = os.path.isfile(filename)

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(csv_data.keys())
        writer.writerow(csv_data.values())


def get_user_public_repos(username):
    repos = []
    page = 1
    while True:
        response = get_github_data(f"/search/repositories?q=user:{username}+is:public&page={page}&per_page=100")
        if not response['items']:
            break
        repos.extend([repo['name'] for repo in response['items']])
        page += 1
    return repos

def main():
    with open('github_username.txt', 'r') as file:
        owner = file.read().strip()
        
    repos = get_user_public_repos(owner)
    
    for repo in repos:
        print(f"Processing repository: {repo}")
        try:
            # Get and save views data
            views_data = get_github_data(f"/repos/{owner}/{repo}/traffic/views")
            save_views_clones_data(views_data['views'], f'data/github_views/{repo}.csv')
            
            # Get and save clones data
            clones_data = get_github_data(f"/repos/{owner}/{repo}/traffic/clones")
            save_views_clones_data(clones_data['clones'], f'data/github_clones/{repo}.csv')
            
            # Get and save popular paths data
            paths_data = get_github_data(f"/repos/{owner}/{repo}/traffic/popular/paths")
            save_referrers_paths_data(paths_data, f'data/github_paths/{repo}.csv', 'path')
            
            # Get and save referrers data
            referrers_data = get_github_data(f"/repos/{owner}/{repo}/traffic/popular/referrers")
            save_referrers_paths_data(referrers_data, f'data/github_referrers/{repo}.csv', 'ref')
            
        except requests.exceptions.HTTPError as e:
            print(f"Error processing {repo}: {e}")
            continue

if __name__ == "__main__":
    main()