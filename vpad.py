import tkinter as tk
from tkinter import ttk
from tkinter import font, filedialog, messagebox
import os
import pyttsx3
import ctypes as ct
import pickle

try:
    import speech_recognition as sr
    import socket
    import webbrowser
    import openai
    from dotenv import load_dotenv
    import json

except Exception as e:
    pass


main_application = tk.Tk()
main_application.geometry('1200x700+180+60')
main_application.minsize(770,300)
main_application.title('Vpad Text Editor')
main_application.wm_iconbitmap('Main\icons2\icon.ico')

############################## Voice Notifications #################################

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices') 

def speakfunc(audio):
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate',150)
    engine.say(audio)
    engine.runAndWait()

########################## MAIN MENU ##################################

main_menu = tk.Menu(main_application)
# file icons
new_icon = tk.PhotoImage(file='Main/icons2/new.png')
open_icon = tk.PhotoImage(file='Main/icons2/open.png')
save_icon = tk.PhotoImage(file='Main/icons2/save.png')
save_as_icon = tk.PhotoImage(file='Main/icons2/save_as.png')
exit_icon = tk.PhotoImage(file='Main/icons2/exit.png')

file = tk.Menu(main_menu, tearoff=False, bd=0)


################################# EDIT
# Edit icons
copy_icon = tk.PhotoImage(file='Main/icons2/copy.png')
paste_icon = tk.PhotoImage(file='Main/icons2/paste.png')
cut_icon = tk.PhotoImage(file='Main/icons2/cut.png')
clear_all_icon = tk.PhotoImage(file='Main/icons2/clear_all.png')
find_icon = tk.PhotoImage(file='Main/icons2/find.png')
undo_icon = tk.PhotoImage(file='Main/icons2/undo.png')
redo_icon = tk.PhotoImage(file='Main/icons2/redo.png')

edit = tk.Menu(main_menu, tearoff=False)

#################################  VIEW

### View icons
tool_bar_icon = tk.PhotoImage(file='Main/icons2/tool_bar.png')
status_bar_icon = tk.PhotoImage(file='Main/icons2/status_bar.png')

view = tk.Menu(main_menu, tearoff=False)

############################ Color theme ###################

### color theme icons
light_default_icon = tk.PhotoImage(file='Main/icons2/light_default.png')
light_plus_icon = tk.PhotoImage(file='Main/icons2/light_plus.png')
dark_icon = tk.PhotoImage(file='Main/icons2/dark.png')
fair_pink_icon = tk.PhotoImage(file='Main/icons2/fair_pink.png')
monokai_icon = tk.PhotoImage(file='Main/icons2/monokai.png')
night_blue_icon = tk.PhotoImage(file='Main/icons2/night_blue.png')
red_icon = tk.PhotoImage(file='Main/icons2/red.png')

################### COLOR DICT ##############

color_theme = tk.Menu(main_menu, tearoff=False)

theme_choice = tk.StringVar()
theme_choice.set('Light Default')
color_icons = (light_default_icon, light_plus_icon, dark_icon, fair_pink_icon, monokai_icon, night_blue_icon, red_icon)

color_dict = {         #Fg,       #Bg,      #Contrast
    'Light Default' : ('#000000', '#ffffff',''),
    'Light Plus'    : ('#990000', '#e0e0e0','#ffffff'),
    'Dark'          : ('#FFCCCB', '#2d2d2d','#3d3d3d'),
    'Fair Pink'     : ('#000000', '#ffe8e8','pink'),
    'Monokai'       : ('#d3b774', '#474747','#2e2e2e'),
    'Night Blue'    : ('#000000', '#6b9dc2','skyblue'),
    'Crimson Red'   : ('#ffff00', '#471002','#990000'),
}

############### VOICE MENU ###############

voice_change = tk.Menu(main_menu, tearoff=False)

############### VOICE DICT ###############

voice_choice = tk.StringVar()
voice_dict = {}

n = len(voices)

for i in range(0,n):
    voice_dict[i] = voices[i].name

voice_choice.set(voice_dict[0])


################### About Menu ##############

about = tk.Menu(main_menu, tearoff=False)

# cascade
main_menu.add_cascade(label='File', menu=file)
main_menu.add_cascade(label='Edit', menu=edit)
main_menu.add_cascade(label='View', menu=view)
main_menu.add_cascade(label='Color Theme', menu=color_theme)
main_menu.add_cascade(label='Voice Options', menu=voice_change)
main_menu.add_cascade(label='About', menu=about)


