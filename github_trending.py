import requests
from datetime import date, timedelta


def get_date_days_ago(days_count):
    return date.today() - timedelta(days=days_count)


def get_trending_repositories(url_api, top_size, date_ago):
    url_search_repo = url_api + '/search/repositories'
    parameters = {
        'q': 'created:>={0}'.format(date_ago),
        'sort': 'stars',
        'per_page': '{0}'.format(top_size)
    }
    response = requests.get(url_search_repo, params=parameters)
    list_top_repo = response.json()['items']
    return list_top_repo


def get_open_issues_amount(url_api, repo_full_name):
    url_open_issues = url_api + '/repos/{0}/issues'.format(repo_full_name)
    open_issues_count = len(requests.get(url_open_issues).json())
    return open_issues_count


def print_repository(repo, open_issues):
    delimiter = '-' * 50
    print(delimiter)
    print(
        'Full name: {0}\n'
        'Stars: {1} Open issues: {2}\n'
        'Url: {3}'.format(
            repo['full_name'],
            repo['stargazers_count'],
            open_issues,
            repo['html_url']
        )
    )


if __name__ == '__main__':
    repo_count = 20
    days_ago = 7
    url_api = 'https://api.github.com'
    date_ago = get_date_days_ago(days_ago)
    try:
        top_repo = get_trending_repositories(url_api, repo_count, date_ago)
        for repo in top_repo:
            open_issues = get_open_issues_amount(url_api, repo['full_name'])
            print_repository(repo, open_issues)
    except requests.exceptions.ConnectionError:
        exit('Сheck your connection')
