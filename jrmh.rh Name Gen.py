global current_page
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
from matplotlib import colors as mcolors
import configparser
import os
import sys
import requests
import subprocess
import tempfile
import platform
__version__ = '1.0.3'
GITHUB_REPO_OWNER = 'iamjrmh'
GITHUB_REPO_NAME = 'CloneHeroColorGen'
GITHUB_RELEASE_API = f'''https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/releases/latest'''
UPDATE_ZIP_FILENAME = 'CloneHeroColorGen.zip'
def hex_to_rgb(hex_color: str) -> tuple:
  if hex_color.startswith('#'):
    hex_color = f'''#{hex_color}'''

  return mcolors.to_rgb(hex_color)

def rgb_to_hex(rgb: tuple) -> str:
  return mcolors.to_hex(rgb).upper()

def interpolate_colors_custom(hex_colors: list[str],steps: int) -> list[str]:
  rgb_colors = [hex_to_rgb(c) for c in hex_colors if c]
  if len(rgb_colors) < 2:
    raise ValueError('At least a start and end color are required.')

  segments = len(rgb_colors)-1
  steps_per_segment = steps//segments
  extra = steps%segments
  result = []
  for i in range(segments):
    start = rgb_colors[i]
    end = rgb_colors[i+1]
    current_steps = steps_per_segment+1 if i < extra else 0
    for j in range(current_steps):
      t = j/max(current_steps-1,1)
      r = start[0]+end[0]-start[0]*t
      g = start[1]+end[1]-start[1]*t
      b = start[2]+end[2]-start[2]*t
      result.append(rgb_to_hex((r,g,b)))

  return result[:steps]

pass
pass
pass
def generate_clone_hero_name(name: str,colors: list[str],bold: bool = False,italic: bool = False,underline: bool = False,strike: bool = False,size: int = None,spacing: int = None) -> tuple[(str,list[str])]:
  gradient = interpolate_colors_custom(colors,len(name))
  segments = [f'''<color={c}>{ch}</color>''' for c,ch in zip(gradient,name)]
  styled = ''.join(segments)
  if bold:
    styled = f'''<b>{styled}</b>'''

  if italic:
    styled = f'''<i>{styled}</i>'''

  if underline:
    styled = f'''<u>{styled}</u>'''

  if strike:
    styled = f'''<s>{styled}</s>'''

  if size:
    styled = f'''<size={size}>{styled}</size>'''

  if spacing:
    styled = f'''<cspace={spacing}>{styled}</cspace>'''

  return (styled,gradient)

pass
def generate_individual_clone_hero_name(letters_data: list[dict],global_size: int = None,global_spacing: int = None) -> tuple[(str,list[str])]:
  segments = []
  colors = []
  for letter_data in letters_data:
    char = letter_data['char']
    color = letter_data['color']
    bold = letter_data['bold']
    italic = letter_data['italic']
    underline = letter_data['underline']
    strike = letter_data['strike']
    if color.startswith('#'):
      color = f'''#{color}'''

    styled_char = f'''<color={color}>{char}</color>'''
    if bold:
      styled_char = f'''<b>{styled_char}</b>'''

    if italic:
      styled_char = f'''<i>{styled_char}</i>'''

    if underline:
      styled_char = f'''<u>{styled_char}</u>'''

    if strike:
      styled_char = f'''<s>{styled_char}</s>'''

    segments.append(styled_char)
    colors.append(color)

  result = ''.join(segments)
  if global_size:
    result = f'''<size={global_size}>{result}</size>'''

  if global_spacing:
    result = f'''<cspace={global_spacing}>{result}</cspace>'''

  return (result,colors)

