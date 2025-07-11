import requests
from requests.exceptions import RequestException, ConnectionError, Timeout, TooManyRedirects 
from datetime import datetime, timedelta

def search_good_first_issues(languages, label="good first issue", max_stars=50, days_since_update=30):
    try:
        # github api endpoint for searching issues
        url = 'https://api.github.com/search/issues'
        if label == "":
            label = "good first issue"
        
        # split languages into a list of strings
        languages = languages.split()
        language_query = ' '.join([f'language:{lang}' for lang in languages])
        
        # calculate the date for recent updates (e.g., updated within last 30 days)
        recent_date = (datetime.now() - timedelta(days=days_since_update)).strftime('%Y-%m-%d')
        
        # parameters for the search query
        params = {
            'q': f'label:"{label}" {language_query} stars:1..{max_stars} updated:>{recent_date} state:open',
            'sort': 'updated',  # sort by most recently updated
            'order': 'desc',
            'per_page': 100  # get more results per page (max is 100)
        }
        
        # send get request to the github api
        response = requests.get(url, params=params)
        
        # check if the request was successful (status code 200)
        if response.status_code == 200:
            # parse the json response
            data = response.json()
            # extract the relevant information
            issues = data['items']
            
            # create a list of dictionaries with more detailed info
            issue_info = []
            for issue in issues:
                repo_info = {
                    'title': issue['title'],
                    'url': issue['html_url'],
                    'repo_name': issue['repository_url'].split('/')[-1],
                    'repo_owner': issue['repository_url'].split('/')[-2],
                    'updated_at': issue['updated_at'],
                    'comments': issue['comments']
                }
                issue_info.append(repo_info)
            
            return issue_info
        else:
            print(f"API request failed with status code: {response.status_code}")
            if response.status_code == 403:
                print("Rate limit exceeded. Try again later or use GitHub authentication.")
            return []
            
    except Timeout as err:
        print('error - the request timed out.')
    except ConnectionError as err:
        print('error - connection error! make sure you are connected to the internet.')
    except TooManyRedirects as err:
        print('too many redirects. check the url or website configuration.')
    except RequestException as err:
        print(f"an error occurred during the request: {err}")
    except Exception as err:
        print(f'an unexpected error occurred: {err}')
    
    # if the request was not successful return an empty list
    return []

# ask what languages you want to search for, saves as a string
languages = input("what languages are you looking to contribute in? please separate using spaces.\n")
label = input("\nplease input the label of the search(enter for default 'good first issue'): ")

# ask for max stars filter
max_stars_input = input("\nmax stars for repositories (enter for default 50): ")
max_stars = int(max_stars_input) if max_stars_input.strip() else 50

# ask for how recently updated
days_input = input("\nshow repos updated within how many days? (enter for default 30): ")
days_since_update = int(days_input) if days_input.strip() else 30

# call the function to retrieve the issue links
issue_info = search_good_first_issues(languages, label, max_stars, days_since_update)

# print the results with more detailed information
counter = 0
print(f"\n{'='*80}")
print(f"Found {len(issue_info)} good first issues:")
print(f"{'='*80}")

for issue in issue_info:
    counter += 1
    print(f"\n{counter}. {issue['title']}")
    print(f"   Repository: {issue['repo_owner']}/{issue['repo_name']}")
    print(f"   Updated: {issue['updated_at'][:10]}")  # show just the date
    print(f"   Comments: {issue['comments']}")
    print(f"   URL: {issue['url']}")
    print("-" * 40)

print(f'\nTotal issues found: {counter}')
print(f"Filters applied:")
print(f"  - Max stars: {max_stars}")
print(f"  - Updated within: {days_since_update} days")
print(f"  - Languages: {languages}")
print(f"  - Label: {label if label else 'good first issue'}")
