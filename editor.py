from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
from tkinter import ttk
import time

#----------------------------------------
# Window config
#----------------------------------------
root = Tk()
root.title('Editor')
root.iconbitmap('/Users/niklaslarsson/Pictures/Icons/icon.icns')

# Designate height and width of the app
app_width = 400
app_height = 400

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)

root.geometry(
		f'{app_width}x{app_height}+{int(x)}+{int(y)}'
		)

root.resizable(False, False)

# Set variable for open file name
global open_status_name
open_status_name = False

# Set variable for highlighted text
global selected
selected = False

#----------------------------------------
# Functions
#----------------------------------------

# Create new file function
def new_file():
	# Delete previous text
	my_text.delete('1.0', END)
	# Update status bars
	status_bar.config(text='  New file')
	root.title('Editor')
	global open_status_name
	open_status_name = False

# Create open files function
def open_file():
	# Delete previous text
	my_text.delete('1.0', END)

	# Grab filename
	text_file = filedialog.askopenfilename(
			initialdir='/users/niklaslarsson/Documents/',
			defaultextension='*.*',
			title='Open File',
			filetypes=(

				(
					'Text Files',
					'*.txt'
					
					),
				
				(
					'HTML Files',
					'*.html'
					
					),
				
				(
					'Python Files',
					'*.py'
					
					),
				
				(
					'All Files',
					'*.*'
					
					),
				
				)
			)

	# Check to see if there is a file name
	if text_file:
		# Make filename global so we can access it later
		global open_status_name
		open_status_name = text_file

		# Open the file
		text_file = open(text_file, 'r')
		stuff = text_file.read()

		# Add file to textbox
		my_text.insert(END, stuff)

		# Close the opened file
		text_file.close()

		# Update status bars
		status_bar.config(text='  Ready')
		root.title('Editor')

# Save file as function
def save_as_file():
	text_file = filedialog.asksaveasfilename(
			defaultextension='.txt',
			title='Save File',
			filetypes=(

				(

					'Text Files',
					'*.txt'

					),

				(

					'HTML Files',
					'*.html'

					),

				(

					'Python Files',
					'*.py'

					),

				(

					'All Files',
					'*.*'

					)
				)

			)

	if text_file:
		global open_status_name
		open_status_name = text_file
		# Save the file
		text_file = open(text_file, 'w')
		text_file.write(my_text.get(1.0, END))

		# Close the file
		text_file.close()

		# Update status bars
		status_bar.config(text='  New file saved')
		root.title('Editor')

# Save file
def save_file():
	global open_status_name
	if open_status_name:
		# Save the file
		text_file = open(open_status_name, 'w')
		text_file.write(my_text.get(1.0, END))
		# Close the file
		text_file.close()
		status_bar.config(text='  Saved')
	else:
		save_as_file()
		
# Cut text
def cut_text(e):
	global selected
	# Check to see if we used keyboard shortcuts
	if e:
		selected = root.clipboard_get()
	else:
		if my_text.selection_get():
			# Grab selected text from textbox
			selected = my_text.selection_get()
			# Delete selected text from textbox
			my_text.delete('sel.first', 'sel.last')
			# Clear the clipboard then append
			root.clipboard_clear()
			root.clipboard_append(selected)

# Copy text
def copy_text(e):
	global selected
	# Check to see if we used keyboard shortcuts
	if e:
		selected = root.clipboard_get()

	if my_text.selection_get():
		# Grab selected text from textbox
		selected = my_text.selection_get()
		# Clear the clipboard then append
		root.clipboard_clear()
		root.clipboard_append(selected)

# Paste text
def paste_text(e):
	global selected
	# Check to see if we used keyboard shortcuts
	if e:
		selected = root.clipboard_get()
	else:
		if selected:
			position = my_text.index(INSERT)
			my_text.insert(position, selected)

