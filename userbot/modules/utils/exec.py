import asyncio
from os import remove
from sys import executable

from userbot import BOTLOG, BOTLOG_CHATID
from userbot.events import register


@register(outgoing=True, pattern=r"^.exec(?:\s+|$)([\s\S]*)")
async def run(event):
    """ For .exec command, which executes the dynamically created program """
    reply_message = await event.get_reply_message()

    if event.pattern_match.group(1):
        code = event.pattern_match.group(1)
    elif reply_message:
        code = reply_message.text
    else:
        await event.edit("``` At least a variable is required to \
execute. Use .help exec for an example.```")
        return

    if event.is_channel and not event.is_group:
        await event.edit("`Exec isn't permitted on channels!`")
        return

    if code in ("userbot.session", "config.env"):
        await event.edit("`That's a dangerous operation! Not Permitted!`")
        return

    if len(code.splitlines()) <= 5:
        codepre = code
    else:
        clines = code.splitlines()
        codepre = clines[0] + "\n" + clines[1] + "\n" + clines[2] + \
                  "\n" + clines[3] + "..."

    command = "".join(f"\n {l}" for l in code.split("\n.strip()"))
    process = await asyncio.create_subprocess_exec(
        executable,
        '-c',
        command.strip(),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) \
             + str(stderr.decode().strip())

    if result:
        if len(result) > 4096:
            file = open("output.txt", "w+")
            file.write(result)
            file.close()
            await event.client.send_file(
                event.chat_id,
                "output.txt",
                reply_to=event.id,
                caption="`Output too large, sending as file`",
            )
            remove("output.txt")
            return
        await event.edit("**Query: **\n`"
                         f"{codepre.strip()} \n"
                         "`\n**Result: **\n`"
                         f"{result}"
                         "`")
    else:
        await event.edit("**Query: **\n`"
                         f"{codepre.strip()} \n"
                         "`\n**Result: **\n`No Result Returned/False`")

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "Exec query " + codepre + " was executed successfully")
