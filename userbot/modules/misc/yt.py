from html import unescape

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ..help import add_help_item
from userbot import YOUTUBE_API_KEY
from userbot.events import register
from userbot.utils import parse_arguments


@register(outgoing=True, pattern=r"^\.yt (.*)")
async def yt_search(video_q):
    """ For .yt command, do a YouTube search from Telegram. """
    query = video_q.pattern_match.group(1)
    result = ''

    if not YOUTUBE_API_KEY:
        await video_q.edit("`Error: YouTube API key missing!\
            Add it to environment vars or config.env.`")
        return

    opts, query = parse_arguments(query, ['limit' 'order'])
    limit = opts.get('limit', 5)
    order = opts.get('order', 'relevance')

    await video_q.edit("Processing search query...")

    full_response = youtube_search(query, order, limit)
    videos_json = full_response[1]

    i = 1
    for video in videos_json:
        result += f"{i}. [{unescape(video['snippet']['title'])}](https://www.youtube.com/watch?v={video['id']['videoId']}) \n"
        i += 1

    reply_text = f"**Search Query:**\n`{query}`\n\n**Result:**\n{result}"

    await video_q.edit(reply_text)


def youtube_search(query,
                   order="relevance",
                   limit=5,
                   token=None,
                   location=None,
                   location_radius=None):
    """ Do a YouTube search. """

    youtube = build('youtube',
                    'v3',
                    developerKey=YOUTUBE_API_KEY,
                    cache_discovery=False)

    search_response = youtube.search().list(
        q=query,
        type="video",
        pageToken=token,
        order=order,
        part="id,snippet",
        maxResults=limit,
        location=location,
        locationRadius=location_radius).execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result)
    try:
        nexttok = search_response["nextPageToken"]
        return nexttok, videos
    except HttpError:
        nexttok = "last_page"
        return nexttok, videos
    except KeyError:
        nexttok = "KeyError, try again."
        return nexttok, videos


add_help_item(
    ".yt",
    "Misc",
    "Search YouTube and return the results.",
    """
    `.yt [options] (query)`
    
    Options:
    `limit`: Limit the results.
    `order`: Order the search results. Must be one of date, rating, relevance, title, videoCount, viewCount.
    """
)
