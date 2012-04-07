#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    fb.py - Some tests on the Facebook social network
#    Copyright (C) 2011 0vercl0k
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import urllib2
import cookielib
import re
import json
import traceback
from os import mkdir
from urllib import urlencode

class Friend:
	def __init__(self, name, id):
		self.name = name
		self.id = id
	
	def get_complete_name(self):
		return self.name
	
	def get_id(self):
		return self.id

	def __str__(self):
		return '%s - id=%s' % (self.name, self.id)
		
class Facebook:
	"""
		A basic facebook interface
	"""
	
	def __init__(self, username, password):
	
		# create the cookie jar
		self.cookie_jar = cookielib.CookieJar()
		
		# plug the cookie jar on our url_opener
		self.url_opener = urllib2.build_opener(
			urllib2.HTTPCookieProcessor(self.cookie_jar)
		)
		
		# authentification on your facebook acount
		self.authentification(username, password)
		
		# test if the authentification succeed or not
		if self.is_authenticated() == False:
			raise Exception('You are not authenticated, check your password/email')
		
		# get our access token
		self.access_token = self.get_access_token()
		
		# get the list of your friends
		self.my_friends = self.get_my_friends()
		if len(self.my_friends) == 0:
			raise Exception('You actually have not any friend')
	
	def query_graph_api(self, who, what):
		# query information to the graph facebook api
		return self.url_opener.open('https://graph.facebook.com/%s/%s?access_token=%s&limit=1000' % (who, what, self.access_token)).read()
	
	def get_my_friends(self):
		# get a list of your friend
		my_friends = {}
		
		# Example of an entry:
		# {"name": "Name Firstname","id": "012345678.."}
		for friend_id, friend_name in re.findall('"name":"([^"]+)",\s*"id":"(\d+)"', self.query_graph_api('me', 'friends')):
			my_friends[friend_id] = Friend(friend_id, friend_name)
		
		self.my_friends = my_friends
		return my_friends
		
	def get_access_token(self):
		# get our access token, useful to use the graph api
		regxp = 'Friends: <a href="https://graph.facebook.com/me/friends\?access_token=(.+)">'
		access_token = re.findall(regxp, self.url_opener.open('http://developers.facebook.com/docs/api').read())
		if len(access_token) != 1:
			raise Exception("Can't retrieve your access token :(")
		
		return access_token[0]
	
	def is_authenticated(self):
		# Test if we are currently authenticated
		return not 'Vous devez vous connecter pour voir cette page.' in self.url_opener.open('https://developers.facebook.com/docs/api').read()

	def authentification(self, username, password):
		# Authentification on the social network
		params = urlencode(
			{'email' : username,
			'pass' : password}
		)
		
		self.url_opener.open('https://login.facebook.com/login.php', params) 
		self.url_opener.open('https://login.facebook.com/login.php', params) 
	
	def list_albums_friend(self, friend):
		# list the different albums of a specific friend
		if self.my_friend.has_key(friend.get_id()) == True:
			return self.list_albums_id(friend.get_id())
		else:
			return None
		
	def list_albums_id(self, id_friend):
		# list the different albums of a specific friend thanks to its id
		albums = json.loads(self.query_graph_api(id_friend, 'albums'))
		albums_info = {}
		
		# Entry example:
		# {
		#	"id": "1253739440",
		#	"from": {
		#		"name": "Foo",
		#		"id": "134884"
		#	},
		#	"name": "photo album",
		#	"link": "https://www.facebook.com/album.php?fbid=blabla&id=foo&aid=bar",
		#	"cover_photo": "139488483",
		#	"count": 16,
		#	"type": "normal",
		#	"created_time": "2011-06-29T20:38:54+0000",
		#	"updated_time": "2011-07-10T20:38:38+0000"
		
		for album in albums['data']:
			albums_info[album['id']] = album
			
		return albums_info
	
	def username_to_id(self, username):
		# retrieve the id for a specific username
		info = json.loads(self.query_graph_api(username, ''))
		return info['id']
	
	def albumid_to_name(self, id):
		# retrieve the name of an album identified by its id
		return self.id_to_username(id)
		
	def id_to_username(self, id):
		# retrieve the username for a specific id
		info = json.loads(self.query_graph_api(id, ''))
		if info.has_key('username'):
			return info['username']
		else:
			return info['name']

	def list_albums(self, arg):
		# list photo albums of a friend (id or Friend instance)
		if type(arg) == Friend:
			return self.list_albums_friend(arg)
		else:
			return self.list_albums_id(arg)
	
	def download_all_albums(self, friend_id, mode = 'dir'):
		# mirror all the photo albums in the current directory
		albums = self.list_albums(friend_id)
		
		# create a special directory to store the differents albums
		root = './%s' % self.id_to_username(friend_id)
		mkdir(root)
		
		nb_total = 0
		pics_name = 1
		
		for id, album in albums.iteritems():
			print '\t* %s - id=%s..\n\t[' % (album['name'], id),
			
			# creation of the output directory if the user wants
			if mode != 'dir':
				path = '%s/%s' % (root, id)
				mkdir(path)
				pics_name = 1
			else:
				path = root

			nb_per_album = 1

			photos = json.loads(self.query_graph_api(id, 'photos'))

			# downloading each photo of the current album
			for photo in photos['data']:
				sys.stdout.write('.')
				sys.stdout.flush()
				
				if 'source' in photo:
					file = open('%s/%d.jpg' % (path, pics_name), 'wb')
					file.write(self.url_opener.open(photo['source']).read())
					file.close()
					nb_per_album += 1
					pics_name += 1
				
			nb_total += (nb_per_album - 1)
			print '] - %d pictures\n' % (nb_per_album - 1)
		
		print 'A total of %d pictures downloaded.' % nb_total
	
def main(argc, argv):
	try:
		fb = Facebook('login', 'pwd')
		print 'You are authenticated on facebook.com'
		
		#print 'Retrieving the list of your friends..'
		#f = fb.get_my_friends()
		#print '%d friends retrieved.' % len(f)
		
		#print 'Enumerating photo albums..'
		#for id, album in fb.list_albums('x.y').iteritems():
		#	try:
		#		print '\t* %s (id=%s, count=%d)' % (album['name'], id, album['count'])
		#	except:
		#		print 'hmm an error occured'
		#		continue
		
		print 'Downloading the albums..'
		fb.download_all_albums('id_person')
		
	except:
		print 'ERROR:'
		print traceback.print_exc()
		return 0
	return 1
	
if __name__ == '__main__':
	sys.exit(main(len(sys.argv), sys.argv))
	

