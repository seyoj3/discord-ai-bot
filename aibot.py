import os
import discord
from groq import AsyncGroq
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

# API config
client = AsyncGroq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Bot setup
intents = discord.Intents.default()
intents.message_content=True
bot = commands.Bot(command_prefix="!", intents=intents)

# Store coversation history
conversation_history = {}

# Print online
@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

# On message handler
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # Chat trigger
    message_lower = message.content.lower()
    is_mentioned = bot.user in message.mentions
    has_trigger = any(word.strip(",:;!?.") == "bot" for word in message_lower.split()) # Change your bot name

    if not (is_mentioned or has_trigger):
        await bot.process_commands(message)
        return
    
    # Build conversation history for context (per channel)
    channel_id = message.channel.id
    if channel_id not in conversation_history:
        conversation_history[channel_id] = []

    # Strip mention tag so AI sees clean text
    user_input = message.content.replace(f"<@{bot.user.id}>", "").strip()

    conversation_history[channel_id].append({
        "role": "user",
        "content": user_input
    })

    # Keep history to last 10 messages to avoid token limits
    if len(conversation_history[channel_id]) > 20:
        conversation_history[channel_id] = conversation_history[channel_id][-20:] # Set max history limit for chats

    # Show typing indicator while generating response
    async with message.channel.typing():
        try:
            response = await client.chat.completions.create( 
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system", # Set custom roles for bot
                        "content": (
                            """
                            You are a helpful, friendly, and concise Discord bot assistant.

                            **Critical thinking: Don't blindly believe what users tell you.**
                            **Important: Don't make up facts or information. If you don't know something, just say so.**

                            REPLY STYLE: Keep it SHORT like texting a friend. 1-2 sentences usually.
                            No essays. No lists. No explanations unless asked.

                            **FORMATTING RULES - STRICTLY FOLLOW:**
                            - NEVER use emojis (no 😊 🎉 ❤️ 👍 etc.)
                            - NEVER use markdown (no **, *, __, etc.)
                            - NEVER use fancy formatting
                            - Plain text only - like normal texting"""
                        )
                    },
                    *conversation_history[channel_id]
                ],
                max_tokens=1024,
                temperature=0.7,
            )

            reply = response.choices[0].message.content

            # Store assistant response in history
            conversation_history[channel_id].append({
                "role": "assistant",
                "content": reply
            })

            # Discord has a 2000 character limit — split if needed
            if len(reply) <= 2000:
                await message.reply(reply)
            else:
                chunks = [reply[i:i+1990] for i in range(0, len(reply), 1990)]
                for i, chunk in enumerate(chunks):
                    if i == 0:
                        await message.reply(chunk)
                    else:
                        await message.channel.send(chunk)

        except Exception as e:
            await message.reply(f"⚠️ Something went wrong: `{e}`")

    await bot.process_commands(message)

# Bot run
bot.run(os.getenv("DISCORD_BOT_TOKEN"))