def export_to_profiles_ini(name_tagged: str):
  folder = filedialog.askdirectory(title='Choose folder to save profiles.ini')
  if folder:
    return None
  else:
    filepath = os.path.join(folder,'profiles.ini')
    config = configparser.ConfigParser()
    if os.path.exists(filepath):
      config.read(filepath)

    profile_num = 1
    while f'''profile{profile_num}''' in config:
      profile_num += 1

    section = f'''profile{profile_num}'''
    config[section] = {'controller_type':'0','lefty_flip':'0','gamepad_mode':'0','is_bot':'0','show_displayname':'0','drum_dynamics_hidden':'0','square_tom_notes':'0','alt_taps':'0','show_accuracy_display':'0','player_name':name_tagged,'note_speed':'7','tilt_activation':'1','highway_length':'100','highway_name':'default','color_profile_name':'DefaultColors','midi_device_id':'-1','dynamics_threshold':'100'}
    try:
      with open(filepath,'w',encoding='utf-8') as f:
        config.write(f)

    except Exception as e:
      messagebox.showerror('Export Error',f'''Failed to save profiles.ini: {e}''')
      return None

    messagebox.showinfo('Exported',f'''Saved profile to:\n{filepath}\nunder section [{section}]''')
    return None

letter_frames = []
letter_controls = []
def choose_color(color_var):
  color_code = colorchooser.askcolor(title='Choose color')
  if color_code[1]:
    color_var.set(color_code[1].upper())
    return None
  else:
    return None

