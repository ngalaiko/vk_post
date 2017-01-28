import argparse
import sys
import os
import time
import func

def create_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-vl', '--vk-login', default = None)
	parser.add_argument('-vp', '--vk-password', default = None)
	parser.add_argument('-vt', '--vk-token', default = None)
	parser.add_argument('-gid', '--group-id', default = None)
	parser.add_argument('-aid', '--album-id', default = None)
	parser.add_argument('-i', '--interval', default = None)

	return parser

if __name__ == '__main__':
	parser = create_parser()
	namespace = parser.parse_args(sys.argv[1:])

	if (not namespace.vk_login and not namespace.vk_password) and (not namespace.vk_token):
		print('You should use login and password or token!')
		sys.exit()

	if not namespace.group_id or not namespace.album_id or not namespace.interval:
		print('You should use all flags!')
		sys.exit()

	vk_api = func.auth(
		namespace.vk_token,
		namespace.vk_login,
		namespace.vk_password)

	buff = []
	while True:
		if len(buff) == 0:
			func.get_buffer(buff, vk_api, namespace.album_id, namespace.group_id)

		func.post_from_buffer(vk_api, buff, namespace.group_id)

		time.sleep(int(namespace.interval))
