def signedhex(intdata):
  
 polarity = (intdata & 32768) >> 15
 absolute = intdata & 32767

 xxx = polarity * ((32767 ^ absolute) + 1) * (-1) + (1-polarity) * absolute

 return xxx



def cksum(alldata):
 x = -1

 if alldata == '':
  x = 9
  return x

 d1 = alldata[0:2]

 if d1 == '00':
  x = 0
  return x
  
 d_1 = alldata[-2:]

 if d1 != 'dd' or d_1 != '77':
  x = 2
  return x

 alllength = len(alldata)
 
 if alllength < 12 or alllength % 2 != 0:
  x = 6
  return x
  
 checksum = alldata[-6:-2]
 sum = []
 targetlength = alllength / 2 - 5
 i = 0
 while i < targetlength:
  a = i * 2 + 4
  b = i * 2 + 6
  sum.append(int(alldata[a:b], 16))
  i += 1
 #print(sum)
 datasum = 0
 for bx in sum:
  datasum = datasum + bx
 datasum_inv = hex(65535 ^ datasum - 1)
 checksum_hex = hex(int(checksum, 16))
 if datasum_inv != checksum_hex:
  x = 5
  return x

 d3 = alldata[4:6]
 if d3 != '00':
  x = 3
  return x

 d4 = alldata[6:8]
 datalength = int(d4, 16)
 length = (datalength + 7) * 2
 if alllength != length:
  x = 4
  return x

 x = 1
 return x



def errmsg(data, xx, dttm, filename_e):
 if xx == 9:
  line = dttm + ' BMS not response: code ' + str(xx) + ': ' + data + '\n' 
 elif xx == 2:
  line = dttm + ' Data not complete: code ' + str(xx) + ': ' + data + '\n' 
 elif xx == 4:
  line = dttm + ' Illegal data length: code ' + str(xx) + ': ' + data + '\n' 
 elif xx == 5:
  line = dttm + ' Data checksum error: code ' + str(xx) + ': ' + data + '\n' 
 elif xx == 3:
  line = dttm + ' BMS returns error: code ' + str(xx) + ': ' + data + '\n' 
 elif xx == 6:
  line = dttm + ' Data too short or odd: code ' + str(xx) + ': ' + data + '\n' 
 else:
  line = dttm + ' Illegal error code: code ' + str(xx) + ': ' + data + '\n' 
 f = open(filename_e,'a')
 f.write(line)
 f.close()
 return xx
 
 

######## main ######

import serial
import binascii
import time
import datetime
import numpy
 
dir = 'path/'  ######
filename_e = dir + 'error'
jj = 0

while True:

 xx = 0
 while xx == 0:
  ser = serial.Serial('/dev/ttyUSB0', '9600', timeout=0.5)
  ser.write('\xdd\xA5\x04\x00\xff\xfc\x77')
  cellvoltages = binascii.hexlify(ser.read(128))
  ser.close()

  xx = cksum(cellvoltages)

 xy = 0
 while xy == 0:
  ser = serial.Serial('/dev/ttyUSB0', '9600', timeout=0.5)
  ser.write('\xdd\xA5\x03\x00\xff\xfd\x77')
  totalvoltage = binascii.hexlify(ser.read(128))
  ser.close()

  xy = cksum(totalvoltage)  

 NOW = datetime.datetime.now()
 dttm = NOW.strftime("%Y-%m-%d %H:%M:%S")


 if xx != 1:
  xx = errmsg(cellvoltages, xx, dttm, filename_e)
  time.sleep(1)  #####
  continue 
  
 if xy != 1:
  xy = errmsg(totalvoltage, xy, dttm, filename_e)
  time.sleep(1)  #####
  continue 
  

 if jj < 23:
  jj += 1
  time.sleep(1)  #####
  continue
 jj = 0


 v = []
 i = 0
 while i < 8:
  a = i * 4 + 8
  b = i * 4 + 12
  v.append(float(int(cellvoltages[a:b], 16))/1000)
  i += 1
 
 va = []
 va.append(float(int(totalvoltage[8:12], 16))/100)
 va.append(float(signedhex(int(totalvoltage[12:16], 16)))/100)
 va.append((float(int(totalvoltage[54:58], 16))-2731)/10)
 va.append((float(int(totalvoltage[58:62], 16))-2731)/10)
 va.append(int(totalvoltage[48:50], 16))
 va.append(bin(int(totalvoltage[40:44], 16)))

 filename = dir + NOW.strftime("%Y%m%d") + '.csv'
 line = dttm
 for ax in v:
  line = line + ', ' + str(ax) 
 for ax in va:
  line = line + ', ' + str(ax) 
 line = line + '\n' 
 
 
 f = open(filename,'a')
 
 f.write(line)
 
 f.close()

 control_u = 0 
 control_l = 0 
 upper = float(numpy.loadtxt("limit", usecols=[0]))
 lower = float(numpy.loadtxt("limit", usecols=[1]))
 switch = int(numpy.loadtxt("limit", usecols=[2]))

 if va[4] == 3 : 
  for ax in v:
   if ax > upper :
    control_u = 2
   if ax < lower :
    control_l = 1
 if va[4] == 2 :
  for ax in v:
   if ax < lower :
    control_l = 1
 if va[4] == 1 :
  for ax in v:
   if ax > upper :
    control_u = 2

 if control_u == 2 or (switch == 2 and va[4] == 3) or (switch == 2 and va[4] == 1) : 
  ser = serial.Serial('/dev/ttyUSB0', '9600', timeout=0.5)
  ser.write('\xdd\x5A\xe1\x02\x00\x01\xff\x1c\x77') ### stop charging
  ser.close()
 if control_l == 1 or (switch == 1 and va[4] == 3) or (switch == 1 and va[4] == 2) : 
  ser = serial.Serial('/dev/ttyUSB0', '9600', timeout=0.5)
  ser.write('\xdd\x5A\xe1\x02\x00\x02\xff\x1b\x77') ### stop dischanging
  ser.close()

 if (va[4] == 2 or va[4] == 1) and switch == 3 :
  ser = serial.Serial('/dev/ttyUSB0', '9600', timeout=0.5)
  ser.write('\xdd\x5A\xe1\x02\x00\x00\xff\x1d\x77') ### close both
  data = binascii.hexlify(ser.read(128))
  ser.close()
 
 time.sleep(1)  #####

exit()



