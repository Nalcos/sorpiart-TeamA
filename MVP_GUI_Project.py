from tkinter import *
from pix2music import *
from tkinter.ttk import Notebook
import gpiozero
from signal import pause
from subprocess import Popen

main = Tk()
main.title("My Fantastic GUI")

tabControl = Notebook(main)
tabControl.pack(expand = True, fill='both',side=LEFT)

PixelFrame = Frame(tabControl)
CanvasFrame = Frame(tabControl)
ButtonFrame = Frame(main)


#Pixel Button Function
def press(get):
    x=get[0]; y=get[1]
    if toggle[x][y] == 0:
        toggle[x][y] = 1
        button[x][y].config(bg="green")
        
    else:
        toggle[x][y] = 0
        button[x][y].config(bg="grey")
    print("Toggle is {}". format(toggle))

#Canvas Function
def savePosn(event):
    global lastx, lasty
    lastx, lasty = event.x, event.y    
    toggleX = int(lastx/45)
    toggleY = int(lasty/47.5)
    print(toggleX,toggleY)
    get = [toggleY,toggleX]
    draw(get)
    
def addLine(event):
    canvas.create_line((lastx, lasty, event.x, event.y))
    savePosn(event)
    
def draw(get):
    x=get[0]; y=get[1]
    if toggleDraw[x][y] == 0:
        toggleDraw[x][y] = 1

#Play Function
def play():
    global toggle,button
    print("toggle is {}".format(toggle))
    
    #Soundtype
    soundtype=soundtypevar.get()
    
    #BPM
    bpmvalue=  bpm.get()
    
    #Note Origin
    note = key_inside.get()
    
    #Mode checking
    #Integrate Music
    if tabControl.tab(tabControl.select(), "text") == "Button Mode":
        pix2music(soundtype,bpmvalue,note,toggle)
    elif tabControl.tab(tabControl.select(), "text") == "Canvas Mode":
        pix2music(soundtype,bpmvalue,note,toggleDraw)
    
#Clear Function
def clear():
    global toggle,button
    for i in range(R):
        for j in range(C):
            toggle[i][j]= 0
            button[i][j].config(bg="grey")
        for j in range(CanvasC):
            toggleDraw[i][j]= 0
    print("Toggle is {}". format(toggle))
    print("Toggle Draw is {}". format(toggleDraw))
    canvas.delete("all")

#Button Volume Functions
def increase_volume():
    Popen(['amixer','set', 'PCM', '500+'])
    pix2music('sine',180,'D4',[[1]])
    
def decrease_volume():
    Popen(['amixer','set', 'PCM', '500-'])
    pix2music('sine',180,'D4',[[1]])
    
def mute():
    Popen(['amixer','set', 'PCM', 'toggle'])
    pix2music('sine',180,'D4',[[1]])


R = 9
C = 15
CanvasC = 15

#Toggle List (button)
toggle = [i for i in range(R)]
for i in range(R):
    toggle[i] = [j for j in range(C)]
    for j in range(C):
        toggle[i][j]= 0
print("Toggle is {}". format(toggle))

toggleDraw = [i for i in range(R)]
for i in range(R):
    toggleDraw[i] = [j for j in range(CanvasC)]
    for j in range(CanvasC):
        toggleDraw[i][j]= 0
print("Toggle Draw is {}". format(toggleDraw))

#Pixel List and Button Creation

button = [i for i in range(R)]
for x in range(R):
    button[x] = [j for j in range(C)]
    for y in range(C):
        button[x][y] = Button(PixelFrame, text=f"{x}", bg="grey", width=2, height=2,
                              command = lambda get = [x,y]: press(get))
        button[x][y].grid(row=x, column=y)
        
#Drawing Canvas
canvas = Canvas (CanvasFrame,height=R*47.5,width=CanvasC*45,bd=1,relief='ridge')
canvas.pack()
canvas.bind("<Button-1>", savePosn)
canvas.bind("<B1-Motion>", addLine)


#BPM Slider
bpmlabel = Label(ButtonFrame,text="BPM:")
bpm=Scale(ButtonFrame, from_=60, to=180, orient=HORIZONTAL)
bpmlabel.pack()
bpm.pack()

#SOUNDTYPE DROPDOWN
#label
soundtypelabel=Label(ButtonFrame,text="SOUNDTYPE: ")
soundtypelabel.pack()

#options
soundtypeoptions=[
    'pluck',
    'sine',
    'square',
    'triangle',
    'sawtooth',
    'trapezium'
]

#datatype
soundtypevar=StringVar()

#set option menu
soundtypevar.set('pluck')

#menu
soundtypemenu=OptionMenu(ButtonFrame,soundtypevar,*soundtypeoptions)
soundtypemenu.pack()



#Note Origin Input Creation
key = ['C1','C2','C3','C4','C5','C6']

key_inside = StringVar()
key_inside.set(key[3])

noteoriginlabel = Label(ButtonFrame,text="NOTE ORIGIN:")
key = OptionMenu(ButtonFrame, key_inside, *key)

noteoriginlabel.pack()
key.pack()

#Play Button Creation
Play = Button(ButtonFrame,text="Play",command=play, width=5, height=2)
Play.pack()

#Clear Button Creation
Clear = Button(ButtonFrame,text="Clear",command=clear, width=5, height=2)
Clear.pack()

#Physical Volume Button
button_up = gpiozero.Button(21)
button_up.when_pressed=increase_volume
button_down = gpiozero.Button(20)
button_down.when_pressed=decrease_volume
button_mute = gpiozero.Button(26)
button_mute.when_pressed=mute

main.attributes("-fullscreen", True)
PixelFrame.pack(fill='both',expand=True)
CanvasFrame.pack(fill='both',expand=True)
ButtonFrame.pack(side=RIGHT)

#Mode Tabs
tabControl.add(PixelFrame, text='Button Mode')
tabControl.add(CanvasFrame, text='Canvas Mode')

print(tabControl.tab(tabControl.select(), "text"))

main.mainloop()
pause()