import customtkinter as ctk
from tkinter import messagebox
import requests
import json

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def delete_messages():
    token = token_entry.get().strip()
    dm_id = dm_entry.get().strip()
    num_messages = message_count_entry.get().strip()

    if not token or not dm_id or not num_messages.isdigit():
        messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides.")
        return

    num_messages = int(num_messages)

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    try:
        for _ in range(num_messages):
            response = requests.get(f"https://discord.com/api/v9/channels/{dm_id}/messages?limit=1", headers=headers)
            if response.status_code == 200 and len(response.json()) > 0:
                message_id = response.json()[0]["id"]
                delete_url = f"https://discord.com/api/v9/channels/{dm_id}/messages/{message_id}"
                delete_response = requests.delete(delete_url, headers=headers)
                if delete_response.status_code in [200, 204]:
                    status_label.configure(text=f"✅ Message {message_id} supprimé", text_color="green")
                else:
                    status_label.configure(text=f"❌ Erreur: {delete_response.text}", text_color="red")
            else:
                status_label.configure(text="🔍 Aucun message trouvé", text_color="orange")
                break
        messagebox.showinfo("Succès", f"{num_messages} messages supprimés avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

root = ctk.CTk()
root.title("Suppression de Messages Discord")
root.geometry("400x350")

title_label = ctk.CTkLabel(root, text="🗑️ Suppression Discord", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

token_entry = ctk.CTkEntry(root, placeholder_text="Token Discord", width=300, show="*")
token_entry.pack(pady=5)

dm_entry = ctk.CTkEntry(root, placeholder_text="ID du DM", width=300)
dm_entry.pack(pady=5)

message_count_entry = ctk.CTkEntry(root, placeholder_text="Nombre de messages", width=100)
message_count_entry.pack(pady=5)

delete_button = ctk.CTkButton(root, text="🗑️ Supprimer Messages", command=delete_messages, fg_color="red", hover_color="darkred")
delete_button.pack(pady=10)

status_label = ctk.CTkLabel(root, text="", font=("Arial", 12))
status_label.pack(pady=5)

root.mainloop()
