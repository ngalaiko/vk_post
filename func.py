import vk
import time
import logging

logging.basicConfig(
	format = u'%(levelname)-8s [%(asctime)s] %(message)s', 
	level = logging.INFO,
	filename = u'log.log'
	)

BUF_SIZE = 1000

def auth(vk_token, vk_login, vk_password):
	vk_api = None

	if vk_token:
		session = vk.AuthSession(access_token=vk_token)

		vk_api = vk.API(session)
	elif vk_login and vk_password:
		session = vk.AuthSession(
			app_id='5844641', 
			user_login = vk_login, 
			user_password = vk_password, 
			scope = 'wall,photos,offline')

		vk_api = vk.API(session)

	return vk_api

def me(vk_api):
	response = vk_api.users.get()
	sleep()
	current_id = response[0]['uid']

	return current_id

def get_posted(vk_api, group_id):
	group_id = "-" + group_id

	posted = []

	count=1000
	offset=0
	while True:
		posts = vk_api.wall.get(
			owner_id=group_id, 
			filter="owner",
			count=count,
			offset=offset)

		sleep()

		posts = posts[1:]

		if len(posts) == 0:
			break

		for post in posts:
			try:
				attachments = post["attachments"]
				for attachment in attachments:
					if attachment["type"] == "photo":
						posted.append(attachment["photo"])
			except:
				pass

		offset += count

		logging.info("Fetched posted photos")

	return posted

def get_buffer(buff, vk_api, album_id, group_id):
	user_id = me(vk_api)
	posted = get_posted(vk_api, group_id)

	posted_ids = []
	for photo in posted:
		posted_ids.append(int(photo["pid"]))

	offset = 0
	count=1000
	while len(buff) < BUF_SIZE:
		photos = vk_api.photos.get(
			owner_id=user_id, 
			album_id=album_id,
			rev=1,
			extended=1,
			offset=offset,
			count=count)

		sleep()

		logging.info("Fetched photos from album")

		for photo in photos:
			pid = int(photo["pid"])
			likes = photo["likes"]["count"]
			if not pid in posted_ids and likes > 0:
				buff.append(photo)	

		offset += count

	logging.info("Buffer filled")

def post_from_buffer(vk_api, buff, group_id):
	group_id = "-" + group_id

	photo = buff.pop(0)
	logging.info("Pop from buffer. %s left", len(buff))

	attachment = "photo" + \
		str(photo["owner_id"]) + \
		"_" + \
		str(photo["pid"])

	vk_api.wall.post(
		owner_id=group_id,
		from_group=1,
		attachments=attachment,
		signed=0)

	logging.info("Posted photo to group wall")

def sleep():
	time.sleep(1)