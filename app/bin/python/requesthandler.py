#!/usr/bin/env python3

import urllib.request as ur
import urllib.parse as up
from lxml import html
import datetime
import requests
import json
import time
import sys
import os

class InstaBot:

	def __init__(self, path_to_config_file, channel, api_token):
		self.path_to_config_file = path_to_config_file
		self.channel = channel
		self.api_token = api_token

	def getUserName(self, user_id):
		time.sleep(5)
		url = url = "https://i.instagram.com/api/v1/users/"+str(user_id)+"/info/"
		user_info = ur.urlopen(url).read()
		user_name = json.loads(user_info)["user"]["username"]
		return str(user_name)

	def getMediaCount(self, user_id):
		time.sleep(5)
		url = "https://i.instagram.com/api/v1/users/"+str(user_id)+"/info/"
		user_info = ur.urlopen(url).read()
		media_count = json.loads(user_info)["user"]["media_count"]
		return int(media_count)

	def getProfilePic(self, user_id):
		time.sleep(5)
		url = "https://i.instagram.com/api/v1/users/"+str(user_id)+"/info/"
		user_info = ur.urlopen(url).read()
		profile_pic_url = json.loads(user_info)["user"]["hd_profile_pic_url_info"]["url"]
		return str(profile_pic_url)

	def sendMessage(self, text):
		r = ur.urlopen("https://api.telegram.org/bot"+self.api_token+"/sendMessage?", up.urlencode({"chat_id": self.channel, "text": text}).encode("utf-8")).read()
		print(r)
		return

	def getNewPost(self, user_id):
		user_name = self.getUserName(user_id)
		time.sleep(5)
		url = "https://instagram.com/"+str(user_name)+"/"
		user_profile = ur.urlopen(url).read()
		post_page = "https://instagram.com/p/"+str(str(user_profile).split("shortcode")[1].split("\"")[2])
		post_pic = str(str(user_profile).split("shortcode")[1].split("display_url")[1].split("\"")[2])
		return [post_page, post_pic]

	def getStories(self, user_ids):
		self.sendMessage("Today's Stories:")
		time.sleep(5)
		for user_id in user_ids:
			user_name = self.getUserName(user_id)
			u = ur.urlopen("https://storiesig.com/?username="+str(user_name))
			time.sleep(5)
			story_link = "https://storiesig.com/stories/"+str(user_name)
			self.sendMessage(story_link)
			time.sleep(5)

	def createConfig(self, user_ids):

		users_media_counts = []
		users_profile_pics = []

		for user_id in user_ids:
			users_media_counts.append(self.getMediaCount(user_id))
			users_profile_pics.append(self.getProfilePic(user_id))

		config_f = open(self.path_to_config_file, "w")
		string_to_write = ""
		for mc in users_media_counts:
			string_to_write = string_to_write + str(mc) + "\n"
		p = 0
		for pb in users_profile_pics:
			if p < len(users_profile_pics)-1:
				string_to_write = string_to_write + str(pb) + "\n"
			else:
				string_to_write = string_to_write + str(pb)
		config_f.write(string_to_write)
		config_f.close()

	def writeConfig(self, users_media_counts, users_profile_pics):

		config_f = open(self.path_to_config_file, "w")
		string_to_write = ""
		for mc in users_media_counts:
			string_to_write = string_to_write + str(mc) + "\n"
		p = 0
		for pb in users_profile_pics:
			if p < len(users_profile_pics)-1:
				string_to_write = string_to_write + str(pb) + "\n"
			else:
				string_to_write = string_to_write + str(pb)
		config_f.write(string_to_write)
		config_f.close()

	def instaBot(self, user_ids, rtime = 3480, stime = 21, debugging_mode = True):

		if debugging_mode:
			self.sendMessage("InstaPython process was launched!")

		user_names = []
		user_names_string = ""
		for user_id in user_ids:
			user_names.append(self.getUserName(user_id))
			user_names_string = user_names_string + self.getUserName(user_id) + "; "

		print("InstaBot initiated with usernames: ", user_names)
		if debugging_mode:
			init_message = "InstaBot initiated with usernames: " + user_names_string.rstrip("; ")
			self.sendMessage(init_message)

		if os.path.isfile(self.path_to_config_file):
			print("Found existing configuration file!")
			if debugging_mode:
				self.sendMessage("Found existing configuration file!")
		else:
			self.createConfig(user_ids)
			print("Created configuration file at: ", self.path_to_config_file)
			if debugging_mode:
				self.sendMessage("Created configuration file!")

		config_f = open(self.path_to_config_file, "r")
		config = config_f.read().splitlines()
		config_f.close()

		users_media_counts = config[:int(len(config)/2)]
		users_profile_pics = config[int(len(config)/2):]

		if rtime != 0:
			rep = 1
			while rep < rtime:
				rep = rep + 60
				time.sleep(60)
				for i in range(len(user_ids)):
					rep = rep + 5
					new_media_count = self.getMediaCount(user_ids[i])
					if new_media_count > int(users_media_counts[i]):
						users_media_counts[i] = new_media_count
						rep = rep + 5
						new_post = self.getNewPost(user_ids[i])
						text = "User "+str(self.getUserName(user_ids[i]))+" posted something new: "+new_post[0]+" ;"
						self.sendMessage(text)
						text = "Raw image can be found here: "+new_post[1]+" ;"
						self.sendMessage(text)
						text = "Link to profile: https://instagram.com/"+str(self.getUserName(user_ids[i]))
						self.sendMessage(text)
						self.writeConfig(users_media_counts, users_profile_pics)
					rep = rep + 5
					new_profile_pic_url = self.getProfilePic(user_ids[i])
					if new_profile_pic_url != users_profile_pics[i]:
						users_profile_pics[i] = new_profile_pic_url
						text = "User "+str(self.getUserName(user_ids[i]))+" has a new profile pic: "+str(new_profile_pic_url)+" ;"
						self.sendMessage(text)
						self.writeConfig(users_media_counts, users_profile_pics)

			self.getStories(user_ids)
			print("Done! Restart?")
		else:
			start_message = "InstaBot started with usernames: " + user_names_string.rstrip("; ")
			self.sendMessage(start_message)
			try:
				while True:
					time.sleep(60)
					for i in range(len(user_ids)):
						new_media_count = self.getMediaCount(user_ids[i])
						if new_media_count > int(users_media_counts[i]):
							users_media_counts[i] = new_media_count
							new_post = self.getNewPost(user_ids[i])
							text = "User "+str(self.getUserName(user_ids[i]))+" posted something new: "+new_post[0]+" ;"
							self.sendMessage(text)
							text = "Raw image can be found here: "+new_post[1]+" ;"
							self.sendMessage(text)
							text = "Link to profile: https://instagram.com/"+str(self.getUserName(user_ids[i]))
							self.sendMessage(text)
							self.writeConfig(users_media_counts, users_profile_pics)
						new_profile_pic_url = self.getProfilePic(user_ids[i])
						if new_profile_pic_url != users_profile_pics[i]:
							users_profile_pics[i] = new_profile_pic_url
							text = "User "+str(self.getUserName(user_ids[i]))+" has a new profile pic: "+str(new_profile_pic_url)+" ;"
							self.sendMessage(text)
							self.writeConfig(users_media_counts, users_profile_pics)
					if datetime.datetime.now().time().hour == stime and datetime.datetime.now().time().minute == 0:
						self.getStories(user_ids)
			except KeyboardInterrupt:
				try:
					self.writeConfig(users_media_counts, users_profile_pics)
				except:
					pass

				print("Exiting!")
		return

