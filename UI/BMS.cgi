#!/usr/bin/python3
import cgi
import subprocess

form = cgi.FieldStorage()
period = form.getvalue('period')
if period is None:
 period = '12'

subprocess.call(["./mkgraph/mkgraph_python.csh", period])
subprocess.call(["cp", "./mkgraph/plot.svg", "."])

fragfile = open('./mkgraph/FLAG', 'r')
FLAG = int(fragfile.read())
fragfile.close()


print('Content-Type: text/html\n\n')
print('<html>')


print('<head>')
print('<meta charset="UTF-8">')
print('<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />')


print('<link rel="stylesheet" href="./style.css">')


print('</head>')
print('<body>')
print('<img src="plot.svg"><br>')
if FLAG == 3:
 print('<p class="on">&nbsp&nbspON</p>')
if FLAG == 2:
 print('<p class="charging">&nbsp&nbspCHARGE&nbspSTOPPED</p>')
if FLAG == 1:
 print('<p class="off">&nbsp&nbspDISCHARGE&nbspSTOPPED</p>')
if FLAG == 0:
 print('<p class="off">&nbsp&nbspBMS&nbspOFF</p>')

print('<form action="BMS.cgi" method="post">')
print('<button class="btn" type="submit" name="period" value="1">1hour</button>')
print('<button class="btn" type="submit" name="period" value="3">3hours</button>')
print('<button class="btn" type="submit" name="period" value="6">6hours</button>')
print('<button  class="btn" type="submit" name="period" value="12">12hours</button>')
print('<button  class="btn" type="submit" name="period" value="24">1day</button>')
print('<button  class="btn" type="submit" name="period" value="48">2days</button>')
print('<button  class="btn" type="submit" name="period" value="168">1week</button>')
print('<button  class="btn" type="submit" name="period" value="744">1month</button>')
print('</form>')

print('<br><br>')
print('<button onclick="location.href=\'stop_charging.cgi\'" class="stop_charging">stop_charging</button>')
print('<br><br>')
print('<button onclick="location.href=\'release.cgi\'" class="release">release MOSFET</button>')
print('<br><br><br><br><br><br>')
print('<button onclick="location.href=\'stop_discharging.cgi\'" class="stop_discharging">stop_discharging</button>')
print('</body>')
print('</html>')




