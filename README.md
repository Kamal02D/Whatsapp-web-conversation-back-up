# Whatsapp-web-conversation-back-up

## Project Description
This project uses Python and Selenium to automate WhatsApp web. The script can be used to extract data from the user's WhatsApp account, such as chat logs, message timestamps, and other metadata.

The script first loads the WhatsApp web app and waits for all the conversations to load. It then reads the messages that are currently on the screen and prints them. The user can also specify the conversation type (group or individual) and get the count of conversations.

The script also allows the user to scroll to the last element of the conversations and extract the message divs. It then filters the divs to only get the text messages and extracts data from the messages, such as message content, date and time, conversation type, group title, sender and receiver names, and sender and receiver phone numbers.

The extracted data is then stored in a CSV file for further analysis. The user can also specify the location and name of the CSV file to be generated.

## Important notes 
* this project only works on chrome
* this project only handle and collects text data 
* when running  the project the google chrome app should be closed 
* scraping through all the conversation might take a large amount of time
* this project assumes that you are logged in into your whasapp in chrome

## Things you might need to change 
(all of these variables are stacked in the begning of the script)
* CSV_FILE_STORING_LOCATION : where you want your csv file to be stored
* CHROME_DATA_LOCATION : you need to add your chrome data location , if you don't know how you can follow this tutoriel  : https://www.howtogeek.com/255653/how-to-find-your-chrome-profile-folder-on-windows-mac-and-linux/
* PROFILE_NAME : the profile name which your whatsapp web app exists
* you need also to find the chrome driver compatible with your chrome from here : https://chromedriver.chromium.org/downloads

## CSV file structure
## How CSV file looks looks like
| Message                                       | Date          | Time   | Conversation Type | Group Title      | Sender      | Receiver    | Sender Number | Receiver Number |
| --------------------------------------------- | ------------- | ------ | ---------------- | ---------------- | -----------| -----------| ------------- | --------------- |
| "Hi, how are you?"                            | 1/1/2022      | 12:30  | personal         |                  | John Doe    |             |               | 1234567890      |
| Can you send me that file?                    | 1/2/2022      | 10:15  | personal         |                  | Jane Smith  |             |               | 1987654321      |
| Meeting postponed to next week                | 1/3/2022      | 14:00  | group            | Marketing Team   |             |             |               |                 |
| "OK, thanks for letting us know"              | 1/3/2022      | 14:05  | group            | Marketing Team   | Jane Smith |             | 1987654321    |                 |
| I won't be able to attend the meeting         | 1/4/2022      | 9:30   | group            | Marketing Team   |             |             |                |                 |
| Is there anything we can do to help?          | 1/4/2022      | 9:35   | group            | Marketing Team   | Jane Smith |             | 1987654321    |                 |
| "Don't worry, I'll catch up with you later"   | 1/5/2022      | 17:00  | personal         |                  | Jane Smith  |             |1987654321 |                 |
| Can you pick up some milk on your way home?    | 1/6/2022      | 8:45   | personal         |                  |             | Jane Smith  |               |1987654321      |
| Here's the report you asked for               | 1/7/2022      | 11:00  | personal         |                  |             | Jane Smith  |               | 1987654321      |
| "Thanks, I'll take a look at it now"          | 1/7/2022      | 11:05  | personal         |                  |             | Jane Smith  |               | 1987654321      |
| Reminder: meeting tomorrow at 10am            | 1/8/2022      | 16:00  | group            | Marketing Team   |             |             |               |                 |
| Thanks for reminding us!                      | 1/8/2022      | 16:05  | group            | Marketing Team   | Jane Smith |             | 1987654321    |                 |
| Who's bringing the coffee?                    | 1/9/2022      | 9:00   | group            | Marketing Team   |             |             |               |                 |
| I can pick it up on my way to work            | 1/9/2022      | 9:05   | group            | Marketing Team   | Jane Smith |             | 1987654321    |                 |
| "Hello everyone, welcome to the group!"       | 1/10/2022     | 10:00  | group            | Marketing Team   |             |             |               |                 |
| Thanks for adding me to the group!            | 1/10/2022     | 10:05  | group           