### SUBMENU of VoiceMenu
speed = tk.Menu(voice_change,tearoff=False)

speed_change = tk.StringVar()
speed_change.set('Normal')

speed_dict = {
    'Very Slow' :  30,
    'Slow'      :  50,
    'Normal'    :  140,
    'Fast'      :  220,
    'Very Fast' :  300,
}

voice_change.add_cascade(label='Speed',menu=speed)

# ------------------------ END MAIN MENU --------------------------------- #

########################## TOOLBAR ##################################

test_bar1 = ttk.Label(main_application)
test_bar1.pack(side=tk.TOP, fill=tk.BOTH)

tool_bar = ttk.Label(test_bar1)
tool_bar.pack(side=tk.TOP, fill=tk.Y)

## font box
font_tuple = tk.font.families()
font_family = tk.StringVar()
font_box = ttk.Combobox(tool_bar, width=30, textvariable=font_family, state='readonly')
font_box['values'] = font_tuple
font_box.current(font_tuple.index('Arial'))
font_box.grid(row=0,column=0, padx=5)

## size box
size_var = tk.IntVar()
font_size = ttk.Combobox(tool_bar, width=12, textvariable= size_var, state='readonly')
font_size['values'] = tuple(range(8,80,2))
font_size.current(2)
font_size.grid(row=0,column=1, padx=5)

## bold button
bold_icon = tk.PhotoImage(file='Main/icons2/bold.png')
bold_btn = ttk.Button(tool_bar, image=bold_icon)
bold_btn.grid(row=0,column=2, padx=5)

## italic button
italic_icon = tk.PhotoImage(file='Main/icons2/italic.png')
italic_btn = ttk.Button(tool_bar, image=italic_icon)
italic_btn.grid(row=0,column=3, padx=5)

## underline button
underline_icon = tk.PhotoImage(file='Main/icons2/underline.png')
underline_btn = ttk.Button(tool_bar, image=underline_icon)
underline_btn.grid(row=0,column=4, padx=5)

## font color button
font_color_icon =tk.PhotoImage(file='Main/icons2/font_color.png')
font_color_btn = ttk.Button(tool_bar, image=font_color_icon)
font_color_btn.grid(row=0,column=5, padx=5)

## align left button
align_left_icon = tk.PhotoImage(file='Main/icons2/align_left.png')
align_left_btn = ttk.Button(tool_bar, image=align_left_icon)
align_left_btn.grid(row=0, column=6, padx=5)

## align center button
align_center_icon = tk.PhotoImage(file='Main/icons2/align_center.png')
align_center_btn = ttk.Button(tool_bar, image=align_center_icon)
align_center_btn.grid(row=0,column=7, padx=5)

## align right button
align_right_icon = tk.PhotoImage(file='Main/icons2/align_right.png')
align_right_btn = ttk.Button(tool_bar, image=align_right_icon)
align_right_btn.grid(row=0, column=8, padx=5)

## voice input button
voice_input_icon = tk.PhotoImage(file='Main/icons2/mic.png')
voice_input_btn = ttk.Button(tool_bar, image= voice_input_icon)
voice_input_btn.grid(row=0,column=9, padx=5)

## text reader button
text_reader_icon = tk.PhotoImage(file='Main/icons2/read1.png')
text_reader_btn = ttk.Button(tool_bar, image= text_reader_icon)
text_reader_btn.grid(row=0,column=10, padx=5)

## Chatgpt results button
gpt_icon = tk.PhotoImage(file='Main/icons2/gpt.png')
gpt_btn = ttk.Button(tool_bar, image= gpt_icon)
gpt_btn.grid(row=0, column=11, padx=5)


# ------------------------ END TOOLBAR --------------------------------- #


########################## STATUS BAR ##################################

test_bar = ttk.Label(main_application)
test_bar.pack(side=tk.BOTTOM,fill=tk.X)
status_bar = ttk.Label(test_bar, text='Status Bar')
status_bar.pack(side=tk.BOTTOM, fill=tk.Y)


text_changed = False
def changed(event=None):
    global text_changed
    if text_editor.edit_modified():
        text_changed = True
        words = len(text_editor.get(1.0, 'end-1c').split())
        characters = len(text_editor.get(1.0, 'end-1c').replace(' ', '')) #for spaces not counted)
        status_bar.config(text=f"Characters : {characters} Words : {words}")
        if words==0:
            status_bar.config(text="Status Bar")

    text_editor.edit_modified(False)

