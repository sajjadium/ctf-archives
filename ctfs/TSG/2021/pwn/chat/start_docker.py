import os
import string
import random
import binascii

IMAGE_NAME = "tsgctf-simple-chat"
NROOMID = 10

if 'BASE' in os.environ:
    BASE = os.environ['BASE'] + '/'
else:
    raise Exception("BASE is not set")

def gen_room_id():
    return ''.join(random.choices(string.ascii_letters, k=NROOMID))

def check_room_id(room_id):
    if len(room_id) != NROOMID:
        return False
    for c in room_id:
        if c not in string.ascii_letters:
            return False

    room_path = os.path.join(BASE, room_id)
    return os.path.isdir(room_path)

def main():
    print('1. create a room')
    print('2. connect to a room as a host')
    print('3. connect to a room as a client')

    s = int(input())
    if s == 1:
        import proof_of_work
        print("To prevent creating too many rooms, you have to do a little heavy PoW. I guess you don't have to create many rooms.")
        if not proof_of_work.main():
            return

        room_id = gen_room_id()
        room_dir = os.path.join(BASE, room_id)
        os.mkdir(room_dir)
        os.chmod(room_dir, 0o777)
        print(f'room id is {room_id}')
    elif s == 2 or s == 3:
        if s == 2:
            target = "HOST"
        else:
            target = "CLIENT"
        print("input a room id")
        room_id = input()
        if not check_room_id(room_id):
            print('invalid room id')
            return
        room_path = os.path.join(BASE, room_id)
        cmd = f'sudo docker run -i -v "$PWD/{room_path}:/env" {IMAGE_NAME} {target}'
        #print(cmd)
        os.system(cmd)

main()
