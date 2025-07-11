from googlesearch import search
from bs4 import BeautifulSoup
import requests
from pytube import YouTube
import os

search_query = input("What do you want to search for on Google? ")

search_results = search(search_query, num_results=10)

video_urls = []

for search_result in search_results:
    response = requests.get(search_result)
    soup = BeautifulSoup(response.text, "html.parser")
    video_elements = soup.find_all("a", href=True)

    for video_element in video_elements:
        video_url = video_element["href"]
        if "youtube.com/watch" in video_url:
            video_urls.append(video_url)

directory_name = input("Enter a name for the directory to store the downloaded videos: ")
os.makedirs(directory_name, exist_ok=True)

for video_url in video_urls:
    yt = YouTube(video_url)
    video_title = yt.title
    file_path = os.path.join(directory_name, f"{video_title}.mp4")
    yt.streams.filter(progressive=True, file_extension="mp4").first().download(output_path=directory_name, filename=video_title)
    print(f"Video {video_title} has been downloaded to {file_path}")