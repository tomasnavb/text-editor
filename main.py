from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter import font, colorchooser, filedialog
import os

# ######################################
#          GLOBAL VARIABLES            #
# ######################################


url = ''
filetypes = (('Text Files', '*txt'), ('All files', '*.*'))
font_size = 12
font_style = 'arial'


# ######################################
#          FUNCTIONALITIES             #
# ######################################

def find():
    def find_word():
        textarea.tag_remove('match', 1.0, END)
        start_position = '1.0'
        word = find_entry.get()
        if word:
            while True:
                start_position = textarea.search(word, start_position, stopindex=END)
                if start_position == "":
                    break
                end_position = f'{start_position} + {len(word)}c'
                textarea.tag_add('match', start_position, end_position)
                textarea.tag_config('match', foreground='red', background='yellow')
                start_position = end_position

    def replace():
        word = find_entry.get()
        new_word = replace_entry.get()
        if new_word:
            content = textarea.get(1.0, END)
            new_content = content.replace(word, new_word)
            textarea.delete(1.0, END)
            textarea.insert(1.0, new_content)

    find_window = Toplevel()
    find_window.title("Search")
    find_window.geometry("450x200+800+200")
    find_window.resizable(False, False)
    frame = LabelFrame(find_window, text='Find/Replace')
    frame.pack(pady=20)
    find_label = Label(frame, text='Find')
    find_label.grid(row=0, column=0, padx=5, pady=5)
    find_entry = Entry(frame)
    find_entry.grid(row=0, column=1, padx=10, pady=10)
    replace_label = Label(frame, text='Replace')
    replace_label.grid(row=1, column=0, padx=5, pady=5)
    replace_entry = Entry(frame)
    replace_entry.grid(row=1, column=1, padx=10, pady=10)
    find_button = Button(frame, text='FIND', command=find_word)
    find_button.grid(row=2, column=0, padx=5, pady=5)
    replace_button = Button(frame, text='REPLACE', command=replace)
    replace_button.grid(row=2, column=1, padx=5, pady=5)

    def close_window():
        textarea.tag_remove('match', 1.0, END)
        find_window.destroy()

    find_window.protocol('WM_DELETE_WINDOW', close_window)
    find_window.mainloop()


def status_bar(event):
    chars = 0
    if textarea.edit_modified():
        content = textarea.get(0.0, END).split()
        words = len(content)
        for word in content:
            chars += len(word)
        statusbar.config(text=f'Characters: {chars} - Words: {words}')
    textarea.edit_modified(False)


def new_file():
    global url
    if textarea.edit_modified():
        save = askyesnocancel(title='You didn\'t save your changes', message='Want to save your changes first?')
        if not save:
            textarea.delete(0.0, END)
            url = ''
            root.title("Text Editor")
        elif save:
            save_file_as()


def open_file():
    global url
    url = filedialog.askopenfilename(title='Open Files', initialdir=os.getcwd(), filetypes=filetypes)
    if url != '':
        data = open(url, 'r')
        textarea.insert(0.0, data.read())
        root.title(os.path.basename(url))


def save_file():
    if url == '':
        save_url = filedialog.asksaveasfile(mode='w', title='Save As', defaultextension='.txt', initialdir=os.getcwd(),
                                            filetypes=filetypes)
        content = textarea.get(0.0, END)
        if save_url is not None:
            save_url.write(content)
            save_url.close()
            root.title(os.path.basename(save_url.name))
    else:
        content = textarea.get(0.0, END)
        file = open(url, 'w')
        file.write(content)


def save_file_as():
    save_url = filedialog.asksaveasfile(mode='w', title='Save As', defaultextension='.txt',
                                        initialdir=os.path.abspath(url),
                                        filetypes=filetypes, initialfile=os.path.basename(url))
    content = textarea.get(0.0, END)
    if save_url is not None:
        save_url.write(content)
        save_url.close()


def exit():
    global url
    if textarea.edit_modified():
        save = askyesnocancel(title='Warning', message='Do you want to save the file?')
        if not save and save is not None:
            root.destroy()
        elif save:
            if url is None:
                save_file_as()
                root.destroy()
            else:
                save_file()
                root.destroy()
    else:
        root.destroy()


def set_font_style(event):
    global font_style
    font_style = font_family_variable.get()
    textarea.config(font=(font_style, font_size))


def set_font_size(event):
    global font_size
    font_size = size_variable.get()
    textarea.config(font=(font_style, font_size))


def set_text_bold():
    text_property = font.Font(font=textarea['font']).actual()
    if text_property['weight'] == 'normal':
        textarea.config(font=(font_style, font_size, 'bold'))
    if text_property['weight'] == 'bold':
        textarea.config(font=(font_style, font_size, 'normal'))


