from cgitb import text
import tkinter as tk
from tkinter import W, font
from turtle import width 
from tkcalendar import DateEntry
import sqlite3

conn = sqlite3.connect('feinstaubstation.db')
c = conn.cursor()

farbeHintergrund = '#cde3ed'

fenster = tk.Tk()
fenster.title('Feinstaubstation')
fenster.configure(bg=farbeHintergrund)
fenster.geometry('750x500')
sel=tk.StringVar() # vereinfacht, Werte von Widgets zu steuern

startdatum = '25.09.20' #Startdatum der standardmäßig geladenen Datensätze
enddatum = '24.09.21' #Enddatum der standardmäßig geladenen Datensätze

lblZeitraum = tk.Label(fenster, text="Verfügbarer Zeitraum: 25.09.2020 - 24.09.2021", bg=farbeHintergrund) #####################################eventuell dropdowns (Jahr, Monat, Tag)
lblZeitraum.grid(row=10, column=5)

lblOnlineSuchen = tk.Label(fenster, text="online suchen", font=("Segoe UI", 10, "underline"), bg=farbeHintergrund, fg='blue', cursor='hand2')
lblOnlineSuchen.grid(row=20, column=5)

def fensterOnlineSuchen(event=None):
    fensterZwei = tk.Toplevel(fenster)
    fensterZwei.configure(bg=farbeHintergrund)
    fensterZwei.geometry('500x300')

lblOnlineSuchen.bind("<Button-1>", fensterOnlineSuchen) #<Button-1> = linker Mausclick

kalender_dateEntry=DateEntry(fenster, selectmode='day', textvariable=sel, width=15) #Datums-Widget(Ort, Auswahlmodus, Variable)
kalender_dateEntry.set_date(startdatum)
kalender_dateEntry.grid(row=1, column=1, padx=20, pady=20)

# lblAusgabe=tk.Label(fenster, bg=farbeHintergrund)
# lblAusgabe.grid(row=1, column=2)

def my_upd(*args): #triggered, wenn sel sich verändert
    gewaehltesDatum = sel.get()
    splitDatum = gewaehltesDatum.split('.')
    # lblAusgabe.config(text=sel.get())
    # print('Messdaten vom: 20' + splitDatum[2] + '-' + splitDatum[1] + '-' + splitDatum[0])
    return splitDatum

