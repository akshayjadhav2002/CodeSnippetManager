from tkinter import *
from tkinter import ttk, filedialog
from tkcode import CodeEditor
import subprocess
import os
import requests

root = Tk()
root.title("Code Snippet Manager")
root.geometry("1420x820")
file_path = ""

# Define the color theme from the CodeEditor widget
select_bg_color = "#282a36"  # Example select background color

# Define the color themes
dark_theme = {
    "bg": "#282a36",
    "fg": "white",
    "select_bg": "grey",
    "select_fg": "white"
}

light_theme = {
    "bg": "white",
    "fg": "black",
    "select_bg": "grey",
    "select_fg": "black"
}

current_theme = dark_theme  # Default theme is dark theme

def changeMode():
    global current_theme
    if current_theme == dark_theme:
        current_theme = light_theme
    else:
        current_theme = dark_theme
    apply_theme()

def apply_theme():
    # Apply theme to various widgets
    root.configure(bg=current_theme["bg"])

    code_editor.configure(
        background=current_theme["bg"],
        foreground=current_theme["fg"],
        selectbackground=current_theme["select_bg"],
        selectforeground=current_theme["select_fg"]
    )

    file_listbox.configure(
        bg=current_theme["bg"],
        fg=current_theme["fg"],
        selectbackground=current_theme["select_bg"],
        selectforeground=current_theme["select_fg"]
    )

    code_output.configure(
        bg=current_theme["bg"],
        fg=current_theme["fg"],
        insertbackground=current_theme["fg"]
    )

    docText.configure(
        bg=current_theme["bg"],
        fg=current_theme["fg"],
        insertbackground=current_theme["fg"]
    )
    middleFrame.configure(
        bg=current_theme["bg"],
        fg=current_theme["fg"],
        insertbackground=current_theme["fg"]
    )
    sideFrame.configure(
        bg=current_theme["bg"],
        fg=current_theme["fg"],
        insertbackground=current_theme["fg"]
    )
    root.configure(
        bg=current_theme["bg"],
        fg=current_theme["fg"],
        insertbackground=current_theme["fg"]
    )
    buttonFrame.configure(
        bg=current_theme["bg"],
        fg=current_theme["fg"],
        insertbackground=current_theme["fg"]
    )
    


def show_description():
    text = code_editor.get("1.0",END)
    lines = text.split("\n")
    for line in lines:
        if line.startswith("#"):
            comment=line[1:].strip()
            docText.insert(END,comment)


def set_file_path(path):
    global file_path
    file_path = path

