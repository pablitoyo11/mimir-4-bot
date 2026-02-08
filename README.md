# mimir-4-bot
NOTE: NOT UPDATING ANYMORE, SOME FILES ARE USELESS CAUSE I HAD MANY FILES FOR TESTING FEATURES, SOME MAPS STOPPED WORKING BECAUSE THEY UPDATED SOME MAPS TRAVEL UI, WICH MAKES THE BOT "RETURN TO MAP" FUNCTION TO FAIL, IF YOU ARE IN THE NEW MAPS (EX: MIRAGE SHIP NOW HAS 2 "LAYERS" WICH WEREN'T THERE BEFORE, SO THE BOT DOESN'T KNOW WHERE TO CLICK AT THIS POINT AND MESSES UP)

(not optimized for everybody to use, you should update files and add map name manually if you want to change the route bot will take)
(you need to open file and hard code /manually write the name of the window you want the bot to work on, example Mir4G[0] or Mir4G[1] etc)
(Game should be on chinesse, this simplifies many texts "overflowing" screen when playing in other languages, wich causes some bugs when text appears in "transparent" background and is hard to check for the bot)
File to edit things and start the bot working, "arjancodesStateClassnew - congoogle.py"
File to create sequences of return to map, or working maps, use "CreateMapGGleUnit - definitivo comas.py"
to create a "return to map" file, use the UI click poin or click area options.
to create a "gathering map", use the map option and add map name and map action, wrong map actin will make the bot not know what to do, you should program a file map action if you create new ones wich aren't included, you should use OpenChest, if you don't know what to add, bot will automatically wait until finish even if colleting other things.


Bot works in a class state way.
Constantly taking screenshots of the game and analyzing to change bot state according to situation
there are few constant checkers that checks: current map / danger situation or death / gathering or collecting things status / moving status / 
some states currently programed are: opening chest / gathering / moving / danger / returning to work map /
I think there is a few more wich I stopped using long ago

video showing
map creation tool and activating bot to start one preselected trayectory searching chests / orbs in mirage ship, couldn't find much orbs to collect during video, server is full of automated bots already 

<video src="https://github.com/user-attachments/assets/71160541-0f5d-480b-8e13-3625c4167158" controls="controls" style="max-width: 100%;">
</video>
https://github.com/user-attachments/assets/71160541-0f5d-480b-8e13-3625c4167158

