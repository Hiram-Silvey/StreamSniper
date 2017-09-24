import requests
import time
import calendar
import json
import clip_cfg as cfg

r = requests.get('https://api.twitch.tv/kraken/clips/top?limit={}&channel={}'.format(cfg.LIMIT, cfg.CHANNEL), headers={'Client-ID': cfg.CLIENT_ID, 'Accept': 'application/vnd.twitchtv.v5+json'})

clips = r.json()['clips']
for i, clip in enumerate(clips):
    date_time = clip['created_at']
    pattern = '%Y-%m-%dT%H:%M:%SZ'
    duration = clip['duration']
    epoch = int(calendar.timegm(time.strptime(date_time, pattern))) - int(duration)
    video_id = clip['vod']['id']
    chat = requests.get('https://rechat.twitch.tv/rechat-messages?start={}&video_id=v{}'.format(epoch, video_id))
    if not chat.ok:
        continue
    end_timestamp = (epoch*1000) + int(duration*1000)
    data = []
    for message in chat.json()['data']:
        if message['attributes']['timestamp'] > end_timestamp:
            break
        data.append(message)
    with open('{}.json'.format(i), 'w') as f:
        json.dump(data, f)
