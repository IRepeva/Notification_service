# Notification Service

GitHub link: https://github.com/IRepeva/notifications_sprint_1

## Description
Service allows to notify users about various events:
- Registration confirmation
- Movies watched per week and other analytics etc.

Notification API implements work with templates and events. 
More detailed information about endpoints is available 
[here](http://0.0.0.0/api/openapi) after project start (`docker-compose up --build`)

Currently service implements only email notifications, but can be 
easily extended with other types of notifications such as push or sms

Each Worker works with one queue (the name of the queue is passed through the parameters) and one Sender.

To add another Sender (for example for different type of notifications), 
the Worker class and another BaseSender implementation should be used 

## Get started
1. Create .env based on .env.example
2. Use `docker-compose up --build`
3. Use `make upgrade_db` to apply migration
