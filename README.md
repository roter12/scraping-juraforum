# Scraping tool for www.juraforum.de

## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Input the following command.

   ```bash
   python -m pip install beautifulsoup4 pandas requests selenium argparse
   ```

## Run

   Input the following command.

   ```bash
   > python juraforum.py -s <start_page_number> -e <end_page_number>
   ```

   Results save as a 'result.json' file.