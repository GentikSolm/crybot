# crybot
Tracks how often you be cryin

### Setup

First, go to [discords application portal](https://discord.com/developers/applications) and create a
new application.
Next, go the `bot` section of the application on the right hand side, and create a new bot.
From there, grab the bot `token`, and then navigate to OAuth2 -> URL Generator and generate an invite link with
`bot` and `application.commands` permissions. It should look something like this  
`https://discord.com/api/oauth2/authorize?client_id=<Your bots client ID>&permissions=0&scope=bot%20applications.commands`

Finally, place your `token` in the `.env` file, along with the mongo db url. Feel free to use the `sample.env` file.

### Testing
To test locally, start the system with `just up`. This will build and run the ecosystem. You can watch the logs via
`docker compose logs -f bot`