# ------------------------ END STATUS BAR --------------------------------- #


########################## TEXT EDITOR ##################################

text_editor = tk.Text(main_application, undo=True)
text_editor.config(wrap='word', relief=tk.FLAT)

scroll_bar = tk.Scrollbar(main_application)
text_editor.focus_set()
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
text_editor.pack(fill=tk.BOTH, expand=True)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)

################# Text Editor Menu #############

###  font family & font size functionality

# Global Variables
current_font_family = 'Arial'
current_font_size = 12
current_font_weight = 'normal'
current_font_slant = 'roman'
current_font_underline = 'normal'
net = False

def change_font(event=None):
    global current_font_family
    current_font_family = font_family.get()
    text_editor.focus_set()
    text_editor.configure(font=(current_font_family, current_font_size,current_font_weight,
    current_font_slant))

def change_font_size(event=None):
    global current_font_size
    current_font_size = size_var.get()
    text_editor.focus_set()
    text_editor.configure(font=(current_font_family, current_font_size,current_font_weight,
    current_font_slant))

font_box.bind("<<ComboboxSelected>>", change_font)
font_size.bind("<<ComboboxSelected>>", change_font_size)

##### bold button functionality
def change_bold(event=None):
    global current_font_weight
    text_property = tk.font.Font(font=text_editor['font'])
    text_editor.focus_set()
    if text_property.actual()['weight'] == 'normal':
        current_font_weight = 'bold'
        text_editor.configure(font=(current_font_family, current_font_size, current_font_weight ,current_font_slant))
    if text_property.actual()['weight'] == 'bold':
        current_font_weight = 'normal'
        text_editor.configure(font=(current_font_family, current_font_size, current_font_weight, current_font_slant))

bold_btn.configure(command=change_bold)

##### italic button
def change_italic(event=None):
    global current_font_slant
    text_property = tk.font.Font(font=text_editor['font'])
    text_editor.focus_set()
    if text_property.actual()['slant'] == 'roman':
        current_font_slant = 'italic'
        text_editor.configure(font=(current_font_family, current_font_size, current_font_weight, current_font_slant))
    if text_property.actual()['slant'] == 'italic':
        current_font_slant = 'roman'
        text_editor.configure(font=(current_font_family, current_font_size,current_font_weight, current_font_slant))

italic_btn.configure(command=change_italic)

##### underline button
def change_underline(event=None):
    global current_font_underline
    text_property = tk.font.Font(font=text_editor['font'])
    text_editor.focus_set()
    if text_property.actual()['underline'] == 0:
        current_font_underline = 'underline'
        text_editor.configure(font=(current_font_family, current_font_size,current_font_weight, current_font_slant, current_font_underline))
    if text_property.actual()['underline'] == 1:
        current_font_underline = 'normal'
        text_editor.configure(font=(current_font_family, current_font_size, current_font_weight, current_font_slant))

underline_btn.configure(command=change_underline) 

#### font color functionality

def change_font_color():
    color_var = tk.colorchooser.askcolor()
    text_editor.configure(fg=color_var[1])
    text_editor.focus_set()

font_color_btn.configure(command=change_font_color)

#### align functionality

### align left
def align_left():
    text_content = text_editor.get(1.0, 'end')
    text_editor.tag_config('left', justify=tk.LEFT)
    text_editor.delete(1.0, tk.END)
    text_editor.insert(tk.INSERT, text_content, 'left')

align_left_btn.configure(command=align_left)

### align center
def align_center():
    text_content = text_editor.get(1.0, 'end')
    text_editor.tag_config('center', justify=tk.CENTER)
    text_editor.delete(1.0, tk.END)
    text_editor.insert(tk.INSERT, text_content, 'center')

align_center_btn.configure(command=align_center)

### align right
def align_right():
    text_content = text_editor.get(1.0, 'end')
    text_editor.tag_config('right', justify=tk.RIGHT)
    text_editor.delete(1.0, tk.END)
    text_editor.insert(tk.INSERT, text_content, 'right')

align_right_btn.configure(command=align_right)

def test_connection():
    try:
        socket.create_connection(("Google.com", 80))
        return True
    except OSError:
        return False

