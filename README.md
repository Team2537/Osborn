# Osborn
A spreadsheet server python script to synchronize data between thebluealliance.com, and a google spreadsheet.

In order to run this, type 
spreadsheet_server.py URL

With a url point to a google spreadsheet. The program goes to the spreadsheet (if it's email address explicitly added to the 
sheet beforehand) and reads the first sheet for activation codes.

All codes start with !Osborn and are then followed by a word.

!Osborn event {KEY} Specifiy the event for the system to use.
!Osborn stats        Get the opr, dpr, and ccwm for the event.
