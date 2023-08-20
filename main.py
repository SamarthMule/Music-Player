from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
import shutil

root = Tk()
root.title("Samarth's Music Player")
root.geometry("700x530")


pygame.mixer.init()
global paused
paused = False

def play_time():
    if stopped:
        return
    current_time = pygame.mixer.music.get_pos() / 1000
    converted_time = time.strftime('%M:%S',time.gmtime(current_time))
    
    song = song_box.get(ACTIVE)
    song =f"D:/Python Programs/Music Player/music/{song}.mp3"
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    converted_song_length = time.strftime('%M:%S',time.gmtime(song_length))
    current_time +=1
    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f"Time Elapsed : {converted_song_length}")
    if not paused:
        pass
    elif int(my_slider.get()) == int(current_time):
        slider_position = int(song_length)
        my_slider.config(to=slider_position,value=int(current_time))
    else:
        slider_position = int(song_length)
        my_slider.config(to=slider_position,value=int(my_slider.get()))      
        converted_time = time.strftime('%M:%S',time.gmtime(int(my_slider.get())))
        status_bar.config(text=f"Time Elapsed : {converted_time} of {converted_song_length}")     
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    status_bar.after(1000,play_time)


def Add_song():
    song = filedialog.askopenfilename(initialdir="Music Player/music/",title="Choose A Song",filetypes=(("mp3 file","*.mp3"), ))
    if "D:/Python Programs/Music Player/music/" not in song:
        shutil.copy(song,"D:/Python Programs/Music Player/music/")
        s = song.split("/")
        song = s[-1]
    song = song.replace("D:/Python Programs/Music Player/music/","")
    song = song.replace(".mp3","")
    song_box.insert(END,song)

def Add_many_songs():
    songs = filedialog.askopenfilenames(initialdir="Music Player/music/",title="Choose A Song",filetypes=(("mp3 file","*.mp3"), ))
    for song in songs:
        if "D:/Python Programs/Music Player/music/" not in song:
            shutil.copy(song,"D:/Python Programs/Music Player/music/")
            s = song.split("/")
            song = s[-1]
        song = song.replace("D:/Python Programs/Music Player/music/","")
        song = song.replace(".mp3","")
        song_box.insert(END,song)

    
def play():
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    song =f"D:/Python Programs/Music Player/music/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    global paused
    paused = True
    play_time()

global stopped
stopped = False

def stop():
    
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    global paused
    paused = False
    status_bar.config(text="Status Bar")
    my_slider.config(value=0)
    global stopped
    stopped = True


def pause():
    global paused
    if paused:
        pygame.mixer.music.pause()
        paused = False
    else:
        pygame.mixer.music.unpause()
        paused = True

def next_song():
    status_bar.config(text="Status Bar")
    my_slider.config(value=0)
    next_one = song_box.curselection()
    next_one = next_one[0] + 1
    song = song_box.get(next_one)
    song =f"D:/Python Programs/Music Player/music/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    slider_position = int(song_length)
    my_slider.config(to=slider_position,value=0)
    
    global paused
    paused = True
    song_box.select_clear(0,END)
    song_box.activate(next_one)
    song_box.select_set(next_one,last=None)
    
def previous_song():
    status_bar.config(text="Status Bar")
    my_slider.config(value=0)
    next_one = song_box.curselection()
    next_one = next_one[0] - 1
    song = song_box.get(next_one)
    song =f"D:/Python Programs/Music Player/music/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    slider_position = int(song_length)
    my_slider.config(to=slider_position,value=0)
    global paused
    paused = True
    song_box.select_clear(0,END)
    song_box.activate(next_one)
    song_box.select_set(next_one,last=None)


def Delete_song():
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()
    global paused
    paused = False
    status_bar.config(text="Status Bar")
    
def Delete_all_song():
    stop()
    song_box.delete(0,END)
    pygame.mixer.music.stop()
    global paused
    paused = False
    status_bar.config(text="Status Bar")
    
def slide(x):
    song = song_box.get(ACTIVE)
    song = f"D:/Python Programs/Music Player/music/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0,start=int(my_slider.get()))
    
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

master_frame = Frame(root)
master_frame.pack(pady=10)

song_box = Listbox(master_frame,bg="black",fg="green",width=50,selectbackground="lightgreen",
                   foreground="green",selectforeground="black",font=("Times",15))
song_box.grid(row=0,column=0,pady=10)

back_btn_img = PhotoImage(file="Images/back.png")
forward_btn_img = PhotoImage(file="Images/next.png")
play_btn_img = PhotoImage(file="Images/play.png")
pause_btn_img = PhotoImage(file="Images/pause.png")
stop_btn_img = PhotoImage(file="Images/stop.png")


control_frame = LabelFrame(master_frame,text="Controls")
control_frame.grid(row=1,column=0,pady=10)

volume_frame = LabelFrame(master_frame,text="Volume")
volume_frame.grid(row=0,column=1,padx=10,pady=10)

back_button = Button(control_frame,image=back_btn_img,borderwidth=0,command=previous_song)
forward_button = Button(control_frame,image=forward_btn_img,borderwidth=0,command=next_song)
play_button = Button(control_frame,image=play_btn_img,borderwidth=0,command=play)
pause_button = Button(control_frame,image=pause_btn_img,borderwidth=0,command=pause)
stop_button = Button(control_frame,image=stop_btn_img,borderwidth=0,command=stop)

back_button.grid(row=0,column=0,padx=5)
forward_button.grid(row=0,column=1,padx=5)
play_button.grid(row=0,column=2,padx=5)
pause_button.grid(row=0,column=3,padx=5)
stop_button.grid(row=0,column=4,padx=5)

my_menu = Menu(root)
root.config(menu=my_menu)

add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs",menu=add_song_menu)
add_song_menu.add_command(label="Add one song to playlist",command=Add_song)
add_song_menu.add_command(label="Add many song to playlist",command=Add_many_songs)

remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs",menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a song from playlist",command=Delete_song)
remove_song_menu.add_command(label="Delete all songs from playlist",command=Delete_all_song)

status_bar = Label(root,text="Status Bar",bd=1,relief=GROOVE,anchor=E,font=("Times",25,"bold"),background="lightgray")
status_bar.pack(fill=X,side=BOTTOM,ipady=20)

style = ttk.Style()
style.theme_use('clam')
style.configure('Horizontal.TScale',background='green',troughcolor='lightgreen',troughrelief=GROOVE)
style.configure('Vertical.TScale',background='blue',troughcolor='lightblue',troughrelief=GROOVE)

my_slider = ttk.Scale(master_frame,from_=0,to=100,orient=HORIZONTAL,value=0,command=slide,length=400)
my_slider.grid(row=2,column=0,pady=20)

volume_slider = ttk.Scale(volume_frame,from_=1,to=0,orient=VERTICAL,value=1,command=volume,length=200)
volume_slider.pack()

root.mainloop()