from tkinter import *
import time
from picamera import PiCamera
from fractions import Fraction
import os
from tkinter import messagebox



window = Tk()

cancel = False
camera = PiCamera()


def take_picture(i):
	filename = ('/home/pi/tl/image%05d.jpg'%i)
	camera.capture(filename)
from tkinter import messagebox
def dark_mode():
        camera.framerate=Fraction(1/6)
        camera.shutter_speed=600000
        camera.exposure_mode = 'off'
        camera.iso=800


class timer_status:
    def __init__(self, how_many, seconds_delay, progress):
        self.cancel = False
        self.how_many = how_many
        self.seconds_delay = seconds_delay
        self.last_tick_time = time.time()
        self.progress = progress
        self.image_number = 0


    def get_canceled(self):
        #print("get_canceled",self.cancel)
        return self.cancel

    def set_canceled(self, canceled):
        self.cancel = canceled

    def set_delay(self,delay):
        self.seconds_delay = delay

    def set_how_many(self,how_many):
        self.how_many = how_many

    def get_progress(self):
        return self.progress

    def tick(self):
        if time.time() >= self.last_tick_time + self.seconds_delay:
            self.last_tick_time = time.time()
            print("   GO!",self.how_many)
            self.progress.configure(text="{} left".format(self.how_many))
            self.how_many = self.how_many - 1
            if self.how_many <= 0:
                self.cancel = True
                self.progress.configure(text='done')
                global_stat.set_canceled(True)
            take_picture(self.image_number)
            self.image_number = self.image_number + 1



global_stat = timer_status(0, 1,None)

window.title("timelapse")
window.geometry('1000x500')

lbl = Label(window, text="Frame count", anchor=W, width = 15)
lbl.grid(column=0, row=0)
def_val = StringVar(window, "1000")
num_txt = Entry(window, width=10,textvariable=def_val)
num_txt.grid(column=1, row=0)

billed_lbl = Label(window, text="seconds delay", anchor=W, width = 15)
billed_lbl.grid(column=0, row=1)
def_sec = StringVar(window, "5")
seconds_txt = Entry(window, width=10,textvariable=def_sec)
seconds_txt.grid(column=1, row=1)

def do_timer(stat):
    stat.tick()
    if not global_stat.get_canceled():
        window.after(1000, do_timer,stat)
    else:
        stat.get_progress().configure(text='CANCELED')


def click_time_check():
    num_frames = num_txt.get()
    delay = seconds_txt.get()
    total_seconds = int(num_frames) * int(delay)
    print("total seconds {}".format(total_seconds))
    total_minutes = total_seconds/60
    print("total minutes {}".format(total_minutes))
    total_hours = total_minutes/60
    print("total hours {}".format(total_hours))
    txt = "{:.2f} hours".format(total_hours)
    time_lbl.configure(text=txt)

def preview():
    camera.start_preview(fullscreen=False,window=(100,100,400,400))
    time.sleep(10)
    camera.stop_preview()


check_btn = Button(window, text="Get total time", command=click_time_check)
check_btn.grid(column=0, row=2)
time_lbl = Label(window, text="0 hours", anchor=W, width = 15)
time_lbl.grid(column=1, row=2)

def clear_directory():
        print("clear directory")
        if messagebox.askokcancel("Timelapse","OK to delete all past images?"):
                print("clearing")
                dir_name = "/home/pi/tl"
                for root,dirs,files in os.walk(dir_name):
                        for f in files:
                                whole_Filename = root+"/"+f
                                os.remove(whole_Filename)
                print("Done")


def click_start():
    num_frames = num_txt.get()
    delay = seconds_txt.get()

    global_stat = timer_status(int(num_frames), int(delay),progress_lbl)
    global_stat.set_canceled(False)
    window.after(1000, do_timer,global_stat)
    print("start")


def click_cancel():
    global_stat.set_canceled(True)
    print("cancel:",str(global_stat.get_canceled()))


start_btn = Button(window, text="start", command=click_start)
start_btn.grid(column=0, row=3)
progress_lbl = Label(window, text="---", anchor=W, width = 15)
progress_lbl.grid(column=1, row=3)

cancel_btn = Button(window, text="CANCEL", command=click_cancel)
cancel_btn.grid(column=0, row=4)

preview_btn = Button(window, text="Preview", command=preview)
preview_btn.grid(column=0, row=5)

dark_btn = Button(window, text="dark", command=dark_mode)
dark_btn.grid(column=1, row=5)

clear_btn = Button(window, text="Clear", command=clear_directory)
clear_btn.grid(column=2, row=5)


window.mainloop()