def add_to_github():
    global file_path
    code = code_editor.get("1.0", END)
    if file_path != "":
        filename = os.path.basename(file_path)
        repository_path = "https://github.com/akshayjadhav2002/pythonpractices.codes.git"  # Replace this with your actual repository path
        github_username = "akshayjadhav2002"
        github_token = ""
        
        try:
            url = f"https://api.github.com/repos/{github_username}/{repository_path}/contents/{filename}"
            headers = {
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            response = requests.put(url, json={
                "message": "Add new code file",
                "content": code
            }, headers=headers)
            
            if response.status_code == 200:
                print("Code added to GitHub successfully!")
            else:
                print(f"Failed to add code to GitHub. Status code: {response.status_code}")
        except Exception as e:
            
            print("Error:", e)
            code_output.insert(END, e)
    else:
        print("No file selected.") 

def openFile():
    try:
        filePath = filedialog.askopenfilename(title="Open File?",
                                               initialdir="D:\\",
                                               filetypes=(("text files", "*.txt"), ("all files", "*.*"))
                                               )
        with open(filePath, "r") as file:
            content = file.read()
            code_editor.delete("1.0", END)
            code_editor.insert("1.0", content)
            set_file_path(filePath)
            list_files()
    except Exception as e:
        print("Exception handled:", e)

def run():
    global file_path
    code = code_editor.get("1.0", END)
    with open("temp.py", "w") as f:
        f.write(code)
    process = subprocess.Popen(['python', 'temp.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    code_output.delete("1.0", END)
    code_output.insert(END, output.decode("utf-8"))
    code_output.insert(END, error.decode("utf-8"))

def save_as():
    global file_path
    if file_path == "":
        path = filedialog.asksaveasfilename(filetypes=(("text files", "*.txt"), ("all files", "*.*")))
    else:
        path = file_path
    with open(path, "w") as file:
        code = code_editor.get("1.0", END)
        file.write(code)
        set_file_path(path)

def open_file():
    global file_path
    path = filedialog.askopenfilename(filetypes=(("text files", "*.txt"), ("all files", "*.*")))
    if path:
        with open(path, "r") as file:
            code = file.read()
            code_editor.delete("1.0", END)
            code_editor.insert("1.0", code)
            set_file_path(path)
        list_files()

def list_files():
    global file_path
    folder_path = os.path.dirname(file_path)
    folders = []
    files = []
    for item in os.listdir(folder_path):
        if os.path.isdir(os.path.join(folder_path, item)):
            folders.append(item)
        else:
            files.append(item)
    file_listbox.delete(0, END)
    file_listbox.insert(END, "Folders:")
    for folder in folders:
        file_listbox.insert(END, folder)
    file_listbox.insert(END, "")
    file_listbox.insert(END, "Files:")
    for file in files:
        file_listbox.insert(END, file)

def open_selected_file(event):
    global file_path
    selected_index = file_listbox.curselection()
    if selected_index:
        selected_item = file_listbox.get(selected_index)
        if selected_item not in ("Folders:", "Files:"):
            selected_file_path = os.path.join(os.path.dirname(file_path), selected_item)
            with open(selected_file_path, "r") as file:
                code = file.read()
                code_editor.delete("1.0", END)
                code_editor.insert("1.0", code)
                set_file_path(selected_file_path)

#icon image
icon_image = PhotoImage(file="D:\\PythonProject\\Code-Snippet-Manager\\logoimage.png")
root.iconphoto(False,icon_image)

# Side frame Widget
sideFrame = Frame(root, bg=select_bg_color, bd=2, relief=SUNKEN, height=900, width=300)
sideFrame.pack(side=LEFT, fill=Y)

# File Listbox
file_listbox = Listbox(sideFrame, width=30, bg=select_bg_color, fg="white", selectbackground="grey", selectforeground="white")
file_listbox.pack(side=TOP, fill=BOTH, expand=True)
file_listbox_label = Label(sideFrame, text="Files and Folders:", bg=select_bg_color, fg="white", font=("Arial", 10, "bold"))
file_listbox_label.pack(side=TOP, pady=5)
file_listbox_scrollbar = Scrollbar(sideFrame, orient=VERTICAL)
file_listbox_scrollbar.config(command=file_listbox.yview)
file_listbox_scrollbar.pack(side=RIGHT, fill=Y)
file_listbox.config(yscrollcommand=file_listbox_scrollbar.set)
file_listbox.bind('<Double-Button-1>', open_selected_file)

# MiddleFrame Widget
middleFrame = Frame(root, bg=select_bg_color, bd=2, relief=SUNKEN, height=900, width=600)
middleFrame.pack(side=LEFT, fill=Y)
code_editor = CodeEditor(middleFrame, width=60, height=20, language="python", highlighter="dracula",
                         background=select_bg_color, foreground="white", selectbackground="grey", selectforeground="white",
                         font="Consolas", autofocus=True, blockcursor=True,
                         insertofftime=0, padx=10, pady=10)
code_editor.pack(pady=5, padx=5)
code_editor.content = '''print("hello")'''

# Button Frame Widget
buttonFrame = Frame(middleFrame, bg=select_bg_color)
buttonFrame.pack(side=TOP, anchor=NE)

runButton = Button(buttonFrame, text="Run", command=run, bg="green", fg="white")
runButton.pack(side=RIGHT, padx=5)

saveButton = Button(buttonFrame, text="Save", command=save_as, bg=select_bg_color, fg="white")
saveButton.pack(side=RIGHT, padx=5)

openButton = Button(buttonFrame, text="Open", command=open_file, bg=select_bg_color, fg="white")
openButton.pack(side=RIGHT, padx=5)

addGitHubButton = Button(buttonFrame, text="Add to GitHub", command=add_to_github, bg=select_bg_color, fg="white")
addGitHubButton.pack(side=RIGHT, padx=5)

descriptionButton=Button(buttonFrame,text="Description",command=show_description,bg=select_bg_color, fg="white")
descriptionButton.pack(side=RIGHT, padx=5)

themeButton = Button(buttonFrame, text="DarkMode", bg=current_theme["bg"], fg=current_theme["fg"], command=changeMode)
themeButton.pack(side=RIGHT, padx=5)

# Output Frame Widget
outputFrame = Frame(root, bg=select_bg_color, bd=2, relief=SUNKEN, height=400, width=800)
outputFrame.pack(side=RIGHT, fill=BOTH, expand=True)

outputLabel = Label(outputFrame, text="Output:", bg=select_bg_color, fg="white", font=("Arial", 12, "bold"))
outputLabel.pack(anchor=NW, padx=10, pady=10)

code_output = Text(outputFrame , height=10, bg=select_bg_color, fg="white", insertbackground="white")
code_output.pack(fill=BOTH, expand=True, padx=10, pady=(0, 5))

# Documentation Frame Widget
docFrame = Frame(outputFrame, bg=select_bg_color, bd=2, relief=SUNKEN, height=150, width=800)
docFrame.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))

docLabel = Label(docFrame, text="Documentation:", bg=select_bg_color, fg="white", font=("Arial", 12, "bold"))
docLabel.pack(anchor=NW, padx=10, pady=10)

docText = Text(docFrame, wrap=WORD, bg=select_bg_color, fg="white", insertbackground="white")
docText.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))

root.mainloop()
