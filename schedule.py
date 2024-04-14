import scrapy
import os
import json
import requests
from difflib import Differ

class ScheduleSpider(scrapy.Spider):
    name = 'schedule'
    allowed_domains = ['archsacyo.sportspilot.com']
    start_urls = ['https://archsacyo.sportspilot.com/scheduler/mobile/public/Report.aspx?contest=4329&team=23334&reportType=schedule']
    data_file = 'previous_data.txt'  # File to store the last scrape data

    def __init__(self, *args, **kwargs):
        super(ScheduleSpider, self).__init__(*args, **kwargs)
        secrets_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'secrets.json')
        with open(secrets_path, 'r') as file:
            self.secrets = json.load(file)

    def normalize_space(self, text):
        """Normalize whitespace and replace non-breaking spaces."""
        return ' '.join(text.replace(u'\xa0', u' ').split())

    def parse(self, response):
        # Extract only visible text, excluding script and style elements
        text_blocks = response.xpath('//body//*[not(self::script or self::style)]/text()').getall()
        current_data = ' '.join([self.normalize_space(text) for text in text_blocks if text.strip()])
        previous_data = self.load_previous_data()

        # Write the current scraped data to a file
        with open('scraped_data.txt', 'w') as file:
            file.write(current_data)

        if current_data != previous_data:
            self.log('Change detected.')
            change_details = self.find_changes(previous_data, current_data)
            self.send_notification(change_details)
            self.save_current_data(current_data)
        else:
            self.log('No change detected.')

    def load_previous_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                last_data = file.read()
            return last_data
        return ''

    def save_current_data(self, data):
        with open(self.data_file, 'w') as file:
            file.write(data)

    def send_notification(self, message):
        if message:
            self.send_groupme_message(self.secrets['GROUPME_BOT_ID'], message)

    def send_groupme_message(self, bot_id, message):
        url = 'https://api.groupme.com/v3/bots/post'
        headers = {'Content-Type': 'application/json'}
        data = {
            'bot_id': bot_id,
            'text': message
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 202:
            self.log("Message sent to GroupMe successfully.")
        else:
            self.log(f"Failed to send message to GroupMe. Status code: {response.status_code}, Response: {response.text}")

    def find_changes(self, old_text, new_text):
        d = Differ()
        diff = list(d.compare(old_text.split(), new_text.split()))
        added = [line[2:].strip() for line in diff if line.startswith('+ ')]
        removed = [line[2:].strip() for line in diff if line.startswith('- ')]

        message = "There has been an update to the schedule:\n"
        if added:
            message += "Added: " + ' '.join(added) + "\n"
        if removed:
            message += "Removed: " + ' '.join(removed)

        return message if added or removed else ''
