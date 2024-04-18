# Schedule Spider Project

This project utilizes Scrapy, an open-source web crawling framework, to monitor changes on a specified website and sends notifications via GroupMe when changes are detected.

## Getting Started

### Prerequisites

- Python 3
- Scrapy
- Requests

You can install Scrapy and Requests using pip:

pip install Scrapy requests

## Project Setup


### Start a New Scrapy Project
If you haven't already created a Scrapy project, you can start one using the following command:


scrapy startproject schedule_project

Navigate into your project directory:

cd schedule_project

Add the Spider:
Save the provided Python script as schedule_spider.py inside the spiders directory of your Scrapy project.

### Create a Secrets File:
You need to create a secrets.json file in the same directory as your spider script (schedule_spider.py). This file should contain necessary credentials or tokens. Here is an example format for the file (secrets.json):

{
  "GROUPME_BOT_ID": "your_bot_id_here"
}

Make sure to replace "your_bot_id_here" with your actual GroupMe bot ID.

### Configuration
Update the Website URL: Ensure the start_urls list in schedule_spider.py contains the correct URL you want to monitor for changes.

start_urls = ['https://example.com/target-page'] (Ask the Coach for the CYO site)
Replace 'https://example.com/target-page' with the URL of the website you wish to monitor.

### Running the Project
To run the spider and start monitoring for changes, use the following command from the root of your Scrapy project:

scrapy crawl schedule

This command instructs Scrapy to run the spider named schedule, which is defined by the name attribute in the ScheduleSpider class.

### Monitoring Changes
The spider automatically compares the current version of the webpage with the previously fetched version stored in previous_data.txt. If any changes are detected, it logs the change and sends a notification through GroupMe. The results of each crawl are stored in scraped_data.txt.


Scheduling Runs: For continuous monitoring, I use a CRON job


Troubleshooting
If you encounter issues with not receiving notifications, ensure the GroupMe bot ID is correct and that your network settings allow outbound HTTP requests to the GroupMe API.
