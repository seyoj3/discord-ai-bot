# AI Discord Bot

A simple Discord bot that lets you chat with an AI directly in your server. It uses Groq's API to run Llama 3.1 under the hood, so responses are fast. The bot remembers the last 20 messages per channel so it has some context for the conversation.

## How it works

You can talk to the bot by either mentioning it (`@botname`) or just saying "bot" somewhere in your message. It'll reply in plain, conversational text — no markdown walls, no emoji spam, just normal responses.

Each channel gets its own conversation history, so chats in #general and #random are kept separate.

## Setup

**1. Clone the repo and install dependencies**

```bash
pip install discord.py groq python-dotenv
```

**2. Create a `.env` file in the project root**

```
DISCORD_BOT_TOKEN=your_discord_bot_token_here
GROQ_API_KEY=your_groq_api_key_here
```

**3. Get your tokens**

- **Discord token** — go to the [Discord Developer Portal](https://discord.com/developers/applications), create an app, add a bot, and copy the token. Make sure to enable the **Message Content Intent** under the bot settings or it won't be able to read messages.
- **Groq API key** — sign up at [groq.com](https://groq.com) and grab a free API key.

**4. Invite the bot to your server**

In the Developer Portal, go to OAuth2 → URL Generator. Select `bot` as the scope and give it `Send Messages`, `Read Message History`, and `Read Messages/View Channels` permissions. Open the generated URL and add it to your server.

**5. Run it**

```bash
python aibot.py
```

You should see `YourBot#1234 is online!` in the terminal when it's ready.

## Customization

- **Trigger word** — the bot currently listens for the word "bot". To change it, find this line and swap it out:
  ```python
  has_trigger = any(word.strip(",:;!?.") == "bot" for word in message_lower.split())
  ```
- **AI model** — it uses `llama-3.1-8b-instant` by default. You can swap this for any model available on Groq (like `llama-3.3-70b-versatile` if you want something more capable).
- **Personality** — edit the `system` prompt in the `messages` list to change how the bot talks or what role it plays.
- **Memory length** — the bot keeps the last 20 messages per channel. Change the `20` in the history trimming logic to whatever works for you.

## Notes

- Discord has a 2000 character limit per message. If the AI writes something longer, the bot will automatically split it into chunks.
- Conversation history is stored in memory, so it resets every time you restart the bot.
- The bot ignores messages from other bots to avoid feedback loops.
