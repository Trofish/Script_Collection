import re

line = re.compile("^[0-9a-f][0-9a-f]:[0-9a-f|:]{14}")


new = open("new.txt","r")
configure = open("configure.txt","w+")

mac = re.compile("^[0-9a-f][0-9a-f]:[0-9a-f|:]{14}")
str = "config macfilter add"

for i in new:
    new_mac = mac.findall(i)
    print(new_mac)
    desc = re.sub("^[0-9a-f][0-9a-f]:[0-9a-f|:]{14}(\s+)(1|Any)(\s+)(unknown)(\s+)", "", i)
    new_str = str + " %s 0 vlan79 \"%s\" \n"%(new_mac[0],desc.strip())
    configure.write(new_str)


new.close()
configure.close()
