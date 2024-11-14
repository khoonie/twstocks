# twstocks

## Institutional
This contains a script to scrape from https://tw.stock.yahoo.com/rank/foreign-investor-buy?exchange=TAI
The script then writes the data into the defaultdb.institutional in Digital Ocean DB
This script is deployed in Digital Ocean Functions and is triggered on weekdays 8PM

The scripts are deployed to Digital Ocean Functions using doctl command:
doctl serverless deploy <function-name>

### Adding additional scrapers
To add additional scraping deployments with similar database tables:

1. Copy the entire sub directory and rename the sub directory and the packages sub directory
2. make sure config.py is included in the sub directory where __main__.py is
3. change the URL to scrape and the DB table to write to in __main__.py 
4. deploy using doctl serverless deploy <function-name>


