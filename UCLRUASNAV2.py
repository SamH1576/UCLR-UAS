#! /usr/bin/env python
#
# GUI module generated by PAGE version 4.8.4
# In conjunction with Tcl version 8.6
#    Dec 09, 2016 09:38:59 PM
import sys

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

import UCLRUASNAV2_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    UCLRUASNAV2_support.set_Tk_var()
    top = UCLRUASNAV (root)
    UCLRUASNAV2_support.init(root, top)
    UCLRUASNAV2_support.setupScreenUpdating()
    root.mainloop()

w = None
def create_UCLRUASNAV(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    UCLRUASNAV2_support.set_Tk_var()
    top = UCLRUASNAV (w)
    UCLRUASNAV2_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_UCLRUASNAV():
    global w
    w.destroy()
    w = None


class UCLRUASNAV:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        self._bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        self._fgcolor = '#000000'  # X11 color: 'black'
        self._compcolor = '#d9d9d9' # X11 color: 'gray85'
        self._ana1color = '#d9d9d9' # X11 color: 'gray85' 
        self._ana2color = '#d9d9d9' # X11 color: 'gray85' 

        top.geometry("320x240")
        top.title("UCLRUASNAV")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.MissionsLabel = Label(top)
        #self.MissionsLabel.place(relx=0.06, rely=0.04, height=21, width=52)
        self.MissionsLabel.grid(row=0)
        self.MissionsLabel.configure(background="#d9d9d9")
        self.MissionsLabel.configure(disabledforeground="#a3a3a3")
        self.MissionsLabel.configure(foreground="#000000")
        self.MissionsLabel.configure(text='''Missions''')

        self.MissionFrame = Frame(top)
        #self.MissionFrame.place(relx=0.06, rely=0.13, relheight=0.19
        #       , relwidth=0.73)
        self.MissionFrame.grid(row=1)
        self.MissionFrame.configure(relief=GROOVE)
        self.MissionFrame.configure(borderwidth="2")
        self.MissionFrame.configure(background="#d9d9d9")
        self.MissionFrame.configure(width=235)

        self.Payload = Radiobutton(self.MissionFrame)
        #self.Payload.place(relx=0.04, rely=0.22, relheight=0.56, relwidth=0.3)
        self.Payload.grid(row=1, column=0)
        self.Payload.configure(activebackground="#d9d9d9")
        self.Payload.configure(activeforeground="#000000")
        self.Payload.configure(background="#d9d9d9")
        self.Payload.configure(disabledforeground="#a3a3a3")
        self.Payload.configure(foreground="#000000")
        self.Payload.configure(highlightbackground="#d9d9d9")
        self.Payload.configure(highlightcolor="black")
        self.Payload.configure(justify=LEFT)
        self.Payload.configure(text='''Payload''')
        self.Payload.configure(value="1")
        self.Payload.configure(variable=UCLRUASNAV2_support.missiontype)

        self.Recon = Radiobutton(self.MissionFrame)
        #self.Recon.place(relx=0.38, rely=0.22, relheight=0.56, relwidth=0.26)
        self.Recon.grid(row=1, column=1)
        self.Recon.configure(activebackground="#d9d9d9")
        self.Recon.configure(activeforeground="#000000")
        self.Recon.configure(background="#d9d9d9")
        self.Recon.configure(disabledforeground="#a3a3a3")
        self.Recon.configure(foreground="#000000")
        self.Recon.configure(highlightbackground="#d9d9d9")
        self.Recon.configure(highlightcolor="black")
        self.Recon.configure(justify=LEFT)
        self.Recon.configure(text='''Recon''')
        self.Recon.configure(value="2")
        self.Recon.configure(variable=UCLRUASNAV2_support.missiontype)

        self.Enduro = Radiobutton(self.MissionFrame)
        #self.Enduro.place(relx=0.68, rely=0.22, relheight=0.56, relwidth=0.28)
        self.Enduro.grid(row=1, column=2)
        self.Enduro.configure(activebackground="#d9d9d9")
        self.Enduro.configure(activeforeground="#000000")
        self.Enduro.configure(background="#d9d9d9")
        self.Enduro.configure(disabledforeground="#a3a3a3")
        self.Enduro.configure(foreground="#000000")
        self.Enduro.configure(highlightbackground="#d9d9d9")
        self.Enduro.configure(highlightcolor="black")
        self.Enduro.configure(justify=LEFT)
        self.Enduro.configure(text='''Enduro''')
        self.Enduro.configure(value="3")
        self.Enduro.configure(variable=UCLRUASNAV2_support.missiontype)

        self.PayloadFrame = Frame(top)
        #self.PayloadFrame.place(relx=0.06, rely=0.33, relheight=0.4
        #        , relwidth=0.73)
        self.PayloadFrame.grid(row=2,sticky=w)
        self.PayloadFrame.configure(relief=GROOVE)
        self.PayloadFrame.configure(borderwidth="2")
        self.PayloadFrame.configure(relief=GROOVE)
        self.PayloadFrame.configure(background="#d9d9d9")
        self.PayloadFrame.configure(width=235)

        self.DistLabel = Message(self.PayloadFrame)
        #self.DistLabel.place(relx=0.21, rely=0.02, relheight=0.24, relwidth=0.51)
        self.DistLabel.grid(row=2, column=1,columnspan=2)
        self.DistLabel.configure(background="#d9d9d9")
        self.DistLabel.configure(foreground="#000000")
        self.DistLabel.configure(highlightbackground="#d9d9d9")
        self.DistLabel.configure(highlightcolor="black")
        self.DistLabel.configure(text='''Distance to Target''')
        self.DistLabel.configure(width=120)

        self.DistX1 = Message(self.PayloadFrame)
        #self.DistX1.place(relx=0.09, rely=0.23, relheight=0.24, relwidth=0.09)
        self.DistX1.grid(row=3, column=1)        
        self.DistX1.configure(background="#d9d9d9")
        self.DistX1.configure(foreground="#000000")
        self.DistX1.configure(highlightbackground="#d9d9d9")
        self.DistX1.configure(highlightcolor="black")
        self.DistX1.configure(text='''X:''')
        self.DistX1.configure(width=20)        

        self.EntryX1 = Entry(self.PayloadFrame)
        #self.EntryX1.place(relx=0.17, rely=0.25, relheight=0.21, relwidth=0.61)
        self.EntryX1.grid(row=3, column=2, padx=10)
        self.EntryX1.configure(background="white")
        self.EntryX1.configure(disabledforeground="#a3a3a3")
        self.EntryX1.configure(font="TkFixedFont")
        self.EntryX1.configure(foreground="#000000")
        self.EntryX1.configure(highlightbackground="#d9d9d9")
        self.EntryX1.configure(highlightcolor="black")
        self.EntryX1.configure(insertbackground="black")
        self.EntryX1.configure(selectbackground="#c4c4c4")
        self.EntryX1.configure(selectforeground="black")

        self.DistY1 = Message(self.PayloadFrame)
        #self.DistY1.place(relx=0.09, rely=0.44, relheight=0.24, relwidth=0.09)
        self.DistY1.grid(row=4, column=1)
        self.DistY1.configure(background="#d9d9d9")
        self.DistY1.configure(foreground="#000000")
        self.DistY1.configure(highlightbackground="#d9d9d9")
        self.DistY1.configure(highlightcolor="black")
        self.DistY1.configure(text='''Y:''')
        self.DistY1.configure(width=20)

        self.EntryY1 = Entry(self.PayloadFrame)
        #self.EntryY1.place(relx=0.17, rely=0.46, relheight=0.21, relwidth=0.61)
        self.EntryY1.grid(row=4, column=2)
        self.EntryY1.configure(background="white")
        self.EntryY1.configure(disabledforeground="#a3a3a3")
        self.EntryY1.configure(font="TkFixedFont")
        self.EntryY1.configure(foreground="#000000")
        self.EntryY1.configure(highlightbackground="#d9d9d9")
        self.EntryY1.configure(highlightcolor="black")
        self.EntryY1.configure(insertbackground="black")
        self.EntryY1.configure(selectbackground="#c4c4c4")
        self.EntryY1.configure(selectforeground="black")

        self.DistTotal1 = Message(self.PayloadFrame)
        #self.DistTotal1.place(relx=0.0, rely=0.65, relheight=0.24, relwidth=0.17)
        self.DistTotal1.grid(row=5, column=1)
        self.DistTotal1.configure(background="#d9d9d9")
        self.DistTotal1.configure(foreground="#000000")
        self.DistTotal1.configure(highlightbackground="#d9d9d9")
        self.DistTotal1.configure(highlightcolor="black")
        self.DistTotal1.configure(text='''Total:''')
        self.DistTotal1.configure(width=40)

        self.EntryTotal1 = Entry(self.PayloadFrame)
        #self.EntryTotal1.place(relx=0.17, rely=0.67, relheight=0.21
        #        , relwidth=0.61)
        self.EntryTotal1.grid(row=5, column=2)
        self.EntryTotal1.configure(background="white")
        self.EntryTotal1.configure(disabledforeground="#a3a3a3")
        self.EntryTotal1.configure(font="TkFixedFont")
        self.EntryTotal1.configure(foreground="#000000")
        self.EntryTotal1.configure(highlightbackground="#d9d9d9")
        self.EntryTotal1.configure(highlightcolor="black")
        self.EntryTotal1.configure(insertbackground="black")
        self.EntryTotal1.configure(selectbackground="#c4c4c4")
        self.EntryTotal1.configure(selectforeground="black")

        self.StatusFrame = Frame(top)
        #self.StatusFrame.place(relx=0.06, rely=0.33, relheight=0.4
        #        , relwidth=0.73)
        self.StatusFrame.grid(row=6)
        self.StatusFrame.configure(relief=GROOVE)
        self.StatusFrame.configure(borderwidth="2")
        self.StatusFrame.configure(background="#d9d9d9")
        self.StatusFrame.configure(width=235)

        self.StatusLabel = Label(self.StatusFrame)
        #self.StatusLabel.place(relx=0.03, rely=0.77, height=21, width=41)
        self.StatusLabel.grid(row=6, sticky=W+E+N+S)
        self.StatusLabel.configure(activebackground="#f9f9f9")
        self.StatusLabel.configure(activeforeground="black")
        self.StatusLabel.configure(background="#d9d9d9")
        self.StatusLabel.configure(disabledforeground="#a3a3a3")
        self.StatusLabel.configure(foreground="#000000")
        self.StatusLabel.configure(highlightbackground="#d9d9d9")
        self.StatusLabel.configure(highlightcolor="black")
        self.StatusLabel.configure(text='''Status:''')

        self.EntryStatus = Text(self.StatusFrame)
        #self.EntryStatus.place(relx=0.16, rely=0.75, relheight=0.23
        #        , relwidth=0.51)
        self.EntryStatus.grid(row=6, column=2,sticky=w)
        self.EntryStatus.configure(background="white")
        self.EntryStatus.configure(font="TkTextFont")
        self.EntryStatus.configure(foreground="black")
        self.EntryStatus.configure(highlightbackground="#d9d9d9")
        self.EntryStatus.configure(highlightcolor="black")
        self.EntryStatus.configure(insertbackground="black")
        self.EntryStatus.configure(selectbackground="#c4c4c4")
        self.EntryStatus.configure(selectforeground="black")
        self.EntryStatus.configure(width=35, height=2)
        self.EntryStatus.configure(wrap=WORD)
        
        self.btnProgram = Button(top)
        #self.btnProgram.place(relx=0.69, rely=0.88, height=24, width=57)
        self.btnProgram.grid(row=7)
        self.btnProgram.configure(activebackground="#d9d9d9")
        self.btnProgram.configure(activeforeground="#000000")
        self.btnProgram.configure(background="#d9d9d9")
        self.btnProgram.configure(command=UCLRUASNAV2_support.startMission)
        self.btnProgram.configure(disabledforeground="#a3a3a3")
        self.btnProgram.configure(foreground="#000000")
        self.btnProgram.configure(highlightbackground="#d9d9d9")
        self.btnProgram.configure(highlightcolor="black")
        self.btnProgram.configure(pady="0")
        self.btnProgram.configure(text='''Program''')

        self.btnQuit = Button(top)
        #self.btnQuit.place(relx=0.88, rely=0.88, height=24, width=34)
        self.btnQuit.grid(row=7,column=1)
        self.btnQuit.configure(activebackground="#d9d9d9")
        self.btnQuit.configure(activeforeground="#000000")
        self.btnQuit.configure(background="#d9d9d9")
        self.btnQuit.configure(command=UCLRUASNAV2_support.CloseWindow)
        self.btnQuit.configure(disabledforeground="#a3a3a3")
        self.btnQuit.configure(foreground="#000000")
        self.btnQuit.configure(highlightbackground="#d9d9d9")
        self.btnQuit.configure(highlightcolor="black")
        self.btnQuit.configure(pady="0")
        self.btnQuit.configure(text='''Quit''')



if __name__ == '__main__':
    vp_start_gui()


