import serial
from Tkinter import *
import struct

PORT = 'COM5'
BAUDRATE = 115200

print "Wolfmote Server"
print "Port :", PORT, "Baudrate : ", BAUDRATE

root = None
serialport = None
canvas = None
joystick = (128, 128)
buttons = (2, 2, 2)
angle = 0

def drawcircle(canv, x, y, rad, filltype):
    # changed this to return the ID
    return canv.create_oval(x-rad, y-rad, x+rad, y+rad, width=1, fill=filltype)

def redraw():
    global root
    global canvas
    global joystick
    global buttons
    global angle

    #print "draw"
    canvas.itemconfig(text, text='Angle : %.1f' % angle)
    #print angle
    (x, y) = joystick
    #print x, y
    x = int((x / 256.0) * 120) + 40
    y = int((1 - (y / 256.0)) * 120) + 40
    canvas.coords(circ2, x - 20, y - 20, x + 20, y + 20)

    (c, z, trigger) = buttons
    #print c, z
    if c == 0:
        canvas.itemconfig(circ3, fill='red')
    else:
        canvas.itemconfig(circ3, fill='black')
    if z == 0:
        canvas.itemconfig(circ4, fill='red')
    else:
        canvas.itemconfig(circ4, fill='black')
    if trigger == 0:
        canvas.itemconfig(circ5, fill='red')
    else:
        canvas.itemconfig(circ5, fill='black')
    root.after(100, redraw)

def getserial():
    global root
    global serialport
    global joystick
    global buttons
    global angle
    #print "serial"
    
    data = serialport.read(100)
    lines = data.split('\n')
    for l in lines[:-1]:
        if l.startswith('gun'):
            print l
            toks = l.split()
            try:
                angle = float(toks[1])
                x = int(toks[4])
                y = int(toks[5])
                c = int(toks[6])
                z = int(toks[7])
                trigger = int(toks[8])
                joystick = (x, y)
                buttons = (c, z, trigger)
            except:
                pass
        elif l.startswith('nun'):
            toks = l.split()
            try:
                x = int(toks[1])
                y = int(toks[2])
                c = int(toks[6])
                z = int(toks[7])
                joystick = (x, y)
                buttons = (c, z)
            except:
                pass
    root.after(10, getserial)

def findPacketMarker():
    global serialport

    marker = 'Wolf'
    index = 0
    print "x",

    while index < 4:
        char = serialport.read()
        if char == marker[index]:
            index += 1
        else:
            index = 0

def getserial_binary():
    global root
    global serialport
    global joystick
    global buttons
    global angle
    global aligned
    #print "serial"

    if serialport.inWaiting() > 40:
        serialport.read(20)

    if not aligned:
        findPacketMarker()
        aligned = True
        data = 'Wolf'
    else:
        data = ''
    
    while len(data) < 20:
        newdata = serialport.read(20 - len(data))
        data = data + newdata
    #print len(data), serialport.inWaiting()
    if not data[0:4] == 'Wolf':
        print "Packet error"
        aligned = False
    else: 
        (_, angle, _, _, x, y, b, _) = struct.unpack('<ffffBBBB', data)
        joystick = (x, y)
        buttons = (b & 0x01, b & 0x02, b & 0x04)

        if not b & 0x04:
            print ".",

    #root.after(0, getserial_binary)

    
 
if __name__ == '__main__':
    root = Tk()
    canvas = Canvas(root, width=300, height=200, bg='white')
    canvas.pack()
    canvas.pack(expand=YES, fill=BOTH)
    text = canvas.create_text(50,10, text="Angle : ---")

    circ1=drawcircle(canvas,100,100,60, 'blue')          
    circ2=drawcircle(canvas,100,100,20, 'red')
    circ3=drawcircle(canvas,200,100,10, 'black')
    circ4=drawcircle(canvas,200,140,10, 'black')
    circ5=drawcircle(canvas,200,180,10, 'black')

    serialport = serial.Serial(PORT, BAUDRATE, timeout=0)
    aligned = False
    '''
    root.after(1000, redraw)
    root.after(100, getserial_binary)
    root.mainloop()
    '''
    while True:
        getserial_binary()

'''
while True:
    data = serialport.read(100)
    lines = data.split('\n')
    for l in lines:
        if l.startswith('euler'):
            print l
        elif l.startswith('nun'):
            print l
'''

