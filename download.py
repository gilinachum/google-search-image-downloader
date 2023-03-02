import requests
import re
import os

def download_images(search_string, min_size_kb=1, large_images_only=True):
    # The search URL
    URL = "https://www.google.com/search?q=" + search_string + "&tbm=isch"
    if large_images_only:
        URL += "&tbs=isz:l" # Large images only

    # User-Agent header to avoid blocking
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Send a GET request to the URL
    response = requests.get(URL, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the content of the response
        content = response.content.decode("utf-8")

        # Find all image URLs in the content
        #image_urls = re.findall('"(http[s]?://.*?\.(png|jpeg|jpg|gif))"', content)
        image_urls = re.findall("(http[s]?://[^\"]*?\.(png|jpeg|jpg|gif))", content)

        # Create a directory to store the images
        os.makedirs(search_string, exist_ok=True)

        # Download each image
        for i, url in enumerate(image_urls):
            url = url[0]
            print(url)
            try:
                response = requests.get(url, timeout=5)
                if len(response.content) < min_size_kb * 1024:
                        print(f"Image {i} is too small. Skipping...")
                        continue
                with open(f"{search_string}/{i}.jpg", "wb") as f:
                    f.write(response.content)
                    print(f"Image {i} downloaded successfully")
            except:
                print(f"Image {i} could not be downloaded")

    else:
        # If the request was not successful, print an error message
        print("An error occurred while downloading the images")

# Test the function
#search_string = "video in-game screen capture"
#search_string = '("ukraine" or "middle east" or "israeli") weapon'
search_string = 'wedding middle east'
download_images(search_string, min_size_kb=50)
