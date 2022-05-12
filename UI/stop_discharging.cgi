#!/usr/bin/python
import cgi
import subprocess

import binascii

fragfile = open('./mkgraph/FLAG_btn', 'w')
fragfile.write('1')
fragfile.close()




print('Content-Type: text/html\n\n')
print('<html>')


print('<head>')
print('<meta charset="UTF-8">')
print('<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />')

print('<meta http-equiv="refresh" content="1;URL=BMS.cgi">')


print('</head>')
print('<body>')

print('wait redirect')



print('</body>')
print('</html>')

