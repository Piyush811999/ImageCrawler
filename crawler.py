import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
from concurrent.futures import ThreadPoolExecutor

# Function to download image from a URL
def download_image(img_url, page_url, depth, folder="crawler_images"):
    os.makedirs(folder, exist_ok=True)
    
    filename = os.path.basename(urlparse(img_url).path)
    # print(filename)

    if not filename or filename == "/":
        filename = f"image_{hash(img_url)}.jpg"  # Use hash as filename if no path is present
    
    print(f"Downloading: {img_url} to {filename}")

    filepath = os.path.join(folder, filename)

    try:
        response = requests.get(img_url, stream=True)
        response.raise_for_status()
        
        with open(filepath, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        
        return {"url": img_url, "page": page_url, "depth": depth}
    except requests.RequestException as e:
        print(f"Failed to download {img_url}: {e}")
        return None

# Function to crawl a URL recursively to a certain depth and download images
def crawl(start_url, depth, visited=set(), images=[]):
    if depth < 0 or start_url in visited:
        return images
    
    visited.add(start_url)
    print(f"Crawling: {start_url} at depth {depth}")
    
    try:
        response = requests.get(start_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve {start_url}: {e}")
        return images
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # downloading images in parallel
    with ThreadPoolExecutor() as executor:
        future_images = []
        for img_tag in soup.find_all("img"):
            img_url = img_tag.get("src")
            if img_url:
                img_url = urljoin(start_url, img_url)
                print(img_url)
                future = executor.submit(download_image, img_url, start_url, depth)
                future_images.append(future)
        
        for future in future_images:
            image_info = future.result() # wait for each result to complete before appending to images
            if image_info:
                images.append(image_info)
    
    # Find links for deeper crawling and crawl in parallel
    future_crawls = []
    if depth > 0:
        with ThreadPoolExecutor() as executor:
            for a_tag in soup.find_all("a", href=True):
                link = urljoin(start_url, a_tag["href"])
                if urlparse(link).netloc == urlparse(start_url).netloc:  # Only crawl same domain
                    future = executor.submit(crawl, link, depth - 1, visited, images)
                    future_crawls.append(future)
            
            for future in future_crawls:
                future.result()
    
    return images

# Function to save the image data in index.json
def save_index(images, folder="crawler_images"):
    os.makedirs(folder, exist_ok=True)
    index_file = os.path.join(folder, "index.json")
    
    if not os.path.exists(index_file):
        with open(index_file, "w") as f:
            json.dump({"images": []}, f, indent=4)
    
    with open(index_file, "w") as f:
        json.dump({"images": images}, f, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Web Image Crawler")
    parser.add_argument("start_url", type=str, help="Starting URL for crawling")
    parser.add_argument("depth", type=int, help="Depth of crawling")
    args = parser.parse_args()
    
    images = crawl(args.start_url, args.depth)
    save_index(images)
    print(f"Crawling finished. {len(images)} images saved in 'images' folder.")
    print(images)

if __name__ == "__main__":
    main()
