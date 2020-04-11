import os
import stagger
import pymysql
import time
import json
import subprocess

# from PIL import Image

print("Init VARS..")
# sql
sql_insert = "INSERT FROM tracks (id,uid,title,public,description,,name,tag,art,size) VALUES (" \
             "f_uid,f_title,f_public,f_description,f_,f_name,f_tag,f_art,f_size) "
sql_update = "UPDATE tracker SET uid=f_uid,title=f_title,public=f_public,description=f_description" \
             ",=f_,name=f_name,tag=f_tag,art=f_art,size=f_size WHERE id=f_id"
sql_last_id = "select id from tracks ORDER BY id DESC LIMIT 1"
# cmd
cmd_lns = "ln -s src dest"
# core
music_na_file = os.path.abspath('.') + '/music_na.json'
music_src_dir = "/media/Lexar64/Music"
music_import_dir = "/media/Lexar64/insides/phpsound/uploads/tracks"
music_cover_dir = "/media/Lexar64/insides/phpsound/uploads/covers"
music_list = []
music_format = ["flac", "wav", "mp3", "ogg"]

# Key = Music_Path Value = List [0]=artist [1]=title [2]=cover
music_na = {}
# Load
if os.path.exists(music_na_file):
    with open(music_na_file, 'r') as fd:
        music_na = json.loads(fd.read())
mysql_ip = "localhost"
mysql_port = 3306
mysql_ur = "root"
mysql_pd = "pd"
mysql_db = "music"
print("Inited.")


def bad_name(name):
    return name.encode('utf8', 'ignore').decode('utf8')


# Get music list
print('Getting Music ON:', music_src_dir)
for root, dirs, files in os.walk(music_src_dir):
    for filename in files:
        if filename.split('.')[-1] in music_format:
            bad_n = bad_name(filename)
            if filename in music_na:
                print('Music:', bad_n, 'exist in dict.')
                continue
            music_list.append(filename)
            print('Music:', bad_n, 'added to list.')

print('Get Done!')
print('Total Add Music:', len(music_list))

# Diving music name and artist
print('Diving name and artist..')
for pm in music_list:
    s = pm.split('.')[0:-1]
    m = ''
    for p in s:
        m += p
    m = m.replace(' ', '').split('-')
    music_na[pm] = [m[0], m[-1]]
    print([m[0], m[-1]])
print('Dive Done!')

# Get music cover
for pc in music_list:
    bad_pc = bad_name(pc)
    path = music_src_dir + '/' + pc
    try:
        pg = stagger.read_tag(path)
        cover = pg[stagger.id3.APIC][0].data
        cname = 'ipm_' + str(time.time()).replace('.', '_') + '.png'
        print('Music:', bad_pc, 'Cover:', cname)
    except stagger.errors.NoTagError:
        print('Music:', bad_pc, 'Not tag found!!')
        music_na[pc].append('default.png')
        continue
    else:
        with open(music_cover_dir + '/' + cname, 'wb') as fd:
            fd.write(cover)
        print('Write Done:', cname)
        music_na[pc].append(cname)

# Create soft links
print('Ready to create soft links.')
for lns in music_list:
    end_f = lns.split('.')[-1]
    mname = 'ipm_' + str(time.time()).replace('.', '_') + '.' + end_f
    music_na[lns].append(mname)
    subprocess.call(['ln', '-s', music_src_dir + '/' + lns, music_import_dir + '/' + mname])
    os.system(f_cmd)
    print('Music:', bad_name(lns), 'Soft_Link:', mname)

# Save dict
with open(music_na_file, 'w+') as fd:
    fd.write(json.dumps(music_na))

print('Preparing to connect mysql..')
# db = pymysql.connect(host=mysql_ip,
#                      user=mysql_ur,
#                      password=mysql_pd,
#                      db=mysql_db,
#                      port=mysql_port,
#                      charset='utf8mb4', )
# cursor = db.cursor()
#
# cursor.execute()