##### voice input
def voice_input():
    global net
    words = len(text_editor.get(1.0, 'end-1c').split())
    net = test_connection()
    text_editor.focus_set()
    if net:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                r.pause_threshold = 1
                audio = r.listen(source, timeout=3)
            except Exception as k:
                speakfunc('Please check microphone settings.')
                messagebox.showwarning('Warning', 'Please check microphone settings!!!')

        try:
            query = r.recognize_google(audio, language='en-in')   
            if words>0:  
                return ' '+query+' '
            else:
                return query+' '

        except Exception as e:
            return None 
    else:
        speakfunc('Please check network connection.')
        messagebox.showwarning('Warning', 'Please check network connection!!!')
        
def voice():
    query = voice_input()
    if query==None:
        pass
    else:
        try:
            text_editor.insert(tk.END, query.lower())
        except Exception as e:
            pass
        
voice_input_btn.configure(command=lambda: [voice()])

##### TTS Feature
def text_reader(event=None):
    try:
        text = str(text_editor.get(1.0, 'end'))
        speak(text)
        text_editor.focus_set()
    except Exception as e:
        text_editor.focus_set()
        return None

text_reader_btn.configure(command=lambda:text_reader())

##### ChatGPT Feature
def ReplyBrain(question):
    try:
        with open('Main/API/config.json') as config:
            data = json.load(config)
        API = data['openai']
        config.close

    except Exception as e:
        print(e)
        pass

    if API=="" or API==None:
        speakfunc('Please provide OpenAI API key!!!')
        messagebox.showwarning('Warning', 'Please provide OpenAI API key!!!')
    else:
        openai.api_key = API
        load_dotenv()
        completion = openai.Completion()
        try:
            response = completion.create(
                model = "text-davinci-003",
                prompt = question,
                temperature = 0.6,
                max_tokens = 150,
                top_p = 0.3,
                frequency_penalty = 0.5,
                presence_penalty = 0)
            answer = response.choices[0].text.strip()
            return answer
        except Exception as e:
            messagebox.showwarning('Warning', e)
            pass

def ChatGPT(event=None):
    try:
        text = str(text_editor.get(1.0, 'end'))
        if text == None:
            return
        
        ans = ReplyBrain(text)
        if ans==None:
            pass
        else:
            try:
                text_editor.delete(1.0, tk.END)
                text_editor.insert(tk.END, ans)
            except Exception:
                pass
        text_editor.focus_set()

    except Exception as e:
        text_editor.focus_set()
        return None


gpt_btn.configure(command=lambda:ChatGPT())

text_editor.configure(font=('Arial', 12))
text_editor.bind('<<Modified>>', changed)
# ------------------------ END TEXT EDITOR --------------------------------- #


########################## MAIN MENU FUNCTIONALITY ##################################

### variable
url = ''

### new functionality
def new_file(event=None):
    global url
    url = ''
    text_editor.delete(1.0, tk.END)

### new command
file.add_command(label='New', image=new_icon, compound=tk.LEFT, accelerator='Ctrl+N', command=new_file)

### open functionality
def open_file(event=None):
    global url
    url = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select File', filetypes=(('Text Files', '*.txt'),('HTML Files', '*.html'),('Python Files', '*.py'), ('All Files', "*.*")))
    try:
        with open(url, 'r') as fr:
            text_editor.delete(1.0, tk.END)
            text_editor.insert(1.0, fr.read())
    except FileNotFoundError:
        return
    except :
        return
    main_application.title(os.path.basename(url))

### open command
file.add_command(label='Open', image=open_icon, compound=tk.LEFT, accelerator='Ctrl+O', command=open_file)
file.add_separator()

### save functionality
def save_file(event=None):
    global url
    try:
        if url:
            content = str(text_editor.get(1.0, tk.END))
            with open(url, 'w', encoding='utf-8') as fw:
                fw.write(content)
        else:
            url = filedialog.asksaveasfile(mode= 'w', defaultextension='.txt', filetypes=(('Text File', '*.txt'),('HTML Files', '*.html'),('Python Files', '*.py'), ('All Files', "*.*")))
            content2 = text_editor.get(1.0, tk.END)
            url.write(content2)
            url.close()
    except:
        return            
            
### save command
file.add_command(label='Save', image=save_icon, compound=tk.LEFT, accelerator='Ctrl+S', command=save_file)

### save as functionality
def save_as_file(event=None):
    global url
    try:
        content = text_editor.get(1.0, tk.END)
        url = filedialog.asksaveasfile(mode= 'w', defaultextension='.txt', filetypes=(('Text File', '*.txt'),('HTML Files', '*.html'),('Python Files', '*.py'), ('All Files', "*.*")))
        url.write(content)
        url.close()
    except:
        return

