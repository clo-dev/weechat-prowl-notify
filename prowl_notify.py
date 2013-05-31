# Author: kidchunks <me@kidchunks.com>
# Homepage: http://github.com/kidchunks/weechat-prowl-notify
# Version: 2.0
#
# prowl_notify requires Prowl on your iPod Touch, iPhone or iPad.
# See more at http://www.prowlapp.com
#
# Requires Weechat 0.3.7 or Greater
# Released under the GNU GPL v3
#
# Prowl Limitations
# IP addresses are limited to 1000 API calls per hour which begins from the start of the first call. Create a new api key just for this script.
# See more at http://www.prowlapp.com/api.php
#
# prowl_away_notify is derived from notifo http://www.weechat.org/files/scripts/notifo.py
# Original Author: ochameau <poirot.alex AT gmail DOT com>


## settings
API_KEY = '' # API key from Prowl
FORCE_ENABLED = 'off' # enables notifications even when not away "on//off"
FLOOD_INTERVAL = '30' # time in seconds between notifications, set to 0 to disable flood control

## libraries
import weechat, time

## variables
old_time = time.time() - FLOOD_INTERVAL

## registration
weechat.register("prowl_notify", "kidchunks", "2.0", "GPL3", "Push notifications to iPod Touch, iPhone or iPad with Prowl", "", "")

## functions
def flood_check():
    current_time = time.time()
    elapsed_time = current_time - old_time
    if FLOOD_INTERVAL >= elapsed_time:
        return False
    else:
        global old_time
        old_time = current_time
        return True

def post_prowl(label, title, message):
    if API_KEY != "":
        opt_dict = "apikey=" + API_KEY + "&application=" + label + "&event=" + title + "&description=" + message
        weechat.hook_process_hashtable("url:https://api.prowlapp.com/publicapi/add?",
            { "postfields": opt_dict },
            30 * 1000, "", "")
    else:
        weechat.prnt("", "API Key is missing!")
        return weechat.WEECHAT_RC_OK

def hook_callback(data, bufferp, uber_empty, tagsn, isdisplayed,
        ishighlight, prefix, message):
    if (bufferp == weechat.current_buffer()):
        pass

    ## highlight
    if ishighlight == "1" and (weechat.buffer_get_string(bufferp, 'localvar_away') or FORCE_ENABLED == 'on'):
        if flood_check():
            buffer = (weechat.buffer_get_string(bufferp, "short_name") or weechat.buffer_get_string(bufferp, "name"))
            if prefix == buffer: # treat as pm if user mentions your nick in a pm
                post_prowl("WeeChat", "Private Message from " + prefix, message)
                weechat.command(bufferp, "/me has been notified, thanks " + prefix + ".")
            elif prefix != buffer: # otherwise, treat as highlight
                post_prowl("WeeChat", prefix + " mentioned you on " + buffer,  message)
                weechat.command(bufferp, "/me has been notified, thanks " + prefix + ".")

    ## privmsg
    elif weechat.buffer_get_string(bufferp, "localvar_type") == "private" and (weechat.buffer_get_string(bufferp, 'localvar_away') or FORCE_ENABLED == 'on'):
        if flood_check():
            post_prowl("WeeChat", "Private Message from " + prefix, message)
            weechat.command(bufferp, "/me has been notified, thanks " + prefix + ".")

    return weechat.WEECHAT_RC_OK

weechat.hook_print("", "notify_message", "", 1, "hook_callback", "")
weechat.hook_print("", "notify_private", "", 1, "hook_callback", "")