class Instagram:

	def __init__(self):
		pass

	def getUserID(self, user_name):
		url = "https://www.instagram.com/" + str(user_name)
		page = ur.urlopen(url).read().decode("utf-8")
		lines = page.splitlines()

		data = ""
		user_id = 0

		for line in lines:
			if "window._sharedData = " in line:
				data = line.replace("window._sharedData = ", "").replace("<script type=\"text/javascript\">", "").replace(";</script>", "").lstrip().rstrip()

		if data != "":
			jdata = json.loads(data)
			try:
				user_id = jdata["entry_data"]["ProfilePage"][0]["graphql"]["user"]["id"]
			except:
				pass

		if user_id != 0:
			return int(user_id)
		else:
			print("It seems retrieving the user ID was unsuccessful!")
			return 1

	def getUserName(self, user_id):
		url = "https://i.instagram.com/api/v1/users/"+str(user_id)+"/info/"
		user_info = ur.urlopen(url).read()
		user_name = json.loads(user_info)["user"]["username"]
		return str(user_name)

	def getMediaCount(self, user_id):
		url = "https://i.instagram.com/api/v1/users/"+str(user_id)+"/info/"
		user_info = ur.urlopen(url).read()
		media_count = json.loads(user_info)["user"]["media_count"]
		return int(media_count)

	def getProfilePic(self, user_id, download = False):
		url = "https://i.instagram.com/api/v1/users/"+str(user_id)+"/info/"
		user_info = ur.urlopen(url).read()
		profile_pic_url = json.loads(user_info)["user"]["hd_profile_pic_url_info"]["url"]
		if download:
			s_path = "downloads/" + str(profile_pic_url).split("/")[-1].split("?")[0]
			ur.urlretrieve(str(profile_pic_url), s_path)
		return str(profile_pic_url)

	def getNewPost(self, user_id, download = False):
		user_name = self.getUserName(user_id)
		url = "https://instagram.com/"+str(user_name)+"/"
		user_profile = ur.urlopen(url).read()
		post_page = "https://instagram.com/p/"+str(str(user_profile).split("shortcode")[1].split("\"")[2])
		if download:
			post_pics = self.getMedia(post_page, True)
		else:
			post_pics = self.getMedia(post_page)
		post_details = [post_page]+post_pics
		return post_details

	def isPrivate(self, instagram_post_url):
		url = str(link)
		shortcode = str(url.split("instagram.com/p/")[1]).split("/")[0]
		if len(shortcode) > 12:
			return True
		else:
			return False

	def isProfilePrivate(self, user_id):
		url = "https://i.instagram.com/api/v1/users/"+str(user_id)+"/info/"
		user_info = ur.urlopen(url).read()
		is_private = json.loads(user_info)["user"]["is_private"]
		return is_private


	def getMedia(self, instagram_post_url, download = False):

		page = requests.get(instagram_post_url)
		tree = html.fromstring(page.content)
		data = tree.xpath('//body/script[@type="text/javascript"]')

		json_unprocessed = data[0].text_content()
		json_processed = str(json_unprocessed).replace("window._sharedData = ", "").rstrip(";")
		json_data = json.loads(json_processed)

		media_links = []

		if str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]) == "GraphImage":
			image = tree.xpath('//meta[@property="og:image"]/@content')
			media_links.append(str(image[0]))
			if download:
				s_path = "downloads/" + str(image[0]).split("/")[-1].split("?")[0]
				ur.urlretrieve(str(image[0]), s_path)
		elif str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]) == "GraphVideo":
			video = tree.xpath('//meta[@property="og:video:secure_url"]/@content')
			media_links.append(str(video[0]))
			if download:
				s_path = "downloads/" + str(video[0]).split("/")[-1].split("?")[0]
				ur.urlretrieve(str(video[0]), s_path)
		elif str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]) == "GraphSidecar":
			prefix = str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["shortcode"])
			edges = json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]
			for edge in edges:
				if edge["node"]["is_video"]:
					url = str(edge["node"]["video_url"])
					media_links.append(url)
					if download:
						s_path = "downloads/" + prefix+"_"+(url.split("/")[-1].split("?")[0])
						ur.urlretrieve(url, s_path)
				else:
					url = str(edge["node"]["display_url"])
					media_links.append(url)
					if download:
						s_path = "downloads/" + prefix+"_"+(url.split("/")[-1].split("?")[0])
						ur.urlretrieve(url, s_path)
		else:
			#print("Unrecognized typename!")
			pass

		return media_links

		def getMediaSafe(self, instagram_post_url, download = False):
			if self.isPrivate(instagram_post_url):
				print("Post might be private!")
				try:
					media = self.getMedia(instagram_post_url, download)
					return media
				except:
					print("Oops! Seems like something went wrong! Try manual download!")
					return 1
			else:
				try:
					media = self.getMedia(instagram_post_url, download)
					return media
				except:
					print("Oops! Seems like something went wrong! Try manual download!")
					return 1

	def getStories(self, user_id, download = False):

		user_name = self.getUserName(user_id)

		url = "https://storiesig.com/stories/" + str(user_name)
		page = ur.urlopen(url).read().decode("utf-8")
		lines = page.splitlines()

		data = ""

		media_links = []

		for line in lines:
			if "__NEXT_DATA__" in line:
				data = line.replace("__NEXT_DATA__ = ", "").lstrip().rstrip()

		if data != "":
			jdata = json.loads(data)
			stories = jdata["props"]["pageProps"]["stories"]["items"]
			if len(stories) == 0:
				return media_links
			else:
				for story in stories:
					original_width = story["original_width"]
					original_height = story["original_height"]
					media_type = int(story["media_type"])
					for entry in story["image_versions2"]["candidates"]:
						if entry["width"] == original_width and entry["height"] == original_height:
							media_links.append(str(entry["url"]))
							if download:
								s_path = "downloads/" + str(entry["url"]).split("/")[-1].split("?")[0]
								ur.urlretrieve(str(entry["url"]), s_path)
					max_height = 0
					max_counter = 0
					i = 0
					if media_type == 2:
						for entry in story["video_versions"]:
							if int(entry["height"]) >= max_height:
								max_height = int(entry["height"])
								max_counter = i
							i = i + 1
						media_links.append(str(story["video_versions"][max_counter]["url"]))
						if download:
							s_path = "downloads/" + str(story["video_versions"][max_counter]["url"]).split("/")[-1].split("?")[0]
							ur.urlretrieve(str(story["video_versions"][max_counter]["url"]), s_path)

				return media_links

