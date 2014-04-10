weechat-prowl-notify
====================

prowl_notify: Push notifications to iPod Touch, iPhone or iPad with [Prowl](http://prowlapp.com)

## Demo
Coming Soon!

## Installation and Usage
1. 'prowl_notify' requires Prowl installed on your iPod Touch, iPhone or iPad and along with an API key from Prowl.

2. Edit prowl_notify.py and add your api key to "API_KEY". This can be multiple API Keys (seperated by commas).
3. Place a copy of `prowl_notify.py` in `~/.weechat/python/autoload`.
4. Once inside weechat, run the command `/python load python/autoload/prowl_notify.py`.
5. Set yourself away!
5. Enjoy IRC highlights and private message notifications sent to your prowl enabled device!

## Configurable Options
Please view the 'settings' section of `prowl_notify.py` to see their description and how to configure them.

If you make changes to the 'prowl_notify.py', simply run these commands within weechat to reload the plugin.
1. /python unload prowl_notify
2. /python /python load python/autoload/prowl_notify.py

## Prowl Limitations
1. IP addresses are limited to 1000 API calls per hour which begins from the start of the first call. I recommend creating a new api key just for this plugin. See more at [http://www.prowlapp.com/api.php](http://www.prowlapp.com/api.php)
2. When using multiple API keys, you will only get a failure response if all API keys are not valid so make sure all the API keys are valid.