# Bold text function
def bold_it():
	# Create our font
	bold_font = font.Font(
		my_text,
		my_text.cget('font'),
		)
	bold_font.configure(
		weight='bold',
	)

	# Configure a tag
	my_text.tag_configure(
		'bold',
		font=bold_font,
		)

	# Define current tags
	current_tags = my_text.tag_names(
		'sel.first',
	)

	# If statement to see if tag has been set
	if 'bold' in current_tags:
		my_text.tag_remove(
			'bold',
			'sel.first',
			'sel.last',
			)
	else:
		my_text.tag_add(
			'bold',
			'sel.first',
			'sel.last',
			)

# Italics text function
def italics_it():
	# Create our font
	italics_font = font.Font(
		my_text,
		my_text.cget('font'),
		)
	italics_font.configure(
		slant='italic',
	)

	# Configure a tag
	my_text.tag_configure(
		'italic',
		font=italics_font,
		)

	# Define current tags
	current_tags = my_text.tag_names(
		'sel.first',
	)

	# If statement to see if tag has been set
	if 'italic' in current_tags:
		my_text.tag_remove(
			'italic',
			'sel.first',
			'sel.last',
			)
	else:
		my_text.tag_add(
			'italic',
			'sel.first',
			'sel.last',
			)

# Change selected text color
def text_color():

	# Pick a color
	my_color = colorchooser.askcolor()[1]
	if my_color:
		#status_bar.config(text=my_color)

		# Create our font
		color_font = font.Font(
			my_text,
			my_text.cget('font'),
			)

		# Configure a tag
		my_text.tag_configure(
			'colored',
			font=color_font,
			foreground=my_color,
			)

		# Define current tags
		current_tags = my_text.tag_names(
			'sel.first',
		)

		# If statement to see if tag has been set
		if 'colored' in current_tags:
			my_text.tag_remove(
				'colored',
				'sel.first',
				'sel.last',
				)
		else:
			my_text.tag_add(
				'colored',
				'sel.first',
				'sel.last',
				)

# Select All Text
def select_all(e):
	# Add sel tag to select all text
	my_text.tag_add('sel', '1.0', 'end')

# Clear All Text
def clear_all():
	my_text.delete(1.0, END)

# Night Mode
def night_mode():
	main_color = 'gray25'
	second_color = 'dim gray'
	text_color = 'SpringGreen2'
	root.config(
			bg=main_color,
			)
	status_bar.config(
			bg=main_color,
			fg=text_color,
			)
	my_text.config(
			bg=second_color,
			fg=text_color,
			selectbackground='yellow',
			selectforeground='SpringGreen2',
			)

	# File Menu Colors
	file_menu.config(
			bg=main_color,
			fg=text_color,
			)
	edit_menu.config(
			bg=main_color,
			fg=text_color,
			)
	color_menu.config(
			bg=main_color,
			fg=text_color,
			)
	options_menu.config(
			bg=main_color,
			fg=text_color,
			)
	font_menu.config(
			bg=main_color,
			fg=text_color,
			)

# Day Mode
def day_mode():
	main_color = 'dark orange'
	second_color = 'sandy brown'
	text_color = 'white'
	root.config(
			bg=main_color,
			)
	status_bar.config(
			bg=main_color,
			fg=text_color,
			)
	my_text.config(
			bg=second_color,
			fg=text_color,
			selectbackground='yellow',
			selectforeground='gray1',
			)

	# File Menu Colors
	file_menu.config(
			bg=main_color,
			fg=text_color,
			)
	edit_menu.config(
			bg=main_color,
			fg=text_color,
			)
	color_menu.config(
			bg=main_color,
			fg=text_color,
			)
	options_menu.config(
			bg=main_color,
			fg=text_color,
			)
	font_menu.config(
			bg=main_color,
			fg=text_color,
			)
	

# Retro Font 1
def font_1():
	my_text.config(
			font=('Press Start 2P', 16),
			)
# Retro Font 2
def font_2():
	my_text.config(
			font=('Px437 VTech BIOS', 16),
			)

def scrollbar_toggle():
	pass

