# Currency Rates Scraper

Automated daily scraper for currency rates using GitHub Actions.

## Data Sources
- Currency rates from Bonbast.com
- Scraped every 3 hours per day

## Workflow
- Scrapes currency rates
- Logs data to `logs/currency_rates.csv`
- Automatically updates on schedule

## Fix
- Fixed js loading time out
