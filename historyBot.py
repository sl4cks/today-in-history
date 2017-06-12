#!/usr/bin/python3.5

#imports for such and such
import tweepy, time
from bs4 import BeautifulSoup as bsoup #need bs for that sweet, sweet web scraping
from urllib.request import urlopen #need to get url
from datetime import date #need to pull the current date
import calendar #calendar can find the name of the month
import markovify
import random
#bot stuff from
#https://dototot.com/how-to-write-a-twitter-bot-with-python-and-tweepy/

#Twitter auth stuff ripped from the article

#to actually implement, put keys here
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#real bot shit

#find today's date and fetch the wiki page
def get_wiki():
		today = date.today()
		#could also possibly add http://www.onthisday.com/today/events.php for stuff
		url = "https://en.wikipedia.org/wiki/"+calendar.month_name[today.month]+"_"+str(today.day)
		print("Now running for ", url) #just checking

		#open the page and turn it into soup
		content = urlopen(url).read()
		soup = bsoup(content, "html.parser")

		#gets the unordered list for events that day
		#events = soup.find_all("ul")[1] #this is a prior version for reference
		return soup.find_all("ul")[1].find_all("li")

#generate a tweet based on the passed resultSet (list subclass, not a tag class)
#note that resultset has the find* methods defined
def make_tweet(events_list):
		#lists for the event dates and the events themselves
		dates = [] #the isolated dates
		events = [] #events

		for event in events_list:
				#split them to get date and body description
				temp = event.get_text().split("–")
				#add the date
				dates.append(temp[0])
				#take a slice of the rest and join it to take care of other - chars
				events.append("".join(temp[1::]))
		#time to get into real markov stuff
		text_model = markovify.Text("".join(events))
		#pick a random date from the list on the page
		event_date = random.choice(dates).strip() + ": "
		return event_date + text_model.make_short_sentence(140-len(event_date))

#tweet the passed string
def tweet(message):
		api.update_status(message)
		#time.sleep(14400)
		#time.sleep(30)

if __name__ == "__main__":
		events = get_wiki()
		message = make_tweet(events)
		tweet(message)