def finnish_language():
	pass

def english_language():
	pass

def editor_info():
	# Pop up a window with info about editor
	infow = Tk()
	infow.title('About this editor')
	infow.config(bg='dark orange')

	infotext = False

	label = Label(
			infow,
			text=infotext,
			font=('Press Start 2P', 10)
			)
	label.config(
			bg='dark orange',
			relief='sunken',
			)
	label.pack(
			fill=X,
			ipady=5,
			ipadx=5,
			pady=10,
			padx=10,
			)

	# Designate height and width of the infow
	infow_width = 300
	infow_height = 150

	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()

	x = (screen_width / 2) - (app_width / 2)
	y = (screen_height / 2) - (app_height / 2)

	infow.geometry(
			f'{infow_width}x{infow_height}+{int(x)}+{int(y)}'
			)

	infow.resizable(False, False)

def text_align():
	pass	

def bind_save(event):
	if event:
		save_file()
	else:
		save_file()

def bind_save_as(event):
	if event:
		save_as_file()
	else:
		save_as_file()

def bind_new_file(event):
	if event:
		new_file()
	else:
		new_file()

def bind_open_file(event):
	if event:
		open_file()
	else:
		open_file()

#------------------------------------------------
# Frames
#------------------------------------------------

# Create a toolbar frame
toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X)

# Create mainframe
my_frame = Frame(root)
my_frame.pack(pady=5)

#------------------------------------------------
# Scrollbar
#------------------------------------------------

# Create scrollbar for the textbox
text_scroll = Scrollbar(my_frame)
#text_scroll.pack(side=RIGHT, fill=Y)

#------------------------------------------------
# Text Box
#------------------------------------------------

# Create textbox
my_text = Text(
		my_frame,
		bd=-1,
		width=21,
		height=19,
		font=('Press Start 2P', 16),
		selectbackground='yellow',
		selectforeground='black',
		undo=True,
		yscrollcommand=text_scroll.set,
		padx=4,
		pady=4,
		tabs=40,
		spacing1=2,
		spacing2=2,
		wrap=WORD,
		)

my_text.pack()
#--------------------------------------------
# Scrollbar Configuration
#--------------------------------------------

text_scroll.config(
	command=my_text.yview,
	bg='grey30'
	)

#--------------------------------------------
# Menus
#--------------------------------------------

# Create menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Create file menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(
		label='File',
		menu=file_menu
		)
file_menu.add_command(
		label='New',
		command=new_file,
		accelerator='Command-N',
		)
file_menu.add_command(
		label='Open',
		command=open_file,
		accelerator='Command-O',
		)
file_menu.add_command(
		label='Save',
		command=save_file,
		accelerator='Command-S',
		)
file_menu.add_command(
		label='Save As',
		command=save_as_file,
		accelerator='Command-Shift-S',
		)
file_menu.add_separator()
file_menu.add_command(
		label='Exit',
		command=root.quit,
		accelerator='Command-Q',
		)

# Create edit menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(
	label='Edit',
	menu=edit_menu
	)
edit_menu.add_command(
	label='Cut',
	command=lambda:
	cut_text(False),
	accelerator='Command-X',
	)
edit_menu.add_command(
	label='Copy',
	command=lambda:
	copy_text(False),
	accelerator='Command-C',
	)
edit_menu.add_command(
	label='Paste',
	command=lambda:
	paste_text(False),
	accelerator='Command-V',
	)
edit_menu.add_command(
	label='Undo',
	command=my_text.edit_undo,
	accelerator='Command-Z',
	)
edit_menu.add_command(
	label='Redo',
	command=my_text.edit_redo,
	accelerator='Command-Y',
	)
edit_menu.add_separator()
edit_menu.add_command(
		label='Select All',
		command=lambda:
		select_all(True),
		accelerator='Command-A',
		)
edit_menu.add_command(
		label='Clear',
		command=clear_all,
		)
