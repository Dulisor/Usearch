# Usearch
A powerful username search tool that scans for a username across multiple social media platforms using both built-in site list and the Sherlock project.

<img width="1853" height="627" alt="Img" src="https://github.com/user-attachments/assets/44496852-a699-476b-87c3-37a8103dfdc8" />

## Features

* Dual Search Methods: Choose between built-in site list or Sherlock CLI

* Multi-threaded Scanning: Fast concurrent checks using ThreadPoolExecutor

* Comprehensive Results: Saves detailed results with timestamps

* User-friendly Interface: Interactive CLI with clear status indicators

* Flexible Configuration: Easy to modify site list in config.py

## Quick Start
### Prerequisites

* ```Python``` 3.6 or higher
* ```pip``` (Python package manager)

## Installation

### Clone the repository
```bash
git clone https://github.com/Dulisor/Usearch
cd Usearch
```

### Install required packages

```bash
pip install -r requirements.txt
```

### Verify Sherlock installation

```bash

sherlock --help
```
## Usage

### Run the script

```bash

python main.py
```
<img width="800" height="420" alt="GIF" src="https://github.com/user-attachments/assets/3a0216bc-0188-4277-b47d-66b42702b9aa" />


### Example Output
```    
Enter username to search: johndoe
Input 'S' for Sherlock or 'B' for Built-In Site list from the config.py file: B
Searching for: johndoe
-------------------------------------------------------
[+] Linktree     User Found      | https://linktr.ee/johndoe
[+] Reddit       User Found      | https://www.reddit.com/user/johndoe
[+] Twitch       User Found      | https://www.twitch.tv/johndoe
[?] Medium       Error(403)
[-] YouTube      User Not Found  | https://www.youtube.com/@johndoe
[+] Instagram    User Found      | https://www.instagram.com/johndoe/
[+] Steam        User Found      | https://steamcommunity.com/id/johndoe
[+] GitHub       User Found      | https://github.com/johndoe
[+] Twitter/X    User Found      | https://x.com/johndoe
[+] Pinterest    User Found      | https://www.pinterest.com/johndoe/
[+] GitLab       User Found      | https://gitlab.com/johndoe
[?] TikTok       Error

[✓] Results saved to: johndoe.txt
```
## Configuration
### Built-in Sites (```config.py```)
```python
SITES = {
    "GitHub": "https://github.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "Twitter/X": "https://x.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "Steam": "https://steamcommunity.com/id/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Linktree": "https://linktr.ee/{}",
    "Medium": "https://medium.com/@{}",
}
```
## Headers

### Customize User-Agent in ```config.py```:
```python

HEADERS = {"User-Agent": "Your custom user agent here"}
```

## Output Format

###Results are saved in a structured text file:

```text
Username Search Results for: johndoe
Search Method: Built-in Site List
Date: 2026-09-01 20:09:01
============================================================

[+] Linktree        FOUND     | https://linktr.ee/johndoe
[+] Reddit          FOUND     | https://www.reddit.com/user/johndoe
[+] Twitch          FOUND     | https://www.twitch.tv/johndoe
[?] Medium          Error(403)
[-] YouTube         NOT FOUND | https://www.youtube.com/@johndoe
[+] Instagram       FOUND     | https://www.instagram.com/johndoe/
[+] Steam           FOUND     | https://steamcommunity.com/id/johndoe
[+] GitHub          FOUND     | https://github.com/johndoe
[+] Twitter/X       FOUND     | https://x.com/johndoe
[+] Pinterest       FOUND     | https://www.pinterest.com/johndoe/
[+] GitLab          FOUND     | https://gitlab.com/johndoe
[?] TikTok          Error

============================================================
Summary: 9 found, 1 not found, 2 errors
Total sites checked: 12
```

## Performance Tips
* Built-in method: Faster, checks ~12 sites

* Sherlock method: More comprehensive, checks 300+ sites

* Threading: Uses 15 concurrent workers for optimal speed

* Timeout: 8 seconds per request to prevent hanging

## Troubleshooting
### Common Issues

#### 1. Sherlock not found
```bash
pip install sherlock-project
```

#### 2. SSL Certificate Errors
```bash
pip install --upgrade certifi
```

#### 3. Rate Limiting

* Some sites may temporarily block multiple requests
* Wait a few minutes and try again

#### 4. Username length validation
* Minimum: 4 characters
* Maximum: 15 characters

## Disclaimer

This tool is for educational and legitimate research purposes only. Users are responsible for:

* Complying with each platform's Terms of Service

* Not using the tool for harassment or stalking

* Respecting privacy and data protection laws

## Contributing

Contributions are welcome! Please:

* Fork the repository
* Create a feature branch
* Submit a pull request

## License
This project is licensed under the GNU General Public License.

* Sherlock Project - The comprehensive username search tool

* All contributors and users of this tool
