#!/usr/bin/env python3
import sys
import os
import requests
import json

# Set up color variables
YELLOW = '\033[1;93m'
GREEN = '\033[0;32m'
NC = '\033[0m'  # No Color

print('''
   ______    _    __         
  / ____/   (_)  / /_   _____
 / / __    / /  / __/  / ___/
/ /_/ /   / /  / /_   / /    
\____/   /_/   \__/  /_/     
                             -Azefox
''')

print(f"{YELLOW}What topic are you interested in?{NC}")
input_topic = input().strip().lower().replace(" ", "+")

# Fetch the total count of repositories
url = f"https://api.github.com/search/repositories?q=stars%3A%3E50+{input_topic}+sort:stars+in%3Aname&per_page=5"
response = requests.get(url)
data = response.json()
total_count = data.get('total_count', None)

# Check if total_count is null or empty
if total_count is None or total_count == 0:
    print(f"{YELLOW}Sorry, no results found{NC}")
    sys.exit(1)

# Calculate the number of pages needed, rounding up
page_count = (total_count + 4) // 5

with open(f"{input_topic}-repos.txt", 'w') as output_file:
    for page in range(1, page_count + 1):
        # Fetch repositories for each page
        url = f"https://api.github.com/search/repositories?q=stars%3A%3E50+{input_topic}+sort:stars+in%3Aname&per_page=5&page={page}"
        response = requests.get(url)
        data = response.json()
        repos = [item['html_url'] for item in data.get('items', []) if 'html_url' in item]

        if not repos:
            break  # Stop the loop if no repositories are returned
        
        for repo_url in repos:
            output_file.write(repo_url + '\n')

if os.path.exists(f"{input_topic}-repos.txt"):
    with open(f"{input_topic}-repos.txt", 'r') as infile:
        total_repos = sum(1 for line in infile)

    print(f"{YELLOW}Total repos found: {GREEN}{total_repos}{NC}")

