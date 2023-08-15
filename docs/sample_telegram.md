### Text message
```json
{
  "update_id": 532599280,
  "message": {
    "message_id": 96,
    "from": {"id": 6373657192, "is_bot": false, "first_name": "Sunil", "last_name": "D Shashidhara", "language_code": "en"},
    "chat": {"id": 6373657192, "first_name": "Sunil", "last_name": "D Shashidhara", "type": "private"},
    "date": 1691062374,
    "text": "hello"}
}
```

### Button click callback
```json
{
  "update_id": 532599588,
  "callback_query": {
    "id": "965958200212072193",
    "from": {
      "id": 6667355613,
      "is_bot": false,
      "first_name": "kartik",
      "last_name": "malhotra",
      "language_code": "en"
    },
    "message": {
      "message_id": 796,
      "from": {
        "id": 6432446944,
        "is_bot": true,
        "first_name": "BotMother",
        "username": "randombum_bot"
      },
      "chat": {
        "id": 6667355613,
        "first_name": "kartik",
        "last_name": "malhotra",
        "type": "private"
      },
      "date": 1691573532,
      "text": "Options",
      "reply_markup": {
        "inline_keyboard": [
          [
            {
              "text": "Option 1",
              "callback_data": "1"
            },
            {
              "text": "Option 2",
              "callback_data": "2"
            }
          ],
          [
            {
              "text": "Option 3",
              "callback_data": "3"
            },
            {
              "text": "Option 4",
              "callback_data": "4"
            }
          ]
        ]
      }
    },
    "chat_instance": "-8590976206145214552",
    "data": "2"
  }
}
```
