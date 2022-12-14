import customtkinter
import random
import string
import clipboard

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("300x200")
root.wm_title("Passwortgenerator")
root.configure(resizeable=False)

def gen():
    in1 = lenght_input1.get()
    # Check if the input is empty or contains only whitespace characters
    if not in1.strip():
        # Handle the error by displaying an error message
        error()
    else:
        # Convert the input to an integer
        in1 = int(in1)

        check1 = check.get()

        if check1 == 1:
            password = ''.join(random.choices(string.punctuation + string.ascii_letters + string.digits, k=int(in1)))
        else:
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=int(in1)))
        create_toplevel(password)

def create_toplevel(password):
    window = customtkinter.CTkToplevel(root)
    window.geometry("300x500")
    window.wm_title("Passwort")

    # create label on CTkToplevel window
    label = customtkinter.CTkLabel(window, text=password)
    label.pack(side="top", fill="both", expand=True, padx=40, pady=40)

    # create a "Copy" button on the Toplevel window
    copy_button = customtkinter.CTkButton(window, text="Kopieren", command=lambda: clipboard.copy(password))
    # pack the button against the top edge of the window and add some padding on the y-axis
    copy_button.pack(side="top", pady=15)

def error():
    window = customtkinter.CTkToplevel(root)
    window.geometry("300x500")
    window.wm_title("Fehler")

    # create label on CTkToplevel window
    label = customtkinter.CTkLabel(window, text="Geben Sie eine Zeichenlänge an.")
    label.pack(side="top", fill="both", expand=True, padx=40, pady=40)

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

check = customtkinter.CTkCheckBox(master=root, text="Sonderzeichen",)
check.pack(padx=20, pady=10)

lenght_input1 = customtkinter.CTkEntry(master=frame, placeholder_text="Länge")
lenght_input1.pack(pady=12, padx=10)

encrypt_button = customtkinter.CTkButton(root, text="Ausführen", command=gen)
encrypt_button.pack(pady=10,padx=10)

lenght_input1.pack()
encrypt_button.pack()

root.mainloop()
