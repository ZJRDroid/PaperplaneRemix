import requests

from userbot.events import register
from userbot.utils import parse_arguments


@register(outgoing=True, pattern=r"^.docs\s+(.*)")
async def doc_search(e):
    params = e.pattern_match.group(1)
    args, lib = parse_arguments(params, ['version'])
    lib = lib.strip()

    version = int(args.get('version', 3))
    python_url = f"https://docs.python.org/{version}/library/{lib}.html"
    pip_url = f"https://pypi.org/project/{lib}/"

    await e.edit(f"Searching docs for `{lib}`...")
    if requests.get(python_url).status_code == 200:
        response = f"[Check out the Python {version} docs for {lib}]({python_url}).\nI think you'll find it useful."
    elif requests.get(pip_url).status_code == 200:
        readthedocs_url = f"https://readthedocs.org/projects/{lib}/"
        if requests.get(readthedocs_url).status_code == 200:
            response = f"[Check out the docs for {lib} on readthedocs]({readthedocs_url}).\nI think you'll find it useful."

    if response:
        await e.edit(response)
    else:
        await e.edit(f"No docs found for `{lib}`...", delete_in=3)