def datenbankabfrage():
    gewaehltesDatum = sel.get()
    splitDatum = gewaehltesDatum.split('.')
    datumformat = splitDatum[2] + '-' + splitDatum[1] + '-' + splitDatum[0]
    fenster.title('Messdaten vom: 20' + splitDatum[2] + '-' + splitDatum[1] + '-' + splitDatum[0])
    # c.execute(f"""SELECT * FROM sds011 WHERE timestamp LIKE '20{datumformat}%' ORDER BY P1 DESC""") # alle Datensätze des gewählten Tages ausgeben
    c.execute(f"""SELECT
    MIN(temperature) as minFirstValue, MAX(temperature) as maxFirstValue, AVG(temperature) as avgFirstValue,
    MIN(humidity) as minSecondValue, MAX(humidity) as maxSecondValue, AVG(humidity) as avgSecondValue
    FROM dht22 WHERE timestamp LIKE '20{datumformat}%' UNION SELECT
    MIN(P1) as minFirstValue, MAX(P1) as maxFirstValue, AVG(P1) as avgFirstValue,
    MIN(P2) as minSecondValue, MAX(P2) as maxSecondValue, AVG(P2) as avgSecondValue
    FROM sds011 WHERE timestamp LIKE '20{datumformat}%'""")
    db_ergebnisse = c.fetchall()
    print(db_ergebnisse)
    AusgabeMinTemp = 'Tiefstwert:', db_ergebnisse[0][0], '°C'
    lblAusgabeMinTemp = tk.Label(fenster, text=AusgabeMinTemp, bg=farbeHintergrund)
    lblAusgabeMinTemp.grid(row=3, column=2)
    AusgabeMaxTemp = 'Höchstwert:', db_ergebnisse[0][1], '°C'
    lblAusgabeMaxTemp = tk.Label(fenster, text=AusgabeMaxTemp, bg=farbeHintergrund)
    lblAusgabeMaxTemp.grid(row=4, column=2)
    AusgabeAvgTemp = 'Durchschnittswert:', db_ergebnisse[0][2], '°C'
    lblAusgabeAvgTemp = tk.Label(fenster, text=AusgabeAvgTemp, bg=farbeHintergrund)
    lblAusgabeAvgTemp.grid(row=5, column=2)

    AusgabeMinHum = 'Tiefstwert:', db_ergebnisse[0][3], '% Luftfeuchtigkeit'
    lblAusgabeMinHum = tk.Label(fenster, text=AusgabeMinHum, bg=farbeHintergrund)
    lblAusgabeMinHum.grid(row=6, column=2)
    AusgabeMaxHum = 'Höchstwert:', db_ergebnisse[0][4], '% Luftfeuchtigkeit'
    lblAusgabeMaxHum = tk.Label(fenster, text=AusgabeMaxHum, bg=farbeHintergrund)
    lblAusgabeMaxHum.grid(row=7, column=2)
    AusgabeAvgHum = 'Durchschnittswert:', db_ergebnisse[0][5], '% Luftfeuchtigkeit'
    lblAusgabeAvgHum = tk.Label(fenster, text=AusgabeAvgHum, bg=farbeHintergrund)
    lblAusgabeAvgHum.grid(row=8, column=2)

    AusgabeMinP1 = 'Tiefstwert:', db_ergebnisse[1][0], 'P1-Partikel (10 µm)'
    lblAusgabeMinP1 = tk.Label(fenster, text=AusgabeMinP1, bg=farbeHintergrund)
    lblAusgabeMinP1.grid(row=9, column=2)
    AusgabeMaxP1 = 'Höchstwert:', db_ergebnisse[1][1], 'P1-Partikel (10 µm)'
    lblAusgabeMaxP1 = tk.Label(fenster, text=AusgabeMaxP1, bg=farbeHintergrund)
    lblAusgabeMaxP1.grid(row=10, column=2)
    AusgabeAvgP1 = 'Durchschnittswert:', db_ergebnisse[1][2], 'P1-Partikel (10 µm)'
    lblAusgabeAvgP1 = tk.Label(fenster, text=AusgabeAvgP1, bg=farbeHintergrund)
    lblAusgabeAvgP1.grid(row=11, column=2)

    AusgabeMinP2 = 'Tiefstwert:', db_ergebnisse[1][3], 'P2-Partikel (<0,1µm)'
    lblAusgabeMinP2 = tk.Label(fenster, text=AusgabeMinP2, bg=farbeHintergrund)
    lblAusgabeMinP2.grid(row=12, column=2)
    AusgabeMaxP2 = 'Höchstwert:', db_ergebnisse[1][4], 'P2-Partikel (<0,1µm)'
    lblAusgabeMaxP2 = tk.Label(fenster, text=AusgabeMaxP2, bg=farbeHintergrund)
    lblAusgabeMaxP2.grid(row=13, column=2)
    AusgabeAvgP2 = 'Durchschnittswert:', db_ergebnisse[1][5], 'P2-Partikel (<0,1µm)'
    lblAusgabeAvgP2 = tk.Label(fenster, text=AusgabeAvgP2, bg=farbeHintergrund)
    lblAusgabeAvgP2.grid(row=14, column=2)
    

btnMessdatenAnzeigen = tk.Button(fenster, text='Messdaten anzeigen', width=15, bd=1, bg=farbeHintergrund, activebackground=farbeHintergrund, relief=tk.SOLID, command=datenbankabfrage)
btnMessdatenAnzeigen.grid(row=1, column=2, sticky=W)

sel.trace('w', my_upd) #trace verfolgt Änderungen von sel und führt daraufhin my_upd() aus

fenster.mainloop()