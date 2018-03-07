import requests
from datetime import date, timedelta


def get_date_days_ago(days_count):
    return date.today() - timedelta(days=days_count)


def get_trending_repositories(top_size, days_ago):
    date_ago = get_date_days_ago(days_ago)
    url_search_repo = 'https://api.github.com/search/repositories'
    parameters = {
        'q': 'created:>={0}'.format(date_ago),
        'sort': 'stars',
        'per_page': '{0}'.format(top_size)
    }
    raw_top_repo = requests.get(url_search_repo, params=parameters)
    list_top_repo = raw_top_repo.json()['items']
    return list_top_repo


def get_most_usable_repositories(repo):
    return sorted(repo, key=lambda x: x['open_issues'])


def print_repositoies(repositories):
    print('Most usable repositories:')
    delimiter = '-' * 50
    for repo in repositories:
        name = repo['full_name']
        stars = repo['stargazers_count']
        open_issues = repo['open_issues']
        url = repo['html_url']
        print(delimiter)
        print(
            'Name: {0}\n'
            'Stars: {1} Open issues: {2}\n'
            'Url: {3}'.format(name, stars, open_issues, url)
        )


if __name__ == '__main__':
    repo_count = 20
    days_ago = 7
    try:
        top_repo = get_trending_repositories(repo_count, days_ago)
        most_usable_repo = get_most_usable_repositories(top_repo)
        print_repositoies(most_usable_repo)
    except requests.exceptions.ConnectionError:
        exit('Сheck your connection')
    except IndexError:
        exit('Received data are not correct')
