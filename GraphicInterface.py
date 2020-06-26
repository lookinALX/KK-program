import tkinter as tk
from tkinter import ttk
import Functional as func

BD_EQUIP = None
BD_SAM = None


class WizardLikeApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('Program by Lukin Alexander ©')

        self.geometry('600x200+{}+{}'.format(self.winfo_screenwidth() // 2 - 300, self.winfo_screenheight() // 2 - 300))
        self.resizable(False, False)
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageStation, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)

        file_menu = tk.Menu(menu_bar, tearoff=0)

        file_menu.add_command(label='NEW', command=self.reset_window)
        file_menu.add_command(label='Station', command=lambda: self.show_frame(PageStation))
        file_menu.add_command(label='SAM', command=lambda: self.show_frame(PageTwo))
        file_menu.add_command(label=' ')  # Free space between buttons
        file_menu.add_command(label='Exit', command=self.quit)
        menu_bar.add_cascade(label='  File  ', menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)

        help_menu.add_command(label='Features', command=self.help_window_show)
        menu_bar.add_cascade(label='  Help  ', menu=help_menu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def reset_window(self):
        self.destroy()
        self.__init__()

    def help_window_show(self):
        window = ChildWindow()
        window.init_child('Window', '300x300')


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.parent = parent

        label1 = tk.Label(self, text='Enter equipment \nData Base directory:', font='Helvetica 12')
        label1.grid(row=0, column=0, sticky='w', pady=10, padx=20)

        ent_db_equip = ttk.Entry(self, width=35, font='Helvetica 11')
        ent_db_equip.insert(0, 'E:/Python Projects/KAESER_Program/test.csv')
        ent_db_equip.grid(row=0, column=1, columnspan=3)

        but_ok_db_equip = ttk.Button(self, text='OK',
                                     command=lambda: self.entry_equip_get_directory(ent_db_equip.get()))
        but_ok_db_equip.grid(row=0, column=5, pady=10, padx=20)

        label2 = tk.Label(self, text='Enter SAM \nData Base directory:', font='Helvetica 12')
        label2.grid(row=1, column=0, sticky='w', pady=10, padx=20)

        ent_sam_equip = tk.Entry(self, width=35, font='Helvetica 11')
        ent_sam_equip.grid(row=1, column=1, columnspan=3)

        but_ok_db_sam = ttk.Button(self, text='OK',
                                   command=lambda: self.entry_sam_get_directory(ent_sam_equip.get()))
        but_ok_db_sam.grid(row=1, column=5, pady=10, padx=20)

    @staticmethod
    def entry_equip_get_directory(entry):
        global BD_EQUIP  # TODO: do it without global
        direct_equip = func.csv_file_directory(entry)
        BD_EQUIP = direct_equip

    @staticmethod
    def entry_sam_get_directory(entry):
        global BD_SAM  # TODO: do it without global
        direct_equip = func.csv_file_directory(entry)
        BD_SAM = direct_equip


class PageStation(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        fake_label = tk.Label(self)
        fake_label.grid(row=4, column=1)

        label1 = tk.Label(self, text='Compressor:', font='Helvetica 11')
        label1.grid(row=0, column=1, pady=5)

        label2 = tk.Label(self, text='Dryer, filter, DSH:', font='Helvetica 11')
        label2.grid(row=2, column=1, pady=5)

        but_back_sp = ttk.Button(self, text='Start Page', command=lambda: controller.show_frame(StartPage))
        but_back_sp.grid(row=5, column=0, pady=20, padx=20)

        but_ok1 = ttk.Button(self, text='OK')
        but_ok1.grid(row=1, column=0, padx=20)

        equip_box1 = ttk.Combobox(self, values=[])
        equip_box1.grid(row=1, column=1, columnspan=2)

        but_ok2 = ttk.Button(self, text='OK')
        but_ok2.grid(row=3, column=0, padx=20)

        equip_box2 = ttk.Combobox(self, values=[])
        equip_box2.grid(row=3, column=1, columnspan=2)


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text='Page Two')
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text='Back to Home',
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text='Page One',
                            command=lambda: controller.show_frame(PageStation))
        button2.pack()


class ChildWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()

    def init_child(self, win_title, win_geometry):
        self.title(win_title)
        self.geometry(win_geometry + '+400+300')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()


app = WizardLikeApp()
app.mainloop()
