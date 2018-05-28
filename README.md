# SHIFTY	
For those who have a job with changing shifts, who wants to keep track of their working hours via telegram

Just send the date, begin and end time of your work and it will be saved : 

    you : +20/01 11h00 14h00 16h30 22h00
    bot : 8.5 hours

Don't remeber ? 

    you : ?20/01
    bot : Saturday 20/1 : 
	      11:0-14:0
	      16:30-22:0
	      8.5 hour

Made an error  ? erase the day with 

    you : -20/01
    bot : 2001 removed

How Many hours did i Worked last week ?
    
    you : week 19
    bot : week 19
	  Monday 7/5 : 
		  11:0-14:30
		  17:0-22:30
		  9.0 hours
	  Tuesday 8/5 : 
		  14:30-21:0
		  6.5 hours
 	  Wednesday 9/5 : 
		  7:30-14:30
		  7.0 hours
 	  Friday 11/5 : 
		  14:30-0:30
		  10.0 hours
 	  Saturday 12/5 : 
		  15:30-20:30
		  5.0 hours

	  37:30 hours


## Requirements 

* Python 3+
* [Telepot](https://github.com/nickoala/telepot)
* sqlite3
* datetime
* time
* Bot key & `tokens.py`
    * Hide all the keys and admin variables in `tokens.py`. Use it only for sensitive variables. Avoid creating functions not to clutter the namespaces through the import.
    * Get a key from the [Bot Father](https://telegram.me/BotFather)
    * Clone that repo
    * In the folder with the cloned repo create a file `tokens.py`
       * It's added to the `.gitignore` so you don't commit your own (and I don't commit mine:)
    * In that file put a string variable `telegrambot` which equals your key
       * For example: `telegrambot = "000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"`
   
## Setting your userid

You have to set a variable `adminchatid` in `tokens.py` to be equal your chat_id or multiple chat_id (if more people will use your bot).
For example:
* `adminchatid = [443355]`

## Running the bot

`python3 __init__.py`




## TODO
I want it to be able to give the total of working hours ~~per week~~, and per month. 
maybe some type of graphical calendar of working days to be send via photo  ?


