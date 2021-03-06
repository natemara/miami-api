#!/usr/bin/env python3
import tornado.autoreload
import tornado.ioloop
import tornado.web
import json
import subprocess
import os

import miami_api
import html_functions


class OpenLocationHandler(tornado.web.RequestHandler):
	def get(self):
		response = miami_api.get_open()
		json_response = json.dumps(response, indent=4 * ' ')
		self.set_header('Content-Type', 'application/json')
		self.write(json_response)


class StatusHandler(tornado.web.RequestHandler):
	def get(self, location):
		response = miami_api.get_status(location)
		json_response = json.dumps(response, indent=4 * ' ')
		self.set_header('Content-Type', 'application/json')
		self.write(json_response)


class PersonInfoHandler(tornado.web.RequestHandler):
	def get(self, name):
		response = miami_api.get_person_info(name)
		json_response = json.dumps(response, indent=4 * ' ')
		self.set_header('Content-Type', 'application/json')
		self.write(json_response)


class TodayStatusHandler(tornado.web.RequestHandler):
	def get(self):
		response = miami_api.get_today_hours()
		json_response = json.dumps(response, indent=4 * ' ')
		self.set_header('Content-Type', 'application/json')
		self.write(json_response)


class GithubHookHandler(tornado.web.RequestHandler):
	def post(self):
		subprocess.call(['git', 'pull', 'origin', 'master'])
		self.write('Update completed sucessfully')

	def get(self):
		self.write('update?')


class MainHandler(tornado.web.RequestHandler):
	def get(self, filename='index.html'):
		if filename is '' or filename == 'index.html':
			open_list = html_functions.get_open_for_html()
			self.render('index.html', open_list=open_list)
			return
		if filename == 'api' or filename == 'api/' or filename == 'api.html':
			open_list = miami_api.get_open()
			url = self.request.uri
			self.render('api.html', open_list = open_list, url = url)
			return
		self.render(filename)

handlers = [
	(r'/api/open', OpenLocationHandler),
	(r'/api/status/([a-zA-Z_]+)', StatusHandler),
	(r'/api/today', TodayStatusHandler),
	(r'/api/update', GithubHookHandler),
	(r'/api/person/([a-zA-Z_+]+)', PersonInfoHandler),
	(r'/(.*)', MainHandler),
	(r'/', MainHandler)
]

settings = {
	'debug': False,
	'static_path': os.path.join('static'),
	'template_path': os.path.join('templates')
	}

application = tornado.web.Application(handlers, **settings)

if __name__ == '__main__':
	application.listen(5000)
	tornado.autoreload.watch('miami_server.py')

	ioloop = tornado.ioloop.IOLoop.instance()
	tornado.autoreload.start(ioloop)
	ioloop.start()