class InstaView:

	def __init__(self):
		pass

	def sanitizeUnderscores(self, some_string):
		return str(some_string.replace("_", "\\_"))

	def sanitizeEmoji(self, some_string):
		allowed = ["/", "\"", "{", "}", "\'", " ", "#", "@", "+", "[", "]", "(", ")", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "\\", "_", ":", "," , ".", ";", "-", "!", "?", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ]
		word = ""
		for char in some_string:
			if char.upper() in allowed:
				word = word + char
			else:
				word = word + "?"
		return str(word)

	def san(self, some_string):
		return self.sanitizeUnderscores(self.sanitizeEmoji(some_string))

	def RMDtoPDF(self):
		try:
			os.system("Rscript -e 'library(rmarkdown); render(\"instaview.Rmd\")'")
		except:
			pass
		print("If PDF file isn't created, try knitting manually!")
		return 0

	def createRMD(self, path = 0):

		#setting path
		if path != 0:
			os.chdir(path)

		# get date
		today = datetime.datetime.today().strftime('%d-%m-%Y')
		# Rmd header definition
		rmd_header = "---\ntitle: \"Instagram Data\"\nauthor: \"Micha Birklbauer\"\ndate: "+str(today)+"\noutput:\n  pdf_document:\n    toc: yes\n---\n"

		# creating new Rmd file
		with open("instaview.Rmd", "w") as rmd_file:
			rmd_file.write(rmd_header)
			rmd_file.close()

		with open("instaview.Rmd", "a") as rmd_file:

			# getting profile information
			with open("profile.json", "r", errors="replace") as profile:
				profile_content = profile.read()
				profile.close()
			profile_json = json.loads(profile_content)
			rmd_file.write("# Profile Information\n\n")
			for item in profile_json:
				w = self.sanitizeUnderscores(str(item)) + " : " + self.san(str(profile_json[item])) + "\n\n"
				rmd_file.write(w)

			# getting profile settings
			with open("settings.json", "r", errors="replace") as settings:
				settings_content = settings.read()
				settings.close()
			settings_json = json.loads(settings_content)
			rmd_file.write("# Profile Settings\n\n")
			for item in settings_json:
				w = self.sanitizeUnderscores(str(item)) + " : " + self.sanitizeUnderscores(str(settings_json[item])) + "\n\n"
				rmd_file.write(w)

			# getting profile searches
			with open("searches.json", "r", errors="replace") as searches:
				searches_content = searches.read()
				searches.close()
			searches_json = json.loads(searches_content)
			rmd_file.write("# Profile Searches\n\n")
			for item in searches_json:
				for subitem in item:
					w = self.sanitizeUnderscores(str(subitem)) + " : " + self.san(str(item[subitem])) + "\n\n"
					rmd_file.write(w)
				rmd_file.write("\\_\\_\\_\\_\\_\n\n")

			# getting profile connections
			with open("connections.json", "r", errors="replace") as connections:
				connections_content = connections.read()
				connections.close()
			connections_json = json.loads(connections_content)
			rmd_file.write("# Profile Connections \n\n")
			for item in connections_json:
				w = "## " + self.sanitizeUnderscores(str(item)) + "\n\n"
				rmd_file.write(w)
				for subitem in connections_json[item]:
					w = self.sanitizeUnderscores(str(subitem)) + " : " + self.sanitizeUnderscores(str(connections_json[item][subitem])) + "\n\n"
					rmd_file.write(w)

			# getting media data
			with open("media.json", "r", errors = "replace") as media:
				media_content = media.read()
				media.close()
			media_json = json.loads(media_content)
			rmd_file.write("# Media \n\n")
			direct_counter = 0
			for media_type in media_json:
				w = "## " + self.sanitizeUnderscores(str(media_type)) + "\n\n"
				rmd_file.write(w)
				for item in media_json[str(media_type)]:
					if media_type != "direct":
						p = str(item["path"])
						file_ending = p.split(".")[-1]
						if file_ending == "mp4":
							pp = "\n\n path\\_to\\_video : " + str(item["path"]) + "\n\n*****\n\n"
						else:
							pp = "\n\n![" + self.san(str(item["caption"])) + "](" + str(item["path"]) + ")\n\n*****\n\n"
						w = "\n\ncaption : " + self.san(str(item["caption"])) + "\n\ntaken\\_at : " + self.sanitizeUnderscores(str(item["taken_at"])) + pp
					elif media_type == "direct":
						direct_counter = direct_counter + 1
						w = "\n\ncaption : direct" + str(direct_counter) + "\n\ntaken\\_at : " + self.sanitizeUnderscores(str(item["taken_at"])) + "\n\n![" + "direct\\_picture" + str(direct_counter) + "](" + str(item["path"]) + ")\n\n*****\n\n"
					else:
						pass
					rmd_file.write(w)

			# getting comments
			with open("comments.json", "r", errors="replace") as comments:
				comments_content = comments.read()
				comments.close()
			comments_json = json.loads(comments_content)
			rmd_file.write("# Comments \n\n")
			for comment_type in comments_json:
				w = "## " + self.sanitizeUnderscores(str(comment_type)) + "\n\n"
				rmd_file.write(w)
				for item in comments_json[str(comment_type)]:
					w = "\n\n recipient : " + self.sanitizeUnderscores(str(item[2])) + "\n\n comment : " + self.san(str(item[1])) + "\n\n time : " + str(item[0]) + "\n\n*****\n\n"
					rmd_file.write(w)

			# getting messages
			with open("messages.json", "r", errors="replace") as messages:
				messages_content = messages.read()
				messages.close()
			messages_json = json.loads(messages_content)
			rmd_file.write("# Messages\n\n")
			for conversations in messages_json:
				participants = conversations["participants"]
				conversation = conversations["conversation"]
				conv_title = "## "
				for name in participants:
					conv_title = conv_title + self.sanitizeUnderscores(str(name)) + ","
				conv_title2 = conv_title.rstrip(",") + "\n\n"
				rmd_file.write(conv_title2)
				for message in conversation:
					for item in message:
						w = self.san(str(item)) + " : " + self.san(str(message[item])) + "\n\n"
						rmd_file.write(w)
					rmd_file.write("\\_\\_\\_\\_\\_\n\n")

			# credits
			w = "# Credits\n\nThis document was created using Micha Birklbauer's [Instagram JSON Viewer](https://github.com/michabirklbauer/instagram_json_viewer)."
			rmd_file.write(w)

			rmd_file.close()

		# try knitting to pdf
		self.RMDtoPDF()

