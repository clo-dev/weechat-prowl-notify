# Author: kidchunks <me@kidchunks.com>
# Homepage: http://github.com/kidchunks/weechat-prowl-notify
# Version: 1.0
#
# prowl_notify requires Prowl on your iPod Touch, iPhone or iPad.
# See more at http://www.prowlapp.com
#
# Requires Weechat 0.3.0 or Greater
# Released under the GNU GPL v3
#
# Prowl Limitations
# IP addresses are limited to 1000 API calls per hour which begins from the start of the first call. Create a new api key just for this script.
# See more at http://www.prowlapp.com/api.php
#
# prowl_away_notify is derived from notifo http://www.weechat.org/files/scripts/notifo.py
# Original Author: ochameau <poirot.alex AT gmail DOT com>


## settings
api_key = '' # API key from Prowl
force_enabled = 'off' # enables notifications even when not away "on//off"
flood_protection =  'on' # helps prevent flooding "on//off"
flood_interval = '30' # time in seconds until reseting.

## libraries
import weechat, urllib, urllib2

## registration
weechat.register("prowl_notify", "kidchunks", "1.0", "GPL3", "prowl_notify: Push notifications to iPod Touch, iPhone or iPad with Prowl", "", "")

## variables
isReset = 1

## functions
def reset_timer(data, remaining_calls):
    global isReset
    if isReset == 0:
        isReset = 1

    return weechat.WEECHAT_RC_OK

def flood_check():
    global isReset
    if flood_protection == 'on':
        isReset = 0

def postProwl(label, title, message):
    PROWL_API = api_key
    if PROWL_API != "":
        url = "https://api.prowlapp.com/publicapi/add"
        opt_dict = {
        "apikey": PROWL_API,
        "application": label,
        "event": title,
        "description": message
            }
        req = urllib2.Request(url, urllib.urlencode(opt_dict))
        res = urllib2.urlopen(req)
        return weechat.WEECHAT_RC_OK

def hook_callback(data, bufferp, uber_empty, tagsn, isdisplayed,
        ishilight, prefix, message):
    if (bufferp == weechat.current_buffer()):
        pass

    # highlight
    elif ishilight == "1" and (weechat.buffer_get_string(bufferp, 'localvar_away') or force_enabled == 'on'):
        if isReset == 1:
            buffer = (weechat.buffer_get_string(bufferp, "short_name") or weechat.buffer_get_string(bufferp, "name"))
            if prefix == buffer: # treat as pm if user mentions your nick in a pm
                postProwl("WeeChat", "Private Message from " + prefix, message)
            elif prefix != buffer: # otherwise, treat as highlight
                postProwl("WeeChat", prefix + " mentioned you on " + buffer,  message)
            
            flood_check()

    # privmsg
    elif weechat.buffer_get_string(bufferp, "localvar_type") == "private" and (weechat.buffer_get_string(bufferp, 'localvar_away') or force_enabled == 'on'):
        if isReset == 1:
            postProwl("WeeChat", "Private Message from " + prefix, message)
            flood_check()

    return weechat.WEECHAT_RC_OK

if flood_protection == "on":
    weechat.hook_timer(int(flood_interval) * 1000, 0, 0, "reset_timer", "")

weechat.hook_print("", "irc_privmsg", "", 1, "hook_callback", "")