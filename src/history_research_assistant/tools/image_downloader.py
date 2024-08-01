from typing import List
import requests


from crewai_tools import BaseTool


class ImagesDownloader(BaseTool):
    name: str = "Images Downloader"
    description: str = (
        "Accepts a list of public URLs pointing to images, and downloads them into the local directory. \
        Returns the the URLs that succeeded and failed as a python dict"
    )


    def download_images(self, urls, file_names):

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
        
        successes = []
        failures = []

        for url,file_name in zip(urls, file_names):

            response = requests.get(url, headers=headers)
            
            # Check if the request was successful
            if response.status_code == 200:
                # Open a file in binary write mode and write the content of the image
                with open(f"downloads/{file_name}", 'wb') as file:
                    file.write(response.content)
                successes.append(url)
            else:
                failures.append(url)
        
        return successes, failures


    def _run(self, image_urls: List[str], file_names: List[str]) -> dict:

        successes, fails = self.download_images(image_urls, file_names)

        return {"successes":successes, "failures":fails}
