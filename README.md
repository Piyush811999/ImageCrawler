# Web Image Crawler 

## Overview

This is a simple **web image crawler** that downloads images from a given web page and its child pages up to a specified depth. It stores the results in an `crawler_images/` folder and logs all downloaded images in `crawler_images/index.json`.

## Installation

Ensure you have Python 3 installed, then install the required dependencies using:

```sh
pip install requests beautifulsoup4
```

## Usage

Run the crawler from the command line as follows:

```sh
python crawler.py <start_url> <depth>
```

- `start_url` - The URL where crawling begins.
- `depth` - The depth of crawling (e.g., `1` only crawls the given page, `2` crawls its child pages, etc.).

### Example:

```sh
python crawler.py https://example.com 2
```

## Output

- Images are saved in the `crawler_images/` folder.
- `crawler_images/index.json` contains a list of downloaded images with metadata:

```json
{
  "images": [
    {"url": "https://example.com/image.jpg", "page": "https://example.com", "depth": 1}
  ]
}
```

## Adding an Alias (Linux/macOS)

To run `crawl` instead of `python crawler.py`, add this alias:

```sh
echo "alias crawl='python crawler.py'" >> ~/.bashrc  # For Bash
source ~/.bashrc
```

Or for Zsh:

```sh
echo "alias crawl='python crawler.py'" >> ~/.zshrc
source ~/.zshrc
```

Now, you can run:

```sh
crawl https://example.com 2
```

## Notes

- Only images from the **same domain** as `start_url` are downloaded.
- The script uses **multi-threading** for faster crawling.
