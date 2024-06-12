import requests
from bs4 import BeautifulSoup
import re
import schedule
import time

# List of Twitter accounts to scrape
twitter_accounts = [
    "https://twitter.com/Mr_Derivatives",
    "https://twitter.com/warrior_0719",
    "https://twitter.com/ChartingProdigy",
    "https://twitter.com/allstarcharts",
    "https://twitter.com/yuriymatso",
    "https://twitter.com/TriggerTrades",
    "https://twitter.com/AdamMancini4",
    "https://twitter.com/CordovaTrades",
    "https://twitter.com/Barchart",
    "https://twitter.com/RoyLMattox"
]

# Function to scrape Twitter for stock symbol mentions
def scrape_twitter(twitter_accounts, stock_symbol):
    count = 0
    stock_symbol_regex = re.compile(re.escape(stock_symbol), re.IGNORECASE)
    
    for account in twitter_accounts:
        try:
            response = requests.get(account)
            print(response.status_code)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                tweets = soup.find_all('div', {'data-testid': 'tweetText'})
                print('tweets: ', tweets)
                for tweet in tweets:
                    tweet_text = tweet.get_text()
                    print('tweet text: ', tweet_text)
                    mentions = stock_symbol_regex.findall(tweet_text)
                    count += len(mentions)
            else:
                print(f"Failed to retrieve data from {account}")
        except Exception as e:
            print(f"An error occurred while scraping {account}: {e}")
    
    return count

# Function to perform scraping and display results
def perform_scraping(twitter_accounts, stock_symbol, interval):
    count = scrape_twitter(twitter_accounts, stock_symbol)
    print(f"'{stock_symbol}' was mentioned '{count}' times in the last '{interval}' minutes.")

# Main function to input parameters and schedule scraping
def main():
    stock_symbol = input("Enter the stock symbol to look for (e.g., $TSLA): ")
    interval = int(input("Enter the time interval for scraping in minutes: "))

    # Schedule the scraping job
    schedule.every(interval).minutes.do(perform_scraping, twitter_accounts, stock_symbol, interval)

    # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
