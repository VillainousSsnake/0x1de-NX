
import customtkinter as ctk

root_1 = ctk.CTk()

root_1.protocol("WM_DELETE_WINDOW", lambda: root_1.destroy())

root_1.mainloop()

root_2 = ctk.CTk()

root_2.protocol("WM_DELETE_WINDOW", lambda: root_2.destroy())

root_2.mainloop()