def set_text_italic():
    text_property = font.Font(font=textarea['font']).actual()
    if text_property['slant'] == 'roman':
        textarea.config(font=(font_style, font_size, 'italic'))
    if text_property['slant'] == 'italic':
        textarea.config(font=(font_style, font_size, 'roman'))


def set_text_underline():
    text_property = font.Font(font=textarea['font']).actual()
    if text_property['underline'] == 0:
        textarea.config(font=(font_style, font_size, 'underline'))
    if text_property['underline'] == 1:
        textarea.config(font=(font_style, font_size, 'normal'))


def select_color():
    color = colorchooser.askcolor()
    textarea.config(fg=color[1])


def right_align():
    data = textarea.get(0.0, END)
    textarea.tag_config('right', justify=RIGHT)
    textarea.delete(0.0, END)
    textarea.insert(INSERT, data, 'right')


def left_align():
    data = textarea.get(0.0, END)
    textarea.tag_config('left', justify=LEFT)
    textarea.delete(0.0, END)
    textarea.insert(INSERT, data, 'left')


def center_align():
    data = textarea.get(0.0, END)
    textarea.tag_config('center', justify=CENTER)
    textarea.delete(0.0, END)
    textarea.insert(INSERT, data, 'center')


def show_hide_toolbar():
    if not show_toolbar.get():
        toolbar.pack_forget()
    else:
        textarea.pack_forget()
        toolbar.pack(fill=X)
        textarea.pack(fill=BOTH, expand=True)


def show_hide_statusbar():
    if not show_statusbar.get():
        statusbar.pack_forget()
    else:
        statusbar.pack()


def change_theme_color(primary_color, secondary_color, text_color):
    toolbar.config(background=primary_color)
    textarea.config(background=secondary_color, foreground=text_color, selectbackground=primary_color)


# ######################################
#          MAIN WINDOW                 #
# ######################################


root = Tk()
root.title("Text Editor")
root.geometry("800x600+10+10")  # Tamanio de la ventana. Ultimos dos valores ubicacion en X e Y
root.minsize(650, 300)
root.resizable(True, True)
icon = PhotoImage(file='icons/icon.png')
root.iconphoto(False, icon)

# ######################################
#              MENU BAR                #
# ######################################
menubar = Menu(root)
root.config(menu=menubar)
filemenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label="File", menu=filemenu, )
# Importing buttons images
newImg = PhotoImage(file="icons/new.png")
openImg = PhotoImage(file="icons/open.png")
saveImg = PhotoImage(file="icons/save.png")
saveAsImg = PhotoImage(file="icons/save_as.png")
exitImg = PhotoImage(file="icons/exit.png")

# ######################################
#              FILEMENU                #
# ######################################


filemenu.add_command(label="New", accelerator="Ctrl+N", image=newImg, compound=LEFT, command=new_file)
filemenu.add_command(label="Open", accelerator="Ctrl+O", image=openImg, compound=LEFT, command=open_file)
filemenu.add_command(label="Save", accelerator="Ctrl+S", image=saveImg, compound=LEFT, command=save_file)
filemenu.add_command(label="Save As", accelerator="Ctrl+Alt+S", image=saveAsImg, compound=LEFT, command=save_file_as)
filemenu.add_separator()
filemenu.add_command(label="Exit", accelerator="Ctrl+Q", image=exitImg, compound=LEFT, command=exit)

# ######################################
#              EDIT MENU               #
# ######################################


editmenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label="Edit", menu=editmenu)
# Importing buttons images
cutImg = PhotoImage(file="icons/cut.png")
copyImg = PhotoImage(file="icons/copy.png")
pasteImg = PhotoImage(file="icons/paste.png")
clearImg = PhotoImage(file="icons/clear_all.png")
findImg = PhotoImage(file="icons/find.png")
# Creating menu buttons
editmenu.add_command(label="Cut", accelerator="Ctrl+X", image=cutImg, compound=LEFT,
                     command=lambda: textarea.event_generate('<Control x>'))
editmenu.add_command(label="Copy", accelerator="Ctrl+C", image=copyImg, compound=LEFT,
                     command=lambda: textarea.event_generate('<Control c>'))
editmenu.add_command(label="Paste", accelerator="Ctrl+B", image=pasteImg, compound=LEFT,
                     command=lambda: textarea.event_generate('<Control v>'))
editmenu.add_command(label="Clear", accelerator="Ctrl+Alt+X", image=clearImg, compound=LEFT,
                     command=lambda: textarea.delete(0.0, END))
editmenu.add_command(label="Find", accelerator="Ctrl+F", image=findImg, compound=LEFT, command=find)

# ######################################
#              VIEW MENU               #
# ######################################


viewmenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label="View", menu=viewmenu)
show_toolbar = BooleanVar()
show_statusbar = BooleanVar()
# Importing buttons images
toolImg = PhotoImage(file="icons/tool_bar.png")
statusImg = PhotoImage(file="icons/status_bar.png")
# Creating menu buttons
viewmenu.add_checkbutton(label='Tool bar', variable=show_toolbar, onvalue=True, offvalue=False, image=toolImg,
                         compound=LEFT, command=show_hide_toolbar)
viewmenu.add_checkbutton(label='Status bar', variable=show_statusbar, onvalue=True, offvalue=False, image=statusImg,
                         compound=LEFT, command=show_hide_statusbar)
show_toolbar.set(True)
show_statusbar.set(True)

# ######################################
#              THEMES MENU             #
# ######################################


themesmenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label="Themes", menu=themesmenu)
theme_choice = StringVar()
# Importing buttons images
lightImg = PhotoImage(file="icons/light_default.png")
lighplusImg = PhotoImage(file="icons/light_plus.png")
darkImg = PhotoImage(file="icons/dark.png")
pinkImg = PhotoImage(file="icons/red.png")
monokaiImg = PhotoImage(file="icons/monokai.png")
# Creating menu buttons
themesmenu.add_radiobutton(label="Light default", variable=theme_choice, image=lightImg, compound=LEFT)
themesmenu.add_radiobutton(label="Light Plus", variable=theme_choice, image=lighplusImg, compound=LEFT,
                           command=lambda: change_theme_color('#48C9B0', '#EBF5FB', '#17202A'))
themesmenu.add_radiobutton(label="Dark", variable=theme_choice, image=darkImg, compound=LEFT)
themesmenu.add_radiobutton(label="Pink", variable=theme_choice, image=pinkImg, compound=LEFT)
themesmenu.add_radiobutton(label="Monokai", variable=theme_choice, image=monokaiImg, compound=LEFT)

# ######################################
#              TOOLBAR                 #
# ######################################


toolbar = Label(root)
toolbar.pack(side=TOP, fill=X)

# ######################################
#              FONT-FAMILY             #
# ######################################


font_families = font.families()
font_family_variable = StringVar()
fontfamily_combobox = Combobox(toolbar, width=30, values=font_families, state='readonly',
                               textvariable=font_family_variable)
fontfamily_combobox.grid(row=0, column=0, padx=5)
fontfamily_combobox.current(font_families.index('Arial'))

# ComboboxSelected Event
fontfamily_combobox.bind('<<ComboboxSelected>>', set_font_style)

# ######################################
#              FONT-SIZE               #
# ######################################


size_variable = IntVar()
font_size_combobox = Combobox(toolbar, width=15, textvariable=size_variable, state='readonly',
                              values=tuple(range(8, 73, 4)))
font_size_combobox.current(1)
font_size_combobox.grid(row=0, column=1, padx=5)

# ComboboxSelected Event
font_size_combobox.bind('<<ComboboxSelected>>', set_font_size)

# ######################################
#              BUTTONS                 #
# ######################################


bold_img = PhotoImage(file='icons/bold.png')
bold_button = Button(toolbar, image=bold_img, command=set_text_bold)
bold_button.grid(row=0, column=2, padx=5)

italic_img = PhotoImage(file='icons/italic.png')
italic_button = Button(toolbar, image=italic_img, command=set_text_italic)
italic_button.grid(row=0, column=3, padx=5)

underline_img = PhotoImage(file='icons/underline.png')
underline_button = Button(toolbar, image=underline_img, command=set_text_underline)
underline_button.grid(row=0, column=4, padx=5)

fontcolor_img = PhotoImage(file='icons/font_color.png')
fontcolor_button = Button(toolbar, image=fontcolor_img, command=select_color)
fontcolor_button.grid(row=0, column=5, padx=5)

leftalign_img = PhotoImage(file='icons/left.png')
leftalign_button = Button(toolbar, image=leftalign_img, command=left_align)
leftalign_button.grid(row=0, column=6, padx=5)

centeralign_img = PhotoImage(file='icons/center.png')
centeralign_button = Button(toolbar, image=centeralign_img, command=center_align)
centeralign_button.grid(row=0, column=7, padx=5)

rightalign_img = PhotoImage(file='icons/right.png')
rightalign_button = Button(toolbar, image=rightalign_img, command=right_align)
rightalign_button.grid(row=0, column=8, padx=5)

# ######################################
#              TEXT-AREA               #
# ######################################


scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
textarea = Text(root, yscrollcommand=scrollbar.set, font=('arial', 12), undo=True)
textarea.pack(fill=BOTH, expand=True)
textarea.bind('<<Modified>>', status_bar)
scrollbar.config(command=textarea.yview)

# ######################################
#              STATUS-BAR             #
# ######################################


statusbar = Label(root, text='Status Bar')
statusbar.pack(side=BOTTOM)

# End
root.mainloop()
