import sys
import re
import gzip
import requests
import io

######
# https://github.com/nyucel/pardus-check/blob/master/get_package_info.py
# https://github.com/PardusGenc/debCompareRepo

# WARNING! Run this code in console before use this py file
# pip3 install requests

######

def get_package_info(package_info, info):
    return re.search(info+": (.*)", package_info).group(1)

def get_package_sha256sum(package_info):
    return get_package_info(package_info, 'SHA256')

def get_package_version(package_info):
    return get_package_info(package_info, 'Version')

def get_package_name(package_info):
    return get_package_info(package_info, 'Package')

def get_package_filename(package_info):
    return './' + '/'.join(get_package_info(package_info, 'Filename').split('/')[2:])

def packet1Conf():
    req = requests.get(sys.argv[1])
    buffer = io.BytesIO(req.content)
    f = gzip.open(buffer, 'rt')
    packages_file = f.read()
    f.close()
    
    packages_list = packages_file.split('\n\n')
    
    for package_info in packages_list:
        if len(package_info) < 10:
            continue
        package_filename = get_package_filename(package_info)
        package_sha256sum = get_package_sha256sum(package_info)
        package_version = get_package_version(package_info)
        sha256_1[package_filename] = package_sha256sum
        version_1[package_filename] = package_version


def packet2Conf():
    req = requests.get(sys.argv[2])
    buffer = io.BytesIO(req.content)
    f = gzip.open(buffer, 'rt')
    packages_file = f.read()
    f.close()
    
    packages_list = packages_file.split('\n\n')
    
    for package_info in packages_list:
        if len(package_info) < 10:
            continue
        package_filename = get_package_filename(package_info)
        package_sha256sum = get_package_sha256sum(package_info)
        package_version = get_package_version(package_info)
        sha256_2[package_filename] = package_sha256sum
        version_2[package_filename] = package_version

def samePacketName():

    counter = 0
    counter2 = 0
    s=[]

    for key, value in sha256_1.items():

        if sha256_2.get(key) != None:

            if value==sha256_2.get(key):    #same version
                counter += 1
            else:                           #different version
                counter2 += 1
                s.append(key)


    file = open("SamePacketNameAndSameVersion.txt","w")
    file.write(str(counter))
    file.close()

    file2 = open("SamePacketNameAndDifferentVersion.txt","w")
    file2.write(str(counter2)+"\n")
    while (len(s) != 0):
        file2.write(s.pop()+"\n")
    file2.close()



def checkFirstPacket():

    counter = 0
    s = []

    for key, value in sha256_1.items():
        if sha256_2.get(key) == None:
            counter += 1
            s.append(key)

    file = open("D1_DifferentPackets.txt","w")
    file.write(str(counter)+"\n")
    while (len(s) != 0):
        file.write(s.pop()+"\n")
    file.close()


def checkSecondPacket():

    counter = 0
    s = []

    for key, value in sha256_2.items():
        if sha256_1.get(key) == None:
            counter += 1
            s.append(key)

    file = open("D2_DifferentPackets.txt","w")
    file.write(str(counter)+"\n")
    while (len(s) != 0):
        file.write(s.pop()+"\n")
    file.close()


sha256_1 = {}
version_1 = {}

sha256_2 = {}
version_2 = {}


packet1Conf()
packet2Conf()
samePacketName()
checkFirstPacket()
checkSecondPacket()







