from cgitb import text
import tkinter as tk
from turtle import width 
from tkcalendar import DateEntry
import sqlite3

conn = sqlite3.connect("messdaten.db")
c = conn.cursor()

farbeHellblau = '#cde3ed'

fenster = tk.Tk()
fenster.title('Feinstaubstation™')
fenster.configure(bg=farbeHellblau)
fenster.geometry('750x500')
sel=tk.StringVar() # vereinfacht, Werte von Widgets zu steuern

startdatum = '25.09.20' #Startdatum der standardmäßig geladenen Datensätze
enddatum = '24.09.21' #Enddatum der standardmäßig geladenen Datensätze

kalender_dateEntry=DateEntry(fenster, selectmode='day', textvariable=sel, width=15) #Datums-Widget(Ort, Auswahlmodus, Variable)
kalender_dateEntry.set_date(startdatum)
kalender_dateEntry.grid(row=1, column=1, padx=20, pady=20)


def my_upd(*args): #triggered, wenn sel sich verändert
    gewaehltesDatum = sel.get()
    splitDatum = gewaehltesDatum.split('.')
    fenster.title('Messdaten vom: 20' + splitDatum[2] + '-' + splitDatum[1] + '-' + splitDatum[0])
    return splitDatum

def datenbankabfrage():
    gewaehltesDatum = sel.get()
    splitDatum = gewaehltesDatum.split('.')
    datumformat = splitDatum[2] + '-' + splitDatum[1] + '-' + splitDatum[0]
    c.execute(f"""SELECT * FROM sds011 WHERE timestamp LIKE '20{datumformat}%' ORDER BY P1 DESC""") # Beispiel: alle Daten eines ausgewählten Tages absteigend nach den Daten des P1-Sensors als Test in der Kosnole ausgeben
    db_ergebnisse = c.fetchall()
    print(db_ergebnisse)

btnMessdatenAnzeigen = tk.Button(fenster, text='Messdaten anzeigen', width=15, bd=1, bg=farbeHellblau, activebackground=farbeHellblau, relief=tk.SOLID, command=datenbankabfrage)
btnMessdatenAnzeigen.grid(row=2, column=1)

sel.trace('w', my_upd) #trace verfolgt Änderungen von sel und führt daraufhin my_upd() aus

fenster.mainloop()