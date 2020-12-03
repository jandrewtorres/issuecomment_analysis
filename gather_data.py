from github import Github, PullRequestComment

columns = ["body", "pull_number", "comment_user", "merged", "state", "locked", "pr_title", "pr_user"]

gh = Github("jandrewtorres", "Andr3w135246")
repos = gh.get_organization("Apache").get_repos()
for repo in repos:
    pulls = repo.get_pulls()
    for pull in pulls:
        pull_number = pull.number()
        pr_user = pull.user()
        reviews = pull.get_reviews()
        review_requests = pull.get_review_requests()
        review_comments = pull.get_comments()
        for review_comment in review_comments:
            body = review_comment.body
            comment_user = review_comment.user





