 # PoroBot
***
 ## Files

 * `cogs`:
-`base.py` basic commands for the bot, such as `ping`.
-`loldata.py` defines Discord commands which call methods in `requests.py` to 
 
 * `utils`:
 -`config.py` module with dictionaries of static data, such as API keys.
 -`requests.py` contains the functions to fetch data from the Riot API.

 * `app.py` instantiates bot and loads cogs.

### `app.py`
Imports dependent packages, instantiates bot with the Discord bot key, loads cogs.

**Methods**
`on_ready()` is an event listener for when the bot is instantiated and ready for use. A message is printed in console to show that the bot is ready.

`reload_cog(ctx, incog)` is a function triggered by command `-reloadcog`*`cog`* where the parameter is the cog to be reloaded. The function unloads and loads the cog. Changes made to cogs can be made even during bot runtime so long as that cog is reloaded.

### **`COG`**`base.py`
Basic commands for Porobot.

**Methods**
`on_message(self, message)` is an event listener. If `-ping` is read then a latency measurement is taken which involves the bot sending `Ping!` in the same channel which is edited to `Pong!`*`x ms`* where `x` is the time taken in miliseconds after sending the message to edit it.

`display_help(self, ctx)` can be invoked with command `-help`. An embed is sent in the channel in which the command was sent with the user-accessible methods.

### **`COG`**`loldata.py`
Uses a `Riotwrapper` object from the `requests` module to fetch data on the Riot API and output to the respective channel in embed form.

**Methods**
`display_status(self, ctx)` is invoked with `-getstatus`. The current version only supports the EUW1 region. `Riotwrapper` method `get_status()` returns the status for the Store, Game, Website and Client in a dictionary object. The statuses are then sent in an `embed` to the respective channel. `status_light(component_status)` returns `:large_blue_circle:` if the status is `online`. 