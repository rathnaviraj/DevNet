import requests
import networkx as nx
import matplotlib.pyplot as plt
import os
import sys, getopt

username = None
repository = None

# list of command line arguments
argument_list = sys.argv[1:]
 
# Options
options = "ur:"
 
# Long options
long_options = ["username=", "repository="]
 
try:
    # Parsing argument
    arguments, values = getopt.getopt(argument_list, options, long_options)
     
    # checking each argument
    for current_argument, current_value in arguments:
 
        if current_argument in ("-u", "--username"):
            username = current_value
             
        elif current_argument in ("-r", "--repository"):
            repository = current_value
             
except getopt.error as err:
    print(str(err))

token = os.environ.get('GITHUB_TOKEN', None)

if not (username and repository and token):
    print(f'Missing required params [{token} - {username} - {repository}], stopping..')
    sys.exit()

# Fetch contributors
contributors_url = f'https://api.github.com/repos/{username}/{repository}/contributors'
headers = {'Authorization': f'token {token}'}
response = requests.get(contributors_url, headers=headers)
contributors = [contributor['login'] for contributor in response.json()]

# Create a directed graph
G = nx.DiGraph()

# Add nodes for each contributor
for contributor in contributors:
    G.add_node(contributor)

# # Fetch pull request and issue comments
# for contributor in contributors:
#     comments_url = f'https://api.github.com/repos/{username}/{repository}/issues/comments'
#     params = {'creator': contributor}
#     response = requests.get(comments_url, headers=headers, params=params)
#     comments = response.json()
#     print(f'Comments: {comments}')
#     for comment in comments:
#         commenter = comment['user']['login']
#         G.add_edge(contributor, commenter, interaction_type='comment')

# Fetch commit history
commits_url = f'https://api.github.com/repos/{username}/{repository}/commits'
response = requests.get(commits_url, headers=headers)
commits = response.json()

# Parse commits and add edges for contributors who worked on the same files
for commit in commits:
    committer = commit['author']['login']
    commit_sha = commit['sha']
    
    # Fetch details of the commit to get the list of changed files
    commit_details_url = f'https://api.github.com/repos/{username}/{repository}/commits/{commit_sha}'
    response = requests.get(commit_details_url, headers=headers)
    commit_details = response.json()
    
    # Iterate through changed files in the commit
    for file_data in commit_details['files']:
        filename = file_data['filename']
        
        # Check if the file was changed by a contributor
        if committer in contributors:
            # Add an edge to represent contributors working on the same file
            G.add_edge(committer, filename, interaction_type='file_change')

# Fetch commit history
# Fetch commit data, extract relevant contributors, and add edges to the graph

# Visualize the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=100, node_color='lightblue')
edge_labels = nx.get_edge_attributes(G, 'interaction_type')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("Developer Social Network")
plt.show()
