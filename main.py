import pdb
import requests
import base64
import time
import sys
import threading
import io
import PIL.Image
import random
import string
import collections
import os
import socket
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

TIMEOUT = 5

class CaptchaSolver:
	def __init__(self, key):
		self.api = "https://api.anti-captcha.com/"
		self.key = key
		print("Solver initialized with key: " + self.key)

	def solve(self, image):
		task = {}
		task["type"] = "ImageToTextTask"
		task["body"] = base64.b64encode(image).decode("utf-8")
		task["phrase"] = False
		task["case"] = False
		task["numeric"] = 1
		task["math"] = False
		task["minLength"] = 6
		task["maxLength"] = 6
		data = requests.post(self.api + "createTask", json={"clientKey" : self.key, "task" : task}, verify=False).json()
		if (data["errorId"] == 0):
			while True:
				response = requests.post(self.api + "getTaskResult", json={"clientKey" : self.key, "taskId" : str(data["taskId"])}, verify=False).json()
				if (response["status"] == "ready"):
					return response["solution"]["text"]
				time.sleep(3)

class Captcha:
	def __init__(self, proxy, agent, board, thread, solver):
		self.api = "https://2ch.hk/api/captcha/2chaptcha/"
		self.proxy = proxy
		self.agent = agent
		self.board = board
		self.thread = thread
		self.solver = solver
		captcha = requests.get(self.api + "id?board=" + self.board + "&thread=" + self.thread, proxies=self.proxy, headers=self.agent, timeout=TIMEOUT, verify=False).json()
		self.id = captcha["id"]
		self.image = requests.get(self.api + "image/" + self.id, proxies=self.proxy, headers=self.agent, timeout=TIMEOUT, verify=False).content

	def solve(self):
		print(self.proxy["http"], "solving captcha")
		self.value = self.solver.solve(self.image)
		return (None, self.id), (None, self.value)

	def verify(self):
		return requests.get(self.api + "check/" + self.id + '?value=' + self.value, proxies=self.proxy, headers=self.agent, verify=False).json()["result"] == 1

class Post:
	def __init__(self, proxy, agent, board, thread, solver):
		self.proxy = {"http": proxy, "https": proxy}
		self.agent = {"User-Agent": agent}
		self.board = board
		self.thread = thread
		self.solver = solver
		self.params = {}
		self.params["task"] = (None, "post")
		self.params["board"] = (None, self.board)
		self.params["thread"] = (None, self.thread)
		self.params["captcha_type"] = (None, "2chaptcha")

	def prepare(self):
		try:
			self.params["2chaptcha_id"], self.params["2chaptcha_value"] = Captcha(self.proxy, self.agent, self.board, self.thread, self.solver).solve()
			print(self.proxy["http"], "solved")
			return True
		except Exception as e:
#			print(e)
			return False

	def set_subject(self, text):
		self.params["subject"] = (None, text)

	def set_text(self, text):
		self.params["comment"] = (None, text)

	def set_image(self, file_name, file_name_displayed):
		image = PIL.Image.open(file_name).convert("RGB")
		width, height = image.size
		for x in range(random.randint(1, 10)): image.putpixel((random.randint(0, width-1), random.randint(0, height-1)), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
		image = image.crop((0 + random.randint(0, 10), 0 + random.randint(0, 10), width-1 - random.randint(0, 10), height-1 - random.randint(0, 10)))
		image_bytes = io.BytesIO()
		image.save(image_bytes, "JPEG", quality=60 + random.randint(10, 30), optimize=bool(random.getrandbits(1)), progressive=bool(random.getrandbits(1)))
		image.close()

		self.params["formimages"] = (file_name_displayed, image_bytes.getvalue(), "image")

	def clear_image(self):
		self.params["formimages"] = ()

	def send(self):
		response = {}
		try:
			print(self.proxy["http"], "posting")
			response = requests.post("https://2ch.hk/makaba/posting.fcgi?json=1", files=self.params, proxies=self.proxy, headers=self.agent, timeout=TIMEOUT, verify=False).json()
			return response["Error"] == None, response
		except Exception as e:
#			print(e)
			return False, response

class Wiper:
	def __init__(self, board, thread):
		print("Wiper started")
		self.proxies = [proxy[:-1] for proxy in open("proxies").readlines()]
		random.shuffle(self.proxies);
		self.agents = [agent[:-1] for agent in open("useragents").readlines()]
		self.board = board
		self.thread = thread
		self.solver = CaptchaSolver("anti-captcha.com api key")

	def send_post(self):
		if (len(self.proxies) == 0): return False
		proxy = self.proxies.pop(0)
		agent = random.choice(self.agents)
		response = {"Error": "proxy"}
		try:
			post = Post(proxy, agent, self.board, self.thread, self.solver)
			while True:
				if (post.prepare()):
					post.set_text("**ALLO YOBA ETO TI**")
					post.set_image("./yoba.png", "blob")
					success, response = post.send()
					if (success):
						post_id = 0
						try:
							post_id = response["Target"]
						except:
							post_id = response["Num"]
						print(proxy + " - success. Post id: " + str(post_id))
						self.proxies.push(proxy)
						break
					else:
						print(proxy, "posting failed -", response)
						try:
							if ((response["Error"] != 6) and (response["Error"] != 4)): raise
						except:
							self.proxies.push(proxy)
				raise
		except Exception as e:
			pass
#			print(proxy, "-", response, e)

		return True

	def wipe(self, thread_count):
		class WiperThread(threading.Thread):
			def __init__(self, wiper):
				threading.Thread.__init__(self)
				self.wiper = wiper

			def run(self):
				while self.wiper.send_post(): pass

		threads = []
		for i in range(thread_count):
			threads.append(WiperThread(self))
			threads[-1].start()

		for thread in threads:
			thread.join()

Wiper(sys.argv[1], sys.argv[2]).wipe(int(sys.argv[3]))
