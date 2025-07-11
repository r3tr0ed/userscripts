import requests
from requests.exceptions import RequestException, ConnectionError, Timeout,TooManyRedirects 
def search_good_first_issues(languages, label="good first issue"):
    try:
        # github api endpoint for searching issues
        url = 'https://api.github.com/search/issues'
        if label == "":
            label = "good first issue"
        # split languages into a list of strings
        languages = languages.split()
        language_query = ' '.join([f'language:{lang}' for lang in languages])
        # parameters for the search query
        params = {
            'q': f'label:"{label}" {language_query}',
            'sort': 'created',
            'order': 'desc',
            'per_page': 100
        }
        # send get request to the github api
        response = requests.get(url, params=params)
        # check if the request was successful (status code 200)
        if response.status_code == 200:
            # parse the json response
            data = response.json()
            # extract the relevant information
            issues = data['items']
            issue_links = [issue['html_url'] for issue in issues]
        # return the list of issue links
            return issue_links
    except Timeout as err:
        print('error - the request timed out.')
    except ConnectionError as err:
        print('error - connection error! make sure you are connected to the internet.')
    # too many redirects is when the url points to 1 url which points back to the first url, meaning
    # it's stuck in a loop. eventually your browser gives up and displays the 'too many redirects' error
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
# call the function to retrieve the issue links
issue_links = search_good_first_issues(languages, label)
# print the links
# displays the number of links printed
counter = 0
for link in issue_links:
    counter += 1
    print(link)
print(f'number of links: {counter}')
