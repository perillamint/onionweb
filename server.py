#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: KBuild, Maneulyori, sookcha
# email: qwer7995@gmail.com(KBuild), maneulyori@gmail.com(Maneulyori), lsookcha@me.com(sookcha)

import string,cgi,time, os, sys, urllib2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from pprint import pprint

class Server(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			patharray = self.path.split('/')

			sc = ServerConfig()
			cdir = sc.getDir(patharray[1])

			if cdir is not False:
				fullpath = cdir
			else:
				self.send_error(404, 'Not found')
				return

			#initialize & title, route, realpath bind
			title, route, realpath = "", "", ""

			if patharray[1] == "":
				title = 'ROOT PATH'
				route = '/'
			else:
				for i in range(len(sc.names)):
					if patharray[1].find(sc.names[i]) != -1:
						title = sc.names[i]
						route = self.path

			# patharray second element to end of array + filename => realpath
			if len(patharray) < 3:
				realpath = fullpath
			else:
				realpath = fullpath
				for i in range(len(patharray) - 2):
					realpath += "/" + patharray[i+2]

			print "URL PATH : " + self.path
			print "PATH : " + fullpath
			print "realpath : " + realpath

			#Directory listing
			if os.path.isdir(realpath):
				print "read template"
				f = open('template', 'r')
				readed = f.read()
				f.close()

				# folder reading
				filelist = ""
				if patharray[1] == "":#if Directory Root
					target = sc.names
				else:
					target = os.listdir(realpath)

				for l in target:
					prevpath = route
					if prevpath.endswith("/") is False:
						prevpath = prevpath + "/"
					if prevpath.startswith(".") is False:
						prevpath = "" + prevpath
					filelist += "\t\t<tr>\n\t\t\t<td><a href=\"" + prevpath + l +"\">" + l + "</a></td>\n\t\t</tr>\n"

				# string replace
				readed = readed.replace("__TITLE__",title)
				readed = readed.replace("__ROUTE__",route)
				readed = readed.replace("__LIST__",filelist)

				self.send_response(200)
				self.send_header('Content-Type', 'text/html')
				self.end_headers()
				self.wfile.write(readed)
				return

			forbidlist = ['server.py', 'main.py', 'template', 'list.conf']

			for forbid in forbidlist:
				if fullpath == os.getcwd() + '/' + forbid:
					self.send_error(403, 'Forbidden')
					return

			#Unescape realpath
			realpath = urllib2.unquote(realpath)
			f = open(realpath)

			self.send_response(200)
			#setting header
			picmimelist = ['jpg', 'jpeg', 'png', 'gif'] # picture
			for mime in picmimelist:
				if( self.path.endswith('.' + mime) ):
					self.send_header('Content-Type', 'image/' + mime)
					break

			musmimelist = ['mp3', 'flac', 'wav']
			for mime in musmimelist:
				if( self.path.endswith('.' + mime) ):
					self.send_header('Content-Type', 'audio/' + mime)
					break

			self.end_headers()

			self.wfile.write(f.read())
			f.close()
			return

		except IOError as e:
			if e.errno is 2:
				self.send_error(404,'Not found');
			elif e.errno is 13:
				self.send_error(403,'Fobidden');

class ServerConfig():
	def getDir(self, virtual_dir):
		count = 0
		for name in self.names:
			if name.find(virtual_dir) is not -1:
				return self.routes[count]
			count += 1
		return False

	def configListing(self):
		f = open('list.conf', 'r')
		datas = f.readlines()
		self.names = []
		self.routes = []
		for data in datas:
			dataarray = data.split(',')
			self.names.append(dataarray[0].strip())
			self.routes.append(dataarray[1].strip())

	def __init__(self):
		self.configListing()

def main():
	try:
		server = HTTPServer(('localhost', int(sys.argv[1])), Server)
		print 'server start...'
		server.serve_forever()
	except KeyboardInterrupt:
		server.socket.close()
		print 'server stop...'

if __name__ == '__main__':
	main()
