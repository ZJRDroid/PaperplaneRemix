from github import InputFileContent

from userbot import github
from userbot.events import register


@register(outgoing=True, pattern=r"^.gist\s+([\S]+)\s+([\S\s]+)")
async def create_gist(e):
    if not github:
        await e.edit("Github information has not been set up", delete_in=3)
        return

    filename = e.pattern_match.group(1)
    match = e.pattern_match.group(2)
    reply_message = await e.get_reply_message()

    if match:
        message = match.strip()
    elif reply_message:
        message = reply_message.message.strip()
    else:
        await e.edit("There's nothing to paste.")
        return

    await e.edit("`Sending paste to Github...`")

    user = github.get_user()
    file = InputFileContent(message)
    gist = user.create_gist(True, {filename: file})

    await e.edit(f"Gist created. You can find it here {gist.html_url}.")