### Save as command
file.add_command(label='Save As', image=save_as_icon, compound=tk.LEFT, accelerator='Ctrl+Alt+S', command=save_as_file)
file.add_separator()

### exit functionality
def exit_file(event=None):
    global url, text_changed
    try:
        if text_changed:
            mbox = messagebox.askyesnocancel('Warning', 'Do you want to save the file ?')
            if mbox is True:
                if url:
                    content = text_editor.get(1.0, tk.END)
                    with open(url, 'w', encoding='utf-8') as fw:
                        fw.write(content)
                        main_application.destroy()
                else:
                    content2 = str(text_editor.get(1.0, tk.END))
                    url = filedialog.asksaveasfile(mode= 'w', defaultextension='.txt', filetypes=(('Text File', '*.txt'), ('All Files', "*.*")))
                    url.write(content2)
                    url.close()
                    main_application.destroy()
            elif mbox is False:
                main_application.destroy()
        else:
            main_application.destroy()
    except:
        return

### exit command
file.add_command(label='Exit', image=exit_icon, compound=tk.LEFT, accelerator='Ctrl+Q', command=exit_file)

#### find functionality
def find_func(event=None):

    def find():
        word = find_input.get()
        text_editor.tag_remove('match', '1.0', tk.END)
        matches = 0
        if word:
            start_pos = '1.0'
            while True:
                start_pos = text_editor.search(word, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f'{start_pos}+{len(word)}c'
                text_editor.tag_add('match', start_pos, end_pos)
                matches += 1
                start_pos = end_pos
                text_editor.tag_config('match', foreground = 'red', background = 'yellow') 
    
    def replace():
        word = find_input.get()
        replace_text = replace_input.get()
        content = text_editor.get(1.0, tk.END)
        new_content = content.replace(word, replace_text)
        text_editor.delete(1.0, tk.END)
        text_editor.insert(1.0, new_content)


    find_dialogue = tk.Toplevel(background='#e0e0e0')
    find_dialogue.geometry('450x250+500+200')
    find_dialogue.title('Find')
    find_dialogue.resizable(0,0)
    find_dialogue.wm_iconbitmap('Main/icons2/icon.ico')

    dark_title_bar(find_dialogue,2)

    ##frame 
    find_frame = ttk.LabelFrame(find_dialogue, text='Find/Replace')
    find_frame.pack(pady=50)

    ##labels
    text_find_label = ttk.Label(find_frame, text='Find : ')
    text_replace_label = ttk.Label(find_frame, text='Replace : ')

    ## entry
    find_input = ttk.Entry(find_frame, width=30)
    find_input.focus_set()
    replace_input = ttk.Entry(find_frame, width=30)

    ## button
    find_btn = ttk.Button(find_frame, text='Find', command=find)
    replace_btn = ttk.Button(find_frame, text='Replace', command=replace)

    ##label grid
    text_find_label.grid(row=0,column=0, padx=4, pady=4)
    text_replace_label.grid(row=1,column=0, padx=4, pady=4)

    ##entry grid
    find_input.grid(row=0,column=1, padx=4, pady=4)
    replace_input.grid(row=1,column=1, padx=4, pady=4)

    ## button grid
    find_btn.grid(row=2,column=0, padx=8, pady=4)
    replace_btn.grid(row=2,column=1, padx=8, pady=4)


    find_dialogue.mainloop()

#### undo & redo functions #####
def undo():
    try:
        text_editor.edit_undo()
    except Exception as e:
        pass
    
def redo():
    try:
        text_editor.edit_redo()
    except Exception as e:
        pass

#### Api KEY ####
def ApiKey():
    global my_data_list

    def load_file():
        with open("Main\API\config.json", "r") as file_handler:
            my_data_list = json.load(file_handler)
            api = my_data_list["openai"]
        file_handler.close
        print('file has been read and closed')
        return api

    Api_key = load_file()

    def enter():
        api = api_input.get()
        dict = {
                "openai" : api
            }
            
        my_data_list = dict

        with open("Main\API\config.json", "w") as file_handler:
            json.dump(my_data_list, file_handler, indent=4)
        file_handler.close
        print('file has been written to and closed')

    api_dialogue = tk.Toplevel(background='#e0e0e0')
    api_dialogue.geometry('450x250+500+200')
    api_dialogue.title('API Key')
    api_dialogue.resizable(0,0)
    api_dialogue.wm_iconbitmap('Main/icons2/icon.ico')

    dark_title_bar(api_dialogue,2)

    ##frame 
    api_frame = ttk.LabelFrame(api_dialogue, text='Provide API Key')
    api_frame.pack(pady=50)

    ##labels
    text_api_label = ttk.Label(api_frame, text='API : ')

    api_input = ttk.Entry(api_frame, width=30)
    api_input.insert(0, Api_key)
    api_input.focus_set()

    api_btn = ttk.Button(api_frame, text='Enter', command=enter)

    text_api_label.grid(row=0,column=0, padx=4, pady=4)

    ##entry grid
    api_input.grid(row=0,column=1, padx=4, pady=4)

    ## button grid
    api_btn.grid(row=2,column=0, padx=8, pady=4)


## edit commands
edit.add_command(label='Undo', image=undo_icon, compound=tk.LEFT, accelerator='Ctrl+Z', command=undo)
edit.add_command(label='Redo', image=redo_icon, compound=tk.LEFT, accelerator='Ctrl+Y', command=redo)
edit.add_separator()
edit.add_command(label='Copy', image=copy_icon, compound=tk.LEFT, accelerator='Ctrl+C', command=lambda:text_editor.event_generate("<<Control c>>"))
edit.add_command(label='Paste', image=paste_icon, compound=tk.LEFT, accelerator='Ctrl+V', command=lambda:text_editor.event_generate("<<Control v>>"))
edit.add_command(label='Cut', image=cut_icon, compound=tk.LEFT, accelerator='Ctrl+X', command=lambda:text_editor.event_generate("<<Control x>>"))
edit.add_command(label='Clear All', image=clear_all_icon, compound=tk.LEFT, accelerator='Ctrl+Alt+X', command= lambda:text_editor.delete(1.0, tk.END))
edit.add_separator()
edit.add_command(label='Find', image=find_icon, compound=tk.LEFT, accelerator='Ctrl+F', command=find_func)
edit.add_separator()
edit.add_command(label='Add API', image=gpt_icon, compound=tk.LEFT, accelerator='Ctrl+G', command=ApiKey)

## view check button
show_statusbar = tk.BooleanVar()
show_statusbar.set(True)
show_toolbar = tk.BooleanVar()
show_toolbar.set(True)

def hide_statusbar():
    global show_statusbar
    if show_statusbar:
        test_bar.pack_forget()
        status_bar.pack_forget()
        show_statusbar = False
    else:
        text_editor.pack_forget()
        test_bar.pack(side=tk.BOTTOM,fill=tk.X)
        status_bar.pack(side=tk.BOTTOM, fill=tk.NONE)
        text_editor.pack(fill=tk.BOTH, expand=True)
        show_statusbar = True

def hide_toolbar():
    global show_toolbar
    if show_toolbar:
        test_bar1.pack_forget()
        tool_bar.pack_forget()
        show_toolbar = False
    else:
        test_bar1.pack(side=tk.TOP,fill=tk.X)
        test_bar.pack_forget()
        status_bar.pack_forget()
        text_editor.pack_forget()
        tool_bar.pack(side=tk.TOP, fill=tk.NONE)
        test_bar.pack(side=tk.BOTTOM, fill=tk.X)
        status_bar.pack(side=tk.BOTTOM, fill=tk.Y)
        text_editor.pack(fill=tk.BOTH, expand=True)
        show_toolbar = True

view.add_checkbutton(label='Tool Bar', onvalue=True, offvalue=0, variable= show_toolbar, image=tool_bar_icon, compound=tk.LEFT, command= hide_toolbar)
view.add_checkbutton(label='Status Bar', onvalue=1, offvalue=False, variable= show_statusbar,image=status_bar_icon, compound=tk.LEFT, command= hide_statusbar)

## color theme 
def change_theme():
    chosen_theme = theme_choice.get()
    color_tuple = color_dict.get(chosen_theme)
    fg_color, bg_color, contrast = color_tuple[0], color_tuple[1], color_tuple[2]
    text_editor.config(background=bg_color, foreground=fg_color)
    test_bar1.config(background=contrast, foreground=fg_color)
    tool_bar.config(background=contrast, foreground=fg_color)
    file.config(background=bg_color, foreground=fg_color)
    edit.config(background=bg_color, foreground=fg_color)
    view.config(background=bg_color, foreground=fg_color)
    color_theme.config(background=bg_color, foreground=fg_color)
    voice_change.config(background=bg_color, foreground=fg_color)
    speed.config(background=bg_color, foreground=fg_color)
    about.config(background=bg_color, foreground=fg_color)
    my_menu.config(background=bg_color, foreground=fg_color)
    status_bar.config(background=contrast, foreground=fg_color)
    test_bar.config(background=contrast, foreground=fg_color)
    if chosen_theme=='Dark' or chosen_theme=='Monokai':
        dark_title_bar(main_application,2)
    else:
        dark_title_bar(main_application,0)

count = 0
for i in color_dict:
    color_theme.add_radiobutton(label=i, image=color_icons[count], variable=theme_choice, compound=tk.LEFT, command= change_theme)
    count+=1 

#### Voice & Speed changer ####
def speak(audio):
    global voice_choice, speed_change
    chosen_voice = voice_choice.get()
    chosen_speed = speed_change.get()
    voice = list(voice_dict.values()).index(chosen_voice)
    speed = speed_dict.get(chosen_speed)
    engine.setProperty('voice', voices[voice].id)
    engine.setProperty('rate',speed)
    engine.say(audio)
    engine.runAndWait()


voice_change.add_separator()
for i in voice_dict.values():
    voice_change.add_radiobutton(label=i, variable=voice_choice, compound=tk.LEFT)

for i in speed_dict:
    speed.add_radiobutton(label=i, variable=speed_change, compound=tk.LEFT)
    

############# about commands ######

about_icon = tk.PhotoImage(file='Main/icons2/icon.png')


def help():
    try:
        webbrowser.open(url='https://www.linkedin.com/in/akbar-k-09b28618b/')
    except Exception as e:
        pass

about.add_command(label='View Help', compound=tk.LEFT, command=help)


def about_menu():
    about_dialogue = tk.Toplevel(background='#e0e0e0')
    about_dialogue.geometry('450x250+500+200')
    about_dialogue.title('About Vpad')
    about_dialogue.resizable(0,0)
    about_dialogue.wm_iconbitmap('Main/icons2/icon.ico')

    dark_title_bar(about_dialogue,2)
    copyright = u"\u00A9"

    ##frame 
    find_frame = ttk.Frame(about_dialogue, relief=tk.FLAT)
    find_frame.pack(pady=35)

    about_image = tk.Label(find_frame, image=about_icon)
    about_label = tk.Label(find_frame, text='Vpad Text Editor 2.0')
    about_label2 = tk.Label(find_frame, text=f'{copyright} 2023. All right reserved by Mr. Akbar Kaleem.')


    about_image.grid(row=0,column=0,padx=4, pady=4)
    about_label.grid(row=1,column=0, padx=4, pady=4)
    about_label2.grid(row=2,column=0, padx=4, pady=6)

    ## button
    def ok_close():
        about_dialogue.destroy()

    dev_btn = ttk.Button(find_frame, text='Developer Info', command=help)
    dev_btn.grid(row=3,column=0, padx=8, pady=2)

    ok_btn = ttk.Button(find_frame, text='OK', command=ok_close)
    ok_btn.grid(row=4,column=0, padx=2, pady=4)

    about_dialogue.mainloop()

about.add_separator()
about.add_command(label='About Vpad', compound=tk.LEFT, command=about_menu)

############ POPUP MENU #################

small_bold_icon = tk.PhotoImage(file='Main/icons2/bold1.png')
small_italic_icon = tk.PhotoImage(file='Main/icons2/italic1.png')
small_underline_icon = tk.PhotoImage(file='Main/icons2/underline1.png')
small_copy_icon = tk.PhotoImage(file='Main/icons2/copy1.png')
small_paste_icon = tk.PhotoImage(file='Main/icons2/paste1.png')
small_cut_icon = tk.PhotoImage(file='Main/icons2/cut1.png')
small_select_all_icon = tk.PhotoImage(file='Main/icons2/clear_all1.png')
small_undo_icon = tk.PhotoImage(file='Main/icons2/undo1.png')
small_gpt_icon = tk.PhotoImage(file='Main/icons2/gpt1.png')

my_menu = tk.Menu(text_editor, tearoff=False)

### popup variables #######
bold_var = "normal"
italic_var = "roman"
underline_var = False

def bold(event=None):
    global bold_var
    bold_var = "bold"
    try:
        bold = font.Font(text_editor,text_editor.cget("font"))
        bold.config(family=current_font_family ,size=current_font_size ,weight=bold_var, slant=italic_var, underline=underline_var)

        text_editor.tag_configure("bold",font=bold)

        current_tags = text_editor.tag_names("sel.first")

        if "bold" in current_tags:
            text_editor.tag_remove("bold", "sel.first", "sel.last")
            bold_var = "normal"
        else:
            text_editor.tag_add("bold", "sel.first", "sel.last")
            bold_var = "bold"

    except Exception as e:
        pass

def italic(event=None):
    global italic_var
    italic_var = "italic"
    try:
        italic = font.Font(text_editor,text_editor.cget("font"))
        italic.config(family=current_font_family, size=current_font_size, slant=italic_var, weight=bold_var, underline=underline_var)

        text_editor.tag_configure("italic",font=italic)

        current_tags =text_editor.tag_names("sel.first")

        if "italic" in current_tags:
            text_editor.tag_remove("italic", "sel.first", "sel.last")
            italic_var = "roman"
        else:
            text_editor.tag_add("italic", "sel.first", "sel.last")
            italic_var = "italic"
    
    except Exception as e:
        pass

def underline(event=None):
    global underline_var
    underline_var = True
    try:
        underline = font.Font(text_editor,text_editor.cget("font"))
        underline.config(family=current_font_family,size=current_font_size,underline=underline_var, weight=bold_var, slant=italic_var )

        text_editor.tag_configure(True,font=underline)

        current_tags = text_editor.tag_names("sel.first")

        if '1' in current_tags:
            text_editor.tag_remove('1', "sel.first", "sel.last")
            underline_var = False
        else:
            text_editor.tag_add('1', "sel.first", "sel.last")
            underline_var = True

    except Exception as e:
        pass

def my_popup(e):
    my_menu.tk_popup(e.x_root, e.y_root)

my_menu.add_command(label='Bold' ,image=small_bold_icon,compound=tk.LEFT, command=bold)
my_menu.add_command(label='Italic', image=small_italic_icon,compound=tk.LEFT, command=italic)
my_menu.add_command(label='Underline', image=small_underline_icon,compound=tk.LEFT, command=underline)
my_menu.add_separator()
my_menu.add_command(label='Undo', image=small_undo_icon,compound=tk.LEFT, command=undo)
my_menu.add_separator()
my_menu.add_command(label='Copy', image=small_copy_icon,compound=tk.LEFT, command=lambda:text_editor.event_generate("<<Copy>>"))
my_menu.add_command(label='Paste', image=small_paste_icon,compound=tk.LEFT, command=lambda:text_editor.event_generate("<<Paste>>"))
my_menu.add_command(label='Cut', image=small_cut_icon,compound=tk.LEFT, command=lambda:text_editor.event_generate("<<Cut>>"))
my_menu.add_separator()
my_menu.add_command(label='Select All', image=small_select_all_icon,compound=tk.LEFT, command=lambda:text_editor.event_generate("<<SelectAll>>"))
my_menu.add_command(label='Clear All', image=small_select_all_icon,compound=tk.LEFT, 
command= lambda:text_editor.delete(1.0, tk.END))
my_menu.add_separator()
my_menu.add_command(label='Ask GPT', image=small_gpt_icon, compound=tk.LEFT, 
command= lambda:ChatGPT())

text_editor.bind("<Button-3>", my_popup)

############## End PopUp Menu ###############


########################### Extra Function #######################

def dark_title_bar(window,n):
    try:
        window.update()
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
        get_parent = ct.windll.user32.GetParent
        hwnd = get_parent(window.winfo_id())
        rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
        value = n
        value = ct.c_int(value)
        set_window_attribute(hwnd, rendering_policy, ct.byref(value),
                            ct.sizeof(value))
    except Exception as e:
        pass

# ------------------------ END MAIN MENU FUNCTIONALITY --------------------------------- #

main_application.config(menu=main_menu)

### bind shortcut keys
main_application.bind("<Control-n>", new_file)
main_application.bind("<Control-o>", open_file)
main_application.bind("<Control-s>", save_file)
main_application.bind("<Control-Alt-s>", save_as_file)
main_application.bind("<Control-q>", exit_file)
main_application.bind("<Control-f>", find_func)
main_application.bind("<Control-g>", ChatGPT)

def close():
    words = len(text_editor.get(1.0, 'end-1c').split())
    characters = len(text_editor.get(1.0, 'end-1c').replace(' ', ''))

    if characters==0 or words==0:
        main_application.destroy()
    else:
        exit_file()
    
main_application.protocol("WM_DELETE_WINDOW",close)
main_application.mainloop()