# Wutbot

This is a very simple program that takes a slack command from a user and searches for their input in a Google Spreadsheet. It then returns the definition of that item.

A major issue with this is that the search is currently case sensitive. To overcome this, I spent like two days messing with different libraries and struggling. Instead, I just added a few extra columns to the spreadsheet itself that create all caps or all lowercase versions of every entry automatically.

The credentials file, wutbot.json, is not included because it contains API Token information. You'll need to generate your own. More details here: https://developers.google.com/identity/protocols/OAuth2ServiceAccount

I'm storing the URL for the spreadsheet itself as an environment variable because this is a public repo. In practice, you'll probably just hardcode yours in.