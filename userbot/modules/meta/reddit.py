import re

from telethon import events
from telethon.errors import MessageNotModifiedError

from ..help import add_help_item
from userbot import bot


@bot.on(events.NewMessage())
async def subreddit(e):
    message = e.text
    matches = re.findall(r"(/?r/\S+)", message)
    if matches:
        print("REDDIT")
        for match in matches:
            sub_name = match.split('/')[-1]
            link = f"[{match}](https://reddit.com/r/{sub_name})"
            message = e.text.replace(match, link)

        try:
            await e.edit(message)
        except MessageNotModifiedError:
            pass


add_help_item(
    "reddit",
    "Meta",
    "Replaces subreddit text with a link to the sub.",
    """
    `r/indianpeoplefacebook`
    """
)