def on_generate_gradient():
  name = gradient_name_entry.get()
  color_inputs = [gradient_start_var.get(),gradient_color2_var.get(),gradient_color3_var.get(),gradient_color4_var.get(),gradient_end_var.get()]
  color_inputs = [f'''#{c}''' for c in color_inputs if c.strip()]
  if len(color_inputs) < 2:
    messagebox.showerror('Input Error','Please provide at least a start and end color for the gradient.')
    return None
  else:
    bold = gradient_bold_var.get()
    italic = gradient_italic_var.get()
    underline = gradient_underline_var.get()
    strike = gradient_strike_var.get()
    size = gradient_size_var.get()
    spacing = gradient_spacing_var.get()
    try:
      size_val = int(size) if size else None
      spacing_val = int(spacing) if spacing else None
      result,gradient = generate_clone_hero_name(name=name,colors=color_inputs,bold=bold,italic=italic,underline=underline,strike=strike,size=size_val,spacing=spacing_val)
      gradient_output_text.config(state=tk.NORMAL)
      gradient_output_text.delete('1.0',tk.END)
      gradient_output_text.insert(tk.END,result)
      gradient_output_text.config(state=tk.DISABLED)
      gradient_preview_text.config(state=tk.NORMAL)
      gradient_preview_text.delete('1.0',tk.END)
      base_font_size = 16
      if size_val:
        base_font_size = min(max(size_val//2,10),24)

      font_styles = []
      if bold:
        font_styles.append('bold')

      if italic:
        font_styles.append('italic')

      if underline:
        font_styles.append('underline')

      if strike:
        font_styles.append('overstrike')

      font_tuple = ('Arial',base_font_size,' '.join(font_styles) if font_styles else 'normal')
      gradient_preview_text.configure(font=font_tuple)
      for i,ch,color in enumerate(zip(name,gradient)):
        tag_name = f'''grad_char_{i}'''
        gradient_preview_text.insert(tk.END,ch,tag_name)
        gradient_preview_text.tag_config(tag_name,foreground=color)

      gradient_preview_text.config(state=tk.DISABLED)
      return None
    except ValueError as ve:
      messagebox.showerror('Input Error',str(ve))
      return None
    except Exception as e:
      messagebox.showerror('Error',f'''An unexpected error occurred: {e}''')
      return None

def update_individual_letters():
  name = individual_name_entry.get()
  for frame in letter_frames:
    frame.destroy()

  letter_frames.clear()
  letter_controls.clear()
  if name:
    return None
  else:
    for i,char in enumerate(name):
      frame = ttk.Frame(individual_letter_controls_frame)
      frame.pack(fill=tk.X,pady=2)
      letter_frames.append(frame)
      ttk.Label(frame,text=f'''\'{char}\'''',width=5,style='Content.TLabel').pack(side=tk.LEFT,padx=5)
      color_var = tk.StringVar(root,value='#FFFFFF')
      color_entry = ttk.Entry(frame,textvariable=color_var,width=10,style='TEntry')
      color_entry.pack(side=tk.LEFT,padx=5)
      color_button = ttk.Button(frame,text='Pick',command=lambda cv=color_var: choose_color(cv),style='Content.TButton')
      color_button.pack(side=tk.LEFT,padx=2)
      bold_var = tk.BooleanVar(root)
      italic_var = tk.BooleanVar(root)
      underline_var = tk.BooleanVar(root)
      strike_var = tk.BooleanVar(root)
      ttk.Checkbutton(frame,text='B',variable=bold_var,width=3,style='TCheckbutton').pack(side=tk.LEFT,padx=2)
      ttk.Checkbutton(frame,text='I',variable=italic_var,width=3,style='TCheckbutton').pack(side=tk.LEFT,padx=2)
      ttk.Checkbutton(frame,text='U',variable=underline_var,width=3,style='TCheckbutton').pack(side=tk.LEFT,padx=2)
      ttk.Checkbutton(frame,text='S',variable=strike_var,width=3,style='TCheckbutton').pack(side=tk.LEFT,padx=2)
      letter_controls.append({'char':char,'color_var':color_var,'bold_var':bold_var,'italic_var':italic_var,'underline_var':underline_var,'strike_var':strike_var})

    return None

def on_generate_individual():
  if letter_controls:
    messagebox.showerror('Error','Please enter a name first and click \'Update Letters\' to generate letter controls.')
    return None
  else:
    try:
      size = individual_size_var.get()
      spacing = individual_spacing_var.get()
      size_val = int(size) if size else None
      spacing_val = int(spacing) if spacing else None
      letters_data = []
      for control in letter_controls:
        letters_data.append({'char':control['char'],'color':control['color_var'].get(),'bold':control['bold_var'].get(),'italic':control['italic_var'].get(),'underline':control['underline_var'].get(),'strike':control['strike_var'].get()})

      result,colors = generate_individual_clone_hero_name(letters_data,size_val,spacing_val)
      individual_output_text.config(state=tk.NORMAL)
      individual_output_text.delete('1.0',tk.END)
      individual_output_text.insert(tk.END,result)
      individual_output_text.config(state=tk.DISABLED)
      individual_preview_text.config(state=tk.NORMAL)
      individual_preview_text.delete('1.0',tk.END)
      base_font_size = 16
      if size_val:
        base_font_size = min(max(size_val//2,10),24)

      for i,control,color in enumerate(zip(letter_controls,colors)):
        char = control['char']
        tag_name = f'''indiv_char_{i}'''
        individual_preview_text.insert(tk.END,char,tag_name)
        font_styles = []
        if control['bold_var'].get():
          font_styles.append('bold')

        if control['italic_var'].get():
          font_styles.append('italic')

        if control['underline_var'].get():
          font_styles.append('underline')

        if control['strike_var'].get():
          font_styles.append('overstrike')

        font = ('Arial',base_font_size,' '.join(font_styles) if font_styles else 'normal')
        individual_preview_text.tag_config(tag_name,foreground=color,font=font)

      individual_preview_text.config(state=tk.DISABLED)
      return None
    except ValueError as ve:
      messagebox.showerror('Input Error',str(ve))
      return None
    except Exception as e:
      messagebox.showerror('Error',f'''An unexpected error occurred: {e}''')
      return None

def on_export_gradient():
  output = gradient_output_text.get('1.0',tk.END).strip()
  if output:
    messagebox.showerror('Error','No output to export. Please generate a name first.')
    return None
  else:
    export_to_profiles_ini(output)
    return None

def on_export_individual():
  output = individual_output_text.get('1.0',tk.END).strip()
  if output:
    messagebox.showerror('Error','No output to export. Please generate a name first.')
    return None
  else:
    export_to_profiles_ini(output)
    return None

def download_update(download_url,save_path):
  '''Downloads the update package from a given URL.'''
  try:
    with requests.get(download_url,stream=True) as r:
      r.raise_for_status()
      with open(save_path,'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
          f.write(chunk)

  except requests.exceptions.RequestException as e:
    messagebox.showerror('Download Error',f'''Failed to download update: {e}''')
    return False
  except IOError as e:
    messagebox.showerror('File Error',f'''Failed to save update file: {e}''')
    return False

  return True

def generate_and_run_batch_updater(downloaded_zip_path,install_dir,main_app_executable_name):
  '''
Generates a temporary batch script, writes it to disk, and runs it to perform the update.
This script will then self-delete.
'''
  if platform.system() != 'Windows':
    messagebox.showerror('Update Error','Automatic update via batch script is only supported on Windows.')
    return False
  else:
    batch_script_name = 'update_temp.bat'
    batch_script_path = os.path.join(install_dir,batch_script_name)
    temp_extract_dir_name = 'CloneHeroGenUpdateTemp'
    temp_extract_dir_path = os.path.join(tempfile.gettempdir(),temp_extract_dir_name)
    batch_content = f'''@echo off
rem This is a temporary update script generated by CloneHeroNameGen.
rem It will delete itself after finishing.

set "DOWNLOAD_PATH={downloaded_zip_path}"\nset "INSTALL_DIR={install_dir}"\nset "MAIN_EXE={main_app_executable_name}"\nset "TEMP_EXTRACT_DIR={temp_extract_dir_path}"

rem Wait a few seconds for the main app to completely close and release file locks
timeout /t 5 /nobreak > nul

rem Optional: Force kill the main app process just in case (can be aggressive)
taskkill /f /im %MAIN_EXE% > nul 2>&1

rem Clean up any previous temp extraction directory
if exist "%TEMP_EXTRACT_DIR%\\" rmdir /s /q "%TEMP_EXTRACT_DIR%"
mkdir "%TEMP_EXTRACT_DIR%"

rem Extract the update package using PowerShell (requires PowerShell 5.0+, usually present on Win10+)
powershell -Command "Expand-Archive -Path \'%DOWNLOAD_PATH%\' -DestinationPath \'%TEMP_EXTRACT_DIR%\' -Force"

rem Find the actual extracted application directory (could be root of zip or a subfolder)
set "EXTRACTED_APP_SOURCE="
for /d %%d in ("%TEMP_EXTRACT_DIR%\\*") do (
    set "EXTRACTED_APP_SOURCE=%%d"
    goto :found_extracted_dir
)
rem If no sub-directory found, assume files are directly in temp_extract_dir
if not defined EXTRACTED_APP_SOURCE set "EXTRACTED_APP_SOURCE=%TEMP_EXTRACT_DIR%"

:found_extracted_dir

rem Copy new files to installation directory, overwriting existing ones
xcopy /s /e /y "%EXTRACTED_APP_SOURCE%\\*" "%INSTALL_DIR%\\"

rem Clean up temporary files and directories
if exist "%TEMP_EXTRACT_DIR%\\" rmdir /s /q "%TEMP_EXTRACT_DIR%"
if exist "%DOWNLOAD_PATH%" del "%DOWNLOAD_PATH%"

rem Relaunch the main application
start "" "%INSTALL_DIR%\\%MAIN_EXE%"

rem Delete this batch script itself
del "%~f0"
'''
    try:
      with open(batch_script_path,'w') as f:
        f.write(batch_content)

    except Exception as e:
      messagebox.showerror('Update Error',f'''Failed to create or launch updater script: {e}''')
      return False

    subprocess.Popen(f'''start "" "{batch_script_path}"''',shell=True,creationflags=subprocess.DETACHED_PROCESS)
    return True

def check_for_updates():
  '''Checks GitHub for a new version and initiates batch script update if available.'''
  try:
    response = requests.get(GITHUB_RELEASE_API)
    response.raise_for_status()
    latest_release = response.json()
    latest_version = latest_release['tag_name'].lstrip('v')
    current_version = __version__.lstrip('v')
    print(f'''Current version: {current_version}''')
    print(f'''Latest version on GitHub: {latest_version}''')
    if tuple(map(int,latest_version.split('.'))) > tuple(map(int,current_version.split('.'))):
      message = f'''A new version ({latest_version}) is available!\nYou are currently on version {current_version}.\nDo you want to update now? The application will restart automatically.'''
      if messagebox.askyesno('Update Available',message):
        download_url = None
        for asset in latest_release['assets']:
          if asset['name'] == UPDATE_ZIP_FILENAME:
            download_url = asset['browser_download_url']
            break

        if download_url:
          if getattr(sys,'frozen',False):
            install_dir = os.path.dirname(sys.executable)
            main_app_exe_name = os.path.basename(sys.executable)
          else:
            install_dir = os.path.dirname(os.path.abspath(__file__))
            main_app_exe_name = 'NameGen.exe'

          temp_dir = tempfile.gettempdir()
          downloaded_zip_path = os.path.join(temp_dir,UPDATE_ZIP_FILENAME)
          if download_update(download_url,downloaded_zip_path):
            messagebox.showinfo('Update Downloaded','Update downloaded. Applying update and restarting application...')
            if generate_and_run_batch_updater(downloaded_zip_path,install_dir,main_app_exe_name):
              sys.exit(0)
              return None
            else:
              messagebox.showerror('Update Failed','Failed to launch updater. Please try again.')
              return None

          else:
            messagebox.showerror('Update Failed','Update download failed. Please try again later.')
            return None

        else:
          messagebox.showerror('Update Error',f'''Update asset \'{UPDATE_ZIP_FILENAME}\' not found in the latest GitHub release.''')
          return None

      else:
        messagebox.showinfo('Update Cancelled','Update cancelled. You can check for updates later.')
        return None

    else:
      messagebox.showinfo('No Updates','You are running the latest version.')
      return None

  except requests.exceptions.RequestException as e:
    messagebox.showerror('Network Error',f'''Could not check for updates. Please check your internet connection.\nError: {e}''')
    return None
  except Exception as e:
    messagebox.showerror('Update Error',f'''An unexpected error occurred during update check: {e}''')
    return None

def on_check_for_updates_button():
  '''Handles the \'Check for Updates\' button click.'''
  check_for_updates()

root = tk.Tk()
root.title(f'''Clone Hero Name Generator v{__version__}''')
root.geometry('1000x700')
root.minsize(800,600)
root.configure(bg='#2b2d30')
gradient_start_var = tk.StringVar(root,value='#8044AB')
gradient_color2_var = tk.StringVar(root)
gradient_color3_var = tk.StringVar(root)
gradient_color4_var = tk.StringVar(root)
gradient_end_var = tk.StringVar(root,value='#F2AAF6')
gradient_bold_var = tk.BooleanVar(root)
gradient_italic_var = tk.BooleanVar(root)
gradient_underline_var = tk.BooleanVar(root)
gradient_strike_var = tk.BooleanVar(root)
gradient_size_var = tk.StringVar(root)
gradient_spacing_var = tk.StringVar(root)
individual_size_var = tk.StringVar(root)
individual_spacing_var = tk.StringVar(root)
style = ttk.Style()
style.theme_use('clam')
main_bg = '#2b2d30'
panel_bg = '#2e3033'
text_color = '#e0e0e0'
input_bg = '#3a3d40'
accent_color = '#4d88ff'
style.configure('.',background=main_bg,foreground=text_color)
style.configure('TFrame',background=main_bg)
style.configure('TLabel',background=main_bg,foreground=text_color)
style.configure('TEntry',fieldbackground=input_bg,foreground=text_color,borderwidth=0,relief='flat',padding=5)
style.map('TEntry',fieldbackground=[('focus','#4a4d50')])
style.configure('TCheckbutton',background=main_bg,foreground=text_color)
style.map('TCheckbutton',background=[('active',main_bg)])
style.configure('LeftNav.TButton',background=panel_bg,foreground=text_color,borderwidth=0,focuscolor='none',relief='flat',font=('Arial',10,'bold'),padding=[10,15])
style.map('LeftNav.TButton',background=[('active','#3a3d40'),('pressed','#3a3d40')])
style.configure('Selected.LeftNav.TButton',background=accent_color,foreground='#ffffff',relief='flat',font=('Arial',10,'bold'))
style.configure('Content.TButton',background='#007acc',foreground='#ffffff',font=('Arial',10,'bold'),borderwidth=0,relief='flat',padding=5)
style.map('Content.TButton',background=[('active','#005f99'),('pressed','#004c80')])
style.configure('Content.TLabel',background=panel_bg,foreground=text_color)
header_frame = ttk.Frame(root,style='TFrame')
header_frame.pack(side=tk.TOP,fill=tk.X,padx=10,pady=10)
ttk.Label(header_frame,text='iamjrmh',font=('Arial',24,'bold'),foreground='#e0e0e0',background=main_bg).pack(side=tk.LEFT,padx=10)
search_entry = ttk.Entry(header_frame,width=30,style='TEntry')
search_entry.insert(0,'Search')
search_entry.bind('<FocusIn>',lambda e: __CHAOS_PY_NULL_PTR_VALUE_ERR__)
search_entry.bind('<FocusOut>',lambda e: __CHAOS_PY_NULL_PTR_VALUE_ERR__)
search_entry.pack(side=tk.RIGHT,padx=10,pady=5)
main_content_frame = ttk.Frame(root,style='TFrame')
main_content_frame.pack(side=tk.TOP,fill=tk.BOTH,expand=True,padx=10,pady=5)
left_panel = ttk.Frame(main_content_frame,width=150,style='TFrame')
left_panel.pack(side=tk.LEFT,fill=tk.Y,padx=(0,10))
left_panel.pack_propagate(False)
right_panel = ttk.Frame(main_content_frame,style='TFrame')
right_panel.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)
pages = {}
current_page = None
def show_page(page_name):
  global current_page
  for page in pages.values():
    page.pack_forget()

  page_to_show = pages.get(page_name)
  if page_to_show:
    page_to_show.pack(fill=tk.BOTH,expand=True)
    current_page = page_name

  for btn_name,btn_widget in nav_buttons.items():
    if btn_name == page_name:
      btn_widget.config(style='Selected.LeftNav.TButton')
      continue

    btn_widget.config(style='LeftNav.TButton')

nav_buttons_frame = ttk.Frame(left_panel,style='TFrame')
nav_buttons_frame.pack(fill=tk.X,pady=(20,0))
nav_buttons = {}
btn_gradient = ttk.Button(nav_buttons_frame,text='Gradient',command=lambda : show_page('gradient_page'),style='LeftNav.TButton')
btn_gradient.pack(fill=tk.X,pady=2)
nav_buttons['gradient_page'] = btn_gradient
btn_individual = ttk.Button(nav_buttons_frame,text='Single Letter Coloring',command=lambda : show_page('individual_page'),style='LeftNav.TButton')
btn_individual.pack(fill=tk.X,pady=2)
nav_buttons['individual_page'] = btn_individual
btn_featured = ttk.Button(nav_buttons_frame,text='Update',command=lambda : show_page('featured_page'),style='LeftNav.TButton')
btn_featured.pack(fill=tk.X,pady=2)
nav_buttons['featured_page'] = btn_featured
gradient_page = ttk.Frame(right_panel,padding=20,style='TFrame')
gradient_page.configure(style='TFrame')
pages['gradient_page'] = gradient_page
ttk.Label(gradient_page,text='jrmh.rh - Gradient Mode',font=('Arial',16,'bold'),style='TLabel').pack(fill=tk.X,pady=(0,15))
def create_gradient_input_row(parent_frame,label_text,entry_var,is_color_picker=True):
  row_frame = ttk.Frame(parent_frame,style='TFrame')
  row_frame.pack(fill=tk.X,pady=4)
  ttk.Label(row_frame,text=label_text,width=25,style='Content.TLabel').pack(side=tk.LEFT,padx=5)
  entry = ttk.Entry(row_frame,textvariable=entry_var,style='TEntry')
  entry.pack(side=tk.LEFT,fill=tk.X,expand=True,padx=5)
  if is_color_picker:
    picker_button = ttk.Button(row_frame,text='Pick Color',command=lambda cv=entry_var: choose_color(cv),style='Content.TButton')
    picker_button.pack(side=tk.LEFT,padx=5)

  return entry

ttk.Label(gradient_page,text='Name:',style='Content.TLabel').pack(anchor='w',pady=(10,0))
gradient_name_entry = ttk.Entry(gradient_page,style='TEntry')
gradient_name_entry.pack(fill=tk.X)
create_gradient_input_row(gradient_page,'Start Color (e.g. #8044ab)',gradient_start_var)
create_gradient_input_row(gradient_page,'Optional Color 2',gradient_color2_var)
create_gradient_input_row(gradient_page,'Optional Color 3',gradient_color3_var)
create_gradient_input_row(gradient_page,'Optional Color 4',gradient_color4_var)
create_gradient_input_row(gradient_page,'End Color (e.g. #f2aaf6)',gradient_end_var)
gradient_check_frame = ttk.Frame(gradient_page,style='TFrame')
gradient_check_frame.pack(anchor='w',pady=(15,0))
ttk.Checkbutton(gradient_check_frame,text='Bold',variable=gradient_bold_var,style='TCheckbutton').pack(side=tk.LEFT,padx=5)
ttk.Checkbutton(gradient_check_frame,text='Italic',variable=gradient_italic_var,style='TCheckbutton').pack(side=tk.LEFT,padx=5)
ttk.Checkbutton(gradient_check_frame,text='Underline',variable=gradient_underline_var,style='TCheckbutton').pack(side=tk.LEFT,padx=5)
ttk.Checkbutton(gradient_check_frame,text='Strikethrough',variable=gradient_strike_var,style='TCheckbutton').pack(side=tk.LEFT,padx=5)
ttk.Label(gradient_page,text='Font Size (optional):',style='Content.TLabel').pack(anchor='w',pady=(10,0))
gradient_size_entry = ttk.Entry(gradient_page,textvariable=gradient_size_var,style='TEntry')
gradient_size_entry.pack(fill=tk.X)
ttk.Label(gradient_page,text='Spacing (optional):',style='Content.TLabel').pack(anchor='w',pady=(5,0))
gradient_spacing_entry = ttk.Entry(gradient_page,textvariable=gradient_spacing_var,style='TEntry')
gradient_spacing_entry.pack(fill=tk.X)
gradient_button_frame = ttk.Frame(gradient_page,style='TFrame')
gradient_button_frame.pack(pady=20)
ttk.Button(gradient_button_frame,text='Generate',command=on_generate_gradient,style='Content.TButton').pack(side=tk.LEFT,padx=10)
ttk.Button(gradient_button_frame,text='Export to profiles.ini',command=on_export_gradient,style='Content.TButton').pack(side=tk.LEFT,padx=10)
ttk.Label(gradient_page,text='Output:',style='Content.TLabel').pack(anchor='w',pady=(0,5))
gradient_output_text = tk.Text(gradient_page,height=4,state=tk.DISABLED,wrap='word',relief='flat',bg=input_bg,fg=text_color)
gradient_output_text.pack(fill=tk.X,pady=(0,5))
ttk.Label(gradient_page,text='Preview:',style='Content.TLabel').pack(anchor='w',pady=(5,5))
gradient_preview_text = tk.Text(gradient_page,height=5,state=tk.DISABLED,wrap='word',relief='flat',bg=input_bg,fg=text_color)
gradient_preview_text.pack(fill=tk.BOTH,expand=True)
individual_page = ttk.Frame(right_panel,padding=20,style='TFrame')
pages['individual_page'] = individual_page
canvas = tk.Canvas(individual_page,highlightthickness=0,bg=main_bg)
scrollbar = ttk.Scrollbar(individual_page,orient='vertical',command=canvas.yview)
individual_scrollable_frame = ttk.Frame(canvas,style='TFrame')
individual_scrollable_frame.bind('<Configure>',lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
canvas.create_window((0,0),window=individual_scrollable_frame,anchor='nw')
canvas.configure(yscrollcommand=scrollbar.set)
ttk.Label(individual_scrollable_frame,text='jrmh.rh - Individual Letter Mode',font=('Arial',16,'bold'),style='TLabel').pack(fill=tk.X,pady=(0,15))
ttk.Label(individual_scrollable_frame,text='Name:',style='Content.TLabel').pack(anchor='w',pady=(10,0))
name_input_frame = ttk.Frame(individual_scrollable_frame,style='TFrame')
name_input_frame.pack(fill=tk.X)
individual_name_entry = ttk.Entry(name_input_frame,style='TEntry')
individual_name_entry.pack(side=tk.LEFT,fill=tk.X,expand=True)
update_button = ttk.Button(name_input_frame,text='Update Letters',command=update_individual_letters,style='Content.TButton')
update_button.pack(side=tk.RIGHT,padx=(10,0))
ttk.Label(individual_scrollable_frame,text='Letter Controls (Color | Styles):',style='Content.TLabel').pack(anchor='w',pady=(10,0))
individual_letter_controls_frame = ttk.Frame(individual_scrollable_frame,style='TFrame')
individual_letter_controls_frame.pack(fill=tk.X,pady=5)
ttk.Label(individual_scrollable_frame,text='Global Font Size (optional):',style='Content.TLabel').pack(anchor='w',pady=(10,0))
individual_size_entry = ttk.Entry(individual_scrollable_frame,textvariable=individual_size_var,style='TEntry')
individual_size_entry.pack(fill=tk.X)
ttk.Label(individual_scrollable_frame,text='Global Spacing (optional):',style='Content.TLabel').pack(anchor='w',pady=(5,0))
individual_spacing_entry = ttk.Entry(individual_scrollable_frame,textvariable=individual_spacing_var,style='TEntry')
individual_spacing_entry.pack(fill=tk.X)
individual_button_frame = ttk.Frame(individual_scrollable_frame,style='TFrame')
individual_button_frame.pack(pady=20)
ttk.Button(individual_button_frame,text='Generate',command=on_generate_individual,style='Content.TButton').pack(side=tk.LEFT,padx=10)
ttk.Button(individual_button_frame,text='Export to profiles.ini',command=on_export_individual,style='Content.TButton').pack(side=tk.LEFT,padx=10)
ttk.Label(individual_scrollable_frame,text='Output:',style='Content.TLabel').pack(anchor='w',pady=(0,5))
individual_output_text = tk.Text(individual_scrollable_frame,height=4,state=tk.DISABLED,wrap='word',relief='flat',bg=input_bg,fg=text_color)
individual_output_text.pack(fill=tk.X,pady=(0,5))
ttk.Label(individual_scrollable_frame,text='Preview:',style='Content.TLabel').pack(anchor='w',pady=(5,5))
individual_preview_text = tk.Text(individual_scrollable_frame,height=2,state=tk.DISABLED,wrap='word',relief='flat',bg=input_bg,fg=text_color)
individual_preview_text.pack(fill=tk.X)
canvas.pack(side='left',fill='both',expand=True,padx=(0,5))
scrollbar.pack(side='right',fill='y')
featured_page = ttk.Frame(right_panel,padding=20,style='TFrame')
pages['featured_page'] = featured_page
ttk.Label(featured_page,text='Update Functionality (Auto via Batch Script)',font=('Arial',20,'bold'),style='TLabel').pack(pady=20)
ttk.Label(featured_page,text=f'''Current Application Version: {__version__}''',style='TLabel').pack(pady=10)
ttk.Button(featured_page,text='Check for Updates',command=on_check_for_updates_button,style='Content.TButton').pack(pady=10)
ttk.Label(featured_page,text='Click \'Check for Updates\' to download and automatically update.',style='TLabel').pack(pady=5)
ttk.Label(featured_page,text='**Note:** This uses a temporary batch script for auto-update on Windows.',style='TLabel',foreground='yellow').pack(pady=5)
show_page('individual_page')
root.mainloop()