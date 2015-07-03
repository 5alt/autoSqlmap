# -*- coding: utf-8 -*-
import requests
import json
import os

import config

class SqlmapAPIWrapper():
	def __init__(self, filename='salt'):
		self.url = config.sqlmap_host
		self.taskid = None
		self.filepath = config.save_path + '/' + filename
		self.options = {'requestFile': self.filepath}
		self.options.update(config.sqlmap_options)
		self.headers = {'Content-Type': 'application/json'}

	def settaskid(self, taskid):
		self.taskid = taskid

	def new(self):
		path = '/task/new'
		r = requests.get(self.url + path, headers=self.headers).json()
		if r['success']:
			self.taskid = r['taskid']
		return r['success']

	def delete(self):
		path = '/task/%s/delete' % self.taskid
		r = requests.get(self.url + path, headers=self.headers).json()
		self.taskid = None
		return r['success']

	def scan_start(self):
		self.new()
		path = '/scan/%s/start' % self.taskid
		r = requests.post(self.url + path, data=json.dumps(self.options), headers=self.headers).json()
		return r['success']

	def scan_stop(self):
		path = '/scan/%s/stop' % self.taskid
		r = requests.get(self.url + path, headers=self.headers).json()
		return r['success']

	def scan_kill(self):
		path = '/scan/%s/kill' % self.taskid
		r = requests.get(self.url + path, headers=self.headers).json()
		return r['success']

	def scan_status(self):
		path = '/scan/%s/status' % self.taskid
		r = requests.get(self.url + path, headers=self.headers).json()
		if r['success']:
			return r['status']
		else:
			return None

	def scan_data(self):
		path = '/scan/%s/data' % self.taskid
		r = requests.get(self.url + path, headers=self.headers).json()
		if r['success']:
			return r['data']
		else:
			return None

	def terminal(self):
		return self.scan_status() == 'terminated'

	def vulnerable(self):
		return len(self.scan_data()) > 0

	def delete_file(self):
		os.remove(self.filepath)

	def clear(self):
		self.scan_stop()
		self.delete_file()

