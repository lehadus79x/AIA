import tkinter as tk
from tkinter import messagebox
import json

inventar = {}
FISIER_INVENTAR = "inventar.json"

# salveaza config
def salveaza_inventar():
    with open(FISIER_INVENTAR, "w") as f:
        json.dump(inventar, f)

# incarcare config
def incarca_inventar():
    global inventar
    try:
        with open(FISIER_INVENTAR, "r") as f:
            inventar = json.load(f)
    except FileNotFoundError:
        inventar = {}
    actualizeaza_lista()

# functiile pt butoane
def adauga_produs(nume, cantitate, pret):
    try:
        cantitate = int(cantitate) 
        pret = float(pret) 
        if nume: 
            inventar[nume] = {"cantitate": cantitate, "pret": pret} 
            salveaza_inventar()
            actualizeaza_lista() 
        else:
            messagebox.showwarning("Input invalid", "Te rog să introduci un nume de produs.") 
    except ValueError:
        messagebox.showwarning("Input invalid", "Te rog să introduci valori valide pentru cantitate și preț.") 

def sterge_produs(nume):
    if nume in inventar: 
        del inventar[nume]
        salveaza_inventar()
        actualizeaza_lista()
    else:
        messagebox.showwarning("Produs inexistent", "Produsul nu există în inventar.")  
        
def valoare_totala():
    total_valoare = sum(item["cantitate"] * item["pret"] for item in inventar.values())
    messagebox.showinfo("Valoare totală", f"Valoarea totală a inventarului este: {total_valoare:.2f} RON") 

def actualizeaza_lista():
    listbox.delete(0, tk.END)
    if not inventar:  # Verifică dacă inventarul este gol
        listbox.insert(tk.END, "Inventarul este gol. Adaugă produse!")
    else:
        for nume, detalii in sorted(inventar.items(), key=lambda item: item[0].lower()):  # Sortează produsele alfabetic
            text_produs = f"{nume} - Cantitate: {detalii['cantitate']}, Preț: {detalii['pret']:.2f} RON" 
            listbox.insert(tk.END, text_produs) 
def sterge_toate_produsele():
    inventar.clear()
    salveaza_inventar()  
    actualizeaza_lista()  
    
def cauta_produs():
    nume_produs = entry_cautare.get().lower()  # transforma numele in litere mici
    gasit = False 
    listbox.delete(0, tk.END)  # Șterge toate elementele din lista grafică
    for nume, detalii in inventar.items():  # Parcurge produsele din inventar
        if nume_produs in nume.lower():  # Verifică dacă numele produsului conține termenul de căutare
            text_produs = f"{nume} - Cantitate: {detalii['cantitate']}, Preț: {detalii['pret']:.2f} RON"  
            listbox.insert(tk.END, text_produs)  # 
            gasit = True  
    if not gasit:  
        listbox.insert(tk.END, "Nu s-au găsit produse care să corespundă căutării.")  

def reia_lista():
    actualizeaza_lista()  
# crearea aplicatiei
root = tk.Tk()
root.title("Inventar Magazin Alimentar")
root.geometry("639x575")
root.config(bg="#000000")

# font
font_label = ("Verdana", 10, "bold")
font_entry = ("Georgia", 10)
font_button = ("Georgia", 10, "bold")

# text adaugare pret, nume, cantitate
label_nume = tk.Label(root, text="Nume Produs (ex: Suc, Chipsuri, Ciocolată):", font=font_label, bg="#000000", fg="white")
label_nume.grid(row=0, column=0, padx=10, pady=10, sticky="w")

label_cantitate = tk.Label(root, text="Cantitate produs (ex: 10 bucăți, 5 litri):", font=font_label, bg="#000000", fg="white")
label_cantitate.grid(row=1, column=0, padx=10, pady=10, sticky="w")

label_pret = tk.Label(root, text="Preț unitar (ex: 5.99 RON):", font=font_label, bg="#000000", fg="white")
label_pret.grid(row=2, column=0, padx=10, pady=10, sticky="w")

entry_nume = tk.Entry(root, font=font_entry, width=30, bd=2, relief="solid", bg="#000000", fg="white")
entry_nume.grid(row=0, column=1, padx=10, pady=10)

entry_cantitate = tk.Entry(root, font=font_entry, width=30, bd=2, relief="solid", bg="#000000", fg="white")
entry_cantitate.grid(row=1, column=1, padx=10, pady=10)

entry_pret = tk.Entry(root, font=font_entry, width=30, bd=2, relief="solid", bg="#000000", fg="white")
entry_pret.grid(row=2, column=1, padx=10, pady=10)

# butoane aplicatie
buton_adauga = tk.Button(root, text="( + ) Adaugă Produs", bg="#388E3C", fg="white", font=font_button, command=lambda: adauga_produs(entry_nume.get(), entry_cantitate.get(), entry_pret.get()))
buton_adauga.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

buton_sterge = tk.Button(root, text="( - ) Șterge Produs", bg="#E53935", fg="white", font=font_button, command=lambda: sterge_produs(entry_nume.get()))
buton_sterge.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

buton_valoare_totala = tk.Button(root, text="( = ) Valoare Produse", bg="#0E2E00", fg="white", font=font_button, command=valoare_totala)
buton_valoare_totala.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

buton_sterge_toate = tk.Button(root, text="( X ) Șterge Toate Produsele", bg="#8B0000", fg="white", font=font_button, command=sterge_toate_produsele)
buton_sterge_toate.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

label_cautare = tk.Label(root, text="Căutare produs:", font=font_label, bg="#000000", fg="white")
label_cautare.grid(row=5, column=0, padx=10, pady=10, sticky="w")

entry_cautare = tk.Entry(root, font=font_entry, width=30, bd=2, relief="solid", bg="#000000", fg="white")
entry_cautare.grid(row=5, column=1, padx=10, pady=10)

buton_cautare = tk.Button(root, text="Caută", bg="#0288D1", fg="white", font=font_button, command=cauta_produs)
buton_cautare.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

buton_reia_lista = tk.Button(root, text="Reîncarcă întreaga listă", bg="#0D47A1", fg="white", font=font_button, command=reia_lista)
buton_reia_lista.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

#afișare inventar
listbox = tk.Listbox(root, width=80, height=10, font=("Arial", 10), bg="#000000", fg="white", bd=0)
listbox.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

#pornire aplicatie
incarca_inventar()
root.mainloop()
