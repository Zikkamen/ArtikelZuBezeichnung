import pathlib
import os
from tkinter import *
import pandas as pd

root = Tk()
root.geometry("600x240")

def getOutputText():
    outputtext = ""

    for index, i in enumerate(text):
        if index > 0:
            outputtext += ", "
        outputtext += i

    textVorschau.config(state=NORMAL)
    textVorschau.delete("1.0", END)
    textVorschau.insert('1.0', outputtext)
    textVorschau.config(state=DISABLED)

    return outputtext

def getTextInput():
    stringArtNr=textArtNr.get("1.0","end").replace("\n", "")
    stringArtAmount=textArtAmount.get("1.0","end").replace("\n", "")

    try:
        Bezeichnung = df.query(f'colA == {stringArtNr}').iloc[0]['colB']
    except:
        return

    textArtNr.delete("1.0", END)
    textArtAmount.delete("1.0", END)
    text.append(f"{Bezeichnung} x{stringArtAmount}")
    getOutputText()

def copyToClipboard():
    string_to_copy = getOutputText()
    cmd = 'echo | set /p nul=' + str(string_to_copy) + '| clip'
    os.system(cmd)
    
    while len(text) > 0:
        text.pop()

    textVorschau.config(state=NORMAL)
    textVorschau.delete("1.0", END)
    textVorschau.config(state=DISABLED)


def undoLastAdd():
    if len(text) > 0:
        text.pop()
        getOutputText()

def change_in_opt(var_char):
    global df
    df = pd.read_csv(f"{CSV_folder_path}/{var_char}.csv", names=['colA', 'colB'], header=None)

def focus_next_window(event):
    event.widget.tk_focusNext().focus()
    return("break")

my_frame = Frame(root, width=600, height=300)
my_frame.pack()

textArtNrDesc=Label(my_frame, text="Artikel Nummer:")
textArtNrDesc.place(x=5, y=20, width=100, height=25)

textArtNr=Text(my_frame)
textArtNr.place(x=120, y=20, width=100, height=25)
textArtNr.bind("<Tab>", focus_next_window)

textArtAmountDesc=Label(my_frame, text="Artikel Anzahl:")
textArtAmountDesc.place(x=250, y=20, width=100, height=25)

textArtAmount=Text(my_frame)
textArtAmount.place(x=370, y=20, width=100, height=25)
textArtAmount.bind("<Tab>", focus_next_window)

btnAdd=Button(my_frame, text="Add", command=getTextInput)
btnAdd.place(x=500, y=20, width=80, height=25)

textVorschauDesc = Label(my_frame, text="Vorschau:")
textVorschauDesc.place(x=0, y=60, width=70, height=20)

textVorschau = Text(my_frame)
textVorschau.place(x=5, y=80, width=595, height=120)
textVorschau.config(state=DISABLED)

btnCopyToClipboard=Button(my_frame, text="Copy to Clipboard", command=copyToClipboard)
btnCopyToClipboard.config(font=("Lucida Grande", 7))
btnCopyToClipboard.place(x=490, y=210, width=100, height=25)

btnCopyToClipboard=Button(my_frame, text="Undo", command=undoLastAdd)
btnCopyToClipboard.place(x=400, y=210, width=80, height=25)

CSV_folder_path = f"{__file__}/../CSV"


text = []

list_of_paths = list(pathlib.Path(CSV_folder_path).glob('*.csv'))
OptionList = [p.stem for p in list_of_paths]
variable = StringVar(root)

try:
    variable.set(OptionList[0])
except:
    textVorschau.config(state=NORMAL)
    textVorschau.delete("1.0", END)
    textVorschau.insert('1.0', "Keine CSV Dateien im Ordner CSV gefunden")
    textVorschau.config(state=DISABLED)

opt = OptionMenu(my_frame, variable, *OptionList, command=change_in_opt)
opt.config(width=90, font=('Helvetica', 10))
opt.place(x=5, y=205, width=200, height=30)

change_in_opt(OptionList[0])

root.mainloop()