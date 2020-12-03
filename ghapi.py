from time import sleep
import datetime
import requests
from requests.auth import HTTPBasicAuth
import pprint

BASE_URL = "https://api.github.com"
HEADERS = {"Accept": "application/vnd.github.full+json"}
RATE_LIMIT_URL = 'https://api.github.com/rate_limit'


class GitHubAPI:
    def __init__(self, username, password):
        self.request_count = 0
        self.authentication = HTTPBasicAuth(username, password)
        self.rate_limit = self.get_rate_limit()
        self.start_time = datetime.datetime.now()

    def add_request(self):
        self.request_count += 1
        elapsed = datetime.datetime.now() - self.start_time
        remaining = datetime.timedelta(hours=1) - elapsed
        print("elapsed: " + str(elapsed.total_seconds()) + " remaining:" + str(
            remaining.total_seconds()))

        if self.request_count == self.rate_limit:
            self.request_count = 0
            sleep(remaining.total_seconds()
                  + datetime.timedelta(minutes=1).total_seconds())

    # Rate Limit
    def get_rate_limit(self):
        res = requests.get(RATE_LIMIT_URL,
                            headers=HEADERS, auth=self.authentication).json()
        pprint.pprint(res)
        metrics = res['rate']['limit']
        return metrics
    
    # Review Comments
    def get_pull_requests(self, owner, repo):
        self.add_request()
        return self.gather_pages(requests.get(BASE_URL + "/repos/" + owner + "/" + repo + "/pulls",
                            headers=HEADERS, auth=self.authentication).json())

    def get_pull_request(self, owner, repo, number):
        self.add_request()
        return self.gather_pages(requests.get(BASE_URL + "/repos/" + owner + "/" + repo + "/pulls",
                            headers=HEADERS, auth=self.authentication).json())
    
    # Review
    def get_reviews_for_pull_request(self, owner, repo, number):
        self.add_request()
        return self.gather_pages(requests.get(BASE_URL + "/repos/" + owner + "/" + repo + "/pulls/"
                                + str(number) + "/reviews", headers=HEADERS, auth=self.authentication).json())

    def get_single_review(self, owner, repo, number, review_id):
        self.add_request()
        return self.gather_pages(requests.get(BASE_URL + "/repos/" + owner + "/" + repo + "/pulls/"
                            + str(number) + "/reviews/"
               + review_id, headers=HEADERS, auth=self.authentication).json())
    
    def get_comments_for_a_single_review(self, owner, repo, number, review_id):
        self.add_request()
        return self.gather_pages(requests.get(BASE_URL + "/repos/" + owner + "/" + repo + "/pulls/"
                            + str(number) + "/reviews/"
                + review_id + "/comments", headers=HEADERS, auth=self.authentication).json())
    
    # Review Requests
    def get_review_requests_for_pull_request(self, owner, repo, number):
        self.add_request()
        return self.gather_pages(requests.get(BASE_URL + "/repos/" + owner + "/" + repo + "/pulls/"
                            + str(number)
               + "/requested_reviewers", headers=HEADERS, auth=self.authentication).json())
    
    def get_pull_request_comments(self, owner, repo, number):
        self.add_request()
        return self.gather_pages(requests.get(BASE_URL + "/repos/" + owner + "/" + repo + "/pulls/"
                            + number + "/comments",
                            headers=HEADERS, auth=self.authentication).json())
    
    def get_all_pull_request_comments(self, owner, repo):
        self.add_request()
        return self.gather_pages(requests.get(BASE_URL + "/repos/" + owner + "/" + repo
                            + "/pulls/comments",
                            headers=HEADERS, auth=self.authentication).json())
    
    def get_single_comment(self, owner, repo, comment_id):
        self.add_request()
        return self.gather_pages(requests.get(BASE_URL + "/repos/" + owner + "/" + repo
                            + "/pulls/comments/" + comment_id,
                            headers=HEADERS, auth=self.authentication).json())

    # Organization
    def get_organization(self, organization):
        self.add_request()
        return self.gather_pages(requests.get(BASE_URL + '/orgs/' + organization))

    # Repos
    def get_repositories(self, organization):
        self.add_request()
        return self.gather_pages(requests.get(BASE_URL + '/orgs/' + organization + '/repos'))

    @staticmethod
    def gather_pages(req):
        reviews = []
        while True:
            res = req
            pprint.pprint(res)
            reviews.append(res)
            if not res.links["next"] or res.links["next"] == '' or res.links['next'] is None:
                break
        return reviews
