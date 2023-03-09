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
CSV_FILE_STORING_LOCATION : where you want your csv file to be stored
CHROME_DATA_LOCATION : you need to add your chrome data location , if you don't know how you can follow this tutoriel  : https://www.howtogeek.com/255653/how-to-find-your-chrome-profile-folder-on-windows-mac-and-linux/
PROFILE_NAME : the profile name which your whatsapp web app exists
