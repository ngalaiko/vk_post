#Vk post

This script will post photos from user album to group wall. 

Note: if you are using token, it should have `wall,photos,offline` permissions.

##Install
```bash
pip3 install -r requirements.txt 
```

##Usage
```bash
login with password:
	python3 main.py -vl <vk_login> -vp <vk_password>
```
```bash
login with token:
	python3 main.py -vt <vk_access_token> -aid<album_id> -gid<group_id> -i<interval_in_seconds>
```
