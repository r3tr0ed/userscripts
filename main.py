import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
class SeleniumBase:
    def __init__(self) -> None:
        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options)
    def getToken(self)



class DiscordAPICall:
    def checkResponse(self,response, requestType, url):
        if response.ok:
            if response.json():
                return response.json()
            else:
                return response.text
        else:
            print("HTTP STATUS CODE:", response.status_code, f"- {requestType} error for url:", url)

    def postUrl(self, url, headers):
        response = requests.post(url, headers=headers)
        self.checkResponse(response, "POST", url)


    def getUrl(self, url, headers=None):
        if headers:
            response = requests.get(url, headers=headers)
        else:
            response = requests.get(url)
        self.checkResponse(response, "GET", url)

discordApiCall = DiscordAPICall()
def discordInviteCallback(inviteId, counts_included, has_expiration):
    baseinviteApiUrl = f"https://discord.com/api/v9/invites/{inviteId}?inputValue={inviteId}&with_counts={counts_included}&with_expiration={has_expiration}"
    discordApiCall.getUrl(baseinviteApiUrl)

def discordMessagePost(message, channelId):
    baseinviteApiUrl = f"https://discord.com/api/v9/channels/{channelId}/messages"
    headers = {}
    discordApiCall.getUrl(baseinviteApiUrl, )