edit_menu.add_separator()
edit_menu.add_command(
	label='Bold',
	command=bold_it,
	accelerator='',
)
edit_menu.add_command(
	label='Italics',
	command=italics_it,
	accelerator='',
)

# Create color menu
color_menu = Menu(
		my_menu,
		tearoff=False,
		)
my_menu.add_cascade(
		label='Colors',
		menu=color_menu,
		)
color_menu.add_command(
		label='Selected Text',
		command=text_color,
		)
color_menu.add_command(
		label='All Text',
		command=text_color,
		)
color_menu.add_command(
		label='Background',
		#command=bg_color,
		)

# Create Text Menu
text_menu = Menu(
		my_menu,
		tearoff=False,
		)
my_menu.add_cascade(
		label='Text',
		menu=text_menu,
		)

# Text Alignment inside Text Menu
align_menu = Menu(
		text_menu,
		tearoff=False
		)
text_menu.add_cascade(
		label='Alignment',
		menu=align_menu,
		)
align_menu.add_command(
		label='Left',
		command=text_align,
		)
align_menu.add_command(
		label='Center',
		command=text_align,
		)
align_menu.add_command(
		label='Right',
		command=text_align,
		)

# Create Options Menu
options_menu = Menu(
		my_menu,
		tearoff=False,
		)
my_menu.add_cascade(
		label='Options',
		menu=options_menu,
		)
options_menu.add_command(
		label='Night Mode',
		command=night_mode,
		)
options_menu.add_command(
		label='Day Mode',
		command=day_mode,
		)
options_menu.add_separator()

# Language menu inside options menu
language_menu = Menu(
		options_menu,
		tearoff=False
		)
options_menu.add_cascade(
		label='Language',
		menu=language_menu,
		)
language_menu.add_command(
		label='Suomi',
		command=finnish_language,
		)
language_menu.add_command(
		label='English',
		command=english_language,
		)

# Create Font Menu
font_menu = Menu(
		my_menu,
		tearoff=False,
		)
my_menu.add_cascade(
		label='Font',
		menu=font_menu,
		)
font_menu.add_command(
		label='Retro 1',
		command=font_1,
		)
font_menu.add_command(
		label='Retro 2',
		command=font_2,
		)

# Create Help Menu
help_menu = Menu(
		my_menu,
		tearoff=False,
		)
my_menu.add_cascade(
		label='Help',
		menu=help_menu,
		)
help_menu.add_command(
		label='About This Editor',
		command=editor_info,
		)

#-----------------------------------
# Status Bar
#-----------------------------------
# Create statusbar to the bottom of the app
status_bar = Label(
		root,
		text='  Ready',
		anchor=W,
		font=('Press Start 2P', 12)
		)
status_bar.config(
	bg='grey30'	
)
status_bar.pack(fill=X, side=BOTTOM, ipady=5)

# Default colorscheme

# Window color
main_color = 'dark orange'

# Textbox color
textbox_color = 'sandy brown'

# Text color
text_color = 'white'
root.config(
		bg=main_color,
		)
status_bar.config(
		bg=main_color,
		fg=text_color,
		)
my_text.config(
		bg=textbox_color,
		fg=text_color,
		selectbackground='yellow',
		selectforeground='gray1',
		)

# File Menu Colors
file_menu.config(
		bg=main_color,
		fg=text_color,
		)
edit_menu.config(
		bg=main_color,
		fg=text_color,
		)
color_menu.config(
		bg=main_color,
		fg=text_color,
		)
options_menu.config(
		bg=main_color,
		fg=text_color,
		)
font_menu.config(
		bg=main_color,
		fg=text_color,
		)

# Edit bindings
root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)
root.bind('<Command-s>', bind_save)
root.bind('<Command-S>', bind_save_as)
root.bind('<Command-o>', bind_open_file)
root.bind('<Command-n>', bind_new_file)

# Select Binding
root.bind('<Command-A>', select_all)
root.bind('<Command-a>', select_all)

my_text.focus()
root.mainloop()