if __name__ == '__main__':

	action = sys.argv[1]
	args = sys.argv[2:]

	instagram = Instagram()

	#usage: instabot channel api_token rtime stime debugging_mode user_id*
	if action == "instabot":
		i = InstaBot("instabot.cfg", str(args[0]), str(args[1]))
		user_ids_cc = args[5]
		user_ids = user_ids_cc.split(";")
		if args[4] == "true":
			i.instaBot(user_ids, int(args[2]), int(args[3]), True)
		else:
			i.instaBot(user_ids, int(args[2]), int(args[3]), False)
	elif action == "getuserid":
		print(instagram.getUserID(args[0]))
	elif action == "getusername":
		print(instagram.getUserName(args[0]))
	elif action == "getmediacount":
		print(instagram.getMediaCount(args[0]))
	elif action == "getprofilepic":
		if args[1] == "True":
			data = instagram.getProfilePic(args[0], True)
			print("Profile Picture Download finished!")
		else:
			data = instagram.getProfilePic(args[0])
			print(data)
		with open("results.json", "w") as r:
			json.dump([data], r)
			r.close()
	elif action == "getnewpost":
		if args[1] == "True":
			data = instagram.getNewPost(args[0], True)
			print("Post Download finished!")
		else:
			data = instagram.getNewPost(args[0])
			print(data[0])
		with open("results.json", "w") as r:
			json.dump(data, r)
			r.close()
	elif action == "getmedia":
		data = instagram.getMedia(args[0], True)
		with open("results.json", "w") as r:
			json.dump(data, r)
			r.close()
		print("Post Media Download finished!")
	elif action == "getstories":
		if args[1] == "True":
			data = instagram.getStories(args[0], True)
			print("Story Download finished!")
		else:
			data = instagram.getStories(args[0])
			print("Stories extracted! See Results tab!")
		with open("results.json", "w") as r:
			json.dump(data, r)
			r.close()
	elif action == "instaview":
		i = InstaView()
		i.createRMD(args[0])
		print("RMD creation successful! Created at //your_path/instaview.Rmd!")
	elif action == "loadresult":
		s = ""
		c = 1
		with open("results.json", "r") as r:
			data = json.load(r)
			for item in data:
				s = s + str(c) + " = " + str(item) + "   ;   "
				c = c + 1
			r.close()
		print(s)
	elif action == "getprivacysetting":
		if instagram.isProfilePrivate(args[0]):
			print("This profile is private!")
		else:
			print("This profile is public!")
	else:
		print("Unknown action!")
