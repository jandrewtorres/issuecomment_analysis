import argparse

import ghapi as gh

# parse arguments
parser = argparse.ArgumentParser()
# positional arguments
parser.add_argument('org', help='name of target organization')
# optional
parser.add_argument('-u', '--user', action='store', help='github username')
parser.add_argument('-p', '--password', action='store', help='github password')
args = parser.parse_args()
ORGANIZATION = args.org
USERNAME = args.user
PASSWORD = args.password

# init gh api
api = gh.GitHubAPI("jandrewtorres", "Andr3w135246")

# init relational tables
repos_table = {'id': [],
               'name': [],
               'description': [],
               'created_at': [],
               'updated_at': [],
               'pushed_at': [],
               'size': [],
               'stargazers_count': [],
               'watchers_count': [],
               'language': [],
               'forks_count': [],
               'archived': [],
               'open_issue_count': [],
               'subscribers_count': []}
# milestone, labels, assignees, requested reviewers, requested teams FK
pulls_table = {
    "id": [],
    "number": [],
    "state": [],
    "locked": [],
    "title": [],
    "user": [],
    "body": [],
    "milestone": [],
    "active_lock_reason": [],
    "created_at": [],
    "updated_at": [],
    "closed_at": [],
    "merged_at": [],
    "assignee": [],
    "merged": [],
    "mergeable": [],
    "rebaseable": [],
    "mergeable_state": [],
    "merged_by": [],
    "comments": [],
    "review_comments": [],
    "commits": [],
    "additions": [],
    "deletions": [],
    "changed_files": []
}
pr_review_comments_table = {
    "id": [],
    "pull_request_review_id": [],
    "in_reply_to_id": [],
    "user": [],
    "body": [],
    "created_at": [],
    "updated_at": []
}
reviews_table = {
    "id": [],
    "user": [],
    "body": [],
    "state": []
}

organization = api.get_organization(ORGANIZATION)
print("Retrieved " + ORGANIZATION)

repos = api.get_repositories(ORGANIZATION)
print("Retrieved " + str(len(repos)) + " repositories")

for repo in repos:
    # insert repo information
    for k in repos_table.keys():
        repos_table[k].append(repo[k])
    print("Added info for repo: " + repo['name'])

    pulls = api.get_pull_requests(ORGANIZATION, repo['name'])
    print("\tRetrieved " + str(len(pulls)) + " PRs")

    pr_review_comments = api.get_all_pull_request_comments(ORGANIZATION, repo['name'])
    print("\tRetrieved " + str(len(pr_review_comments)) + " PR Review Comments")


    for pull in pulls:
        pull_detail = api.get_pull_request(ORGANIZATION, repo['name'], pull['number'])
        for k in pulls_table.keys():
            pulls_table[k].append(pull_detail[k])

        reviews = api.get_reviews_for_pull_request(ORGANIZATION, repo, pull['number'])
        print("\tRetrieved " + str(len(reviews)) + " Reviews for PR #" + str(pull['number']))

        requests = api.get_review_requests_for_pull_request(ORGANIZATION, repo, pull['number'])
        print("\tRetrieved " + str(len(requests)) + " Requests for PR #" + str(pull['number']))

        data = {
            'pull_num': pull['number'],
            'repo': repo,
            'org': ORGANIZATION,
            'review_requests': requests,
            'reviews': reviews,
            'review_comments': pr_review_comments
        }


