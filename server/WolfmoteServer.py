import serial
from Tkinter import *

PORT = 'COM3'
BAUDRATE = 115200

print "Wolfmote Server"
print "Port :", PORT, "Baudrate : ", BAUDRATE

root = None
serialport = None
canvas = None
joystick = (128, 128)
buttons = (2, 2)

def drawcircle(canv, x, y, rad, filltype):
    # changed this to return the ID
    return canv.create_oval(x-rad, y-rad, x+rad, y+rad, width=1, fill=filltype)

def redraw():
    global root
    global canvas
    global joystick
    global buttons

    print "draw"
    (x, y) = joystick
    print x, y
    x = int((x / 256.0) * 120) + 40
    y = int((1 - (y / 256.0)) * 120) + 40
    canvas.coords(circ2, x - 20, y - 20, x + 20, y + 20)

    (c, z) = buttons
    print c, z
    if c == 0:
        canvas.itemconfig(circ3, fill='red')
    else:
        canvas.itemconfig(circ3, fill='black')
    if z == 0:
        canvas.itemconfig(circ4, fill='red')
    else:
        canvas.itemconfig(circ4, fill='black')
    root.after(1000, redraw)

def getserial():
    global root
    global serialport
    global joystick
    global buttons
    #print "serial"
    
    data = serialport.read(100)
    lines = data.split('\n')
    for l in lines:
        if l.startswith('euler'):
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
    root.after(100, getserial)

    
if __name__ == '__main__':
    root = Tk()
    canvas = Canvas(root, width=300, height=200, bg='white')
    canvas.pack()
    canvas.pack(expand=YES, fill=BOTH)
    #text = canvas.create_text(50,10, text="tk test")

    circ1=drawcircle(canvas,100,100,60, 'blue')          
    circ2=drawcircle(canvas,100,100,20, 'red')
    circ3=drawcircle(canvas,200,100,10, 'black')
    circ4=drawcircle(canvas,200,140,10, 'black')

    serialport = serial.Serial(PORT, BAUDRATE)
    root.after(1000, redraw)
    root.after(100, getserial)
    root.mainloop()

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

