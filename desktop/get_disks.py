import subprocess
import sys
import json

disk_name=sys.argv[1]
user_name=sys.argv[2] if len(sys.argv) > 2 else 'rahul'
user_id= subprocess.run(['id','-u',user_name],stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','')
group_id= subprocess.run(['id','-g',user_name],stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','')
device_cmd_arguments = ['lsblk', '-o', 'NAME,SIZE,TYPE,UUID,VENDOR,MODEL,LABEL,FSTYPE', '--json']
device_outputs = subprocess.run(device_cmd_arguments, stdout=subprocess.PIPE)
device_obj = json.loads(device_outputs.stdout)

FSTAB_TEMPLATE='UUID={} /media/{}/{} {} {} 0 0'

def get_filesystem_string(fstype):
    if fstype == 'ntfs':
       return 'ntfs-3g'
    return fstype

def get_fs_options(fstype):
    if fstype == 'ntfs':
       return 'rw,auto,user,fmask=133,dmask=022,uid={},gid={}'.format(user_id,group_id)
    if fstype == 'exfat':
       return 'defaults,uid={},gid={}'.format(user_id,group_id)
    if fstype == 'ext4':
       return 'noatime,errors=remount-ro'

for d in device_obj['blockdevices']:
    if d['model'] == disk_name:
       for idx,p in enumerate(d['children']):
           fstype = p['fstype']
           label = p['label'] if p['label'] != 'null' else idx 
           print(FSTAB_TEMPLATE.format(p['uuid'],user_name,p['label'],get_filesystem_string(fstype),get_fs_options(fstype)))
