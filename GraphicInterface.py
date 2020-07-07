import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import Functional as func
import configurations as conf

BD_EQUIP = None
BD_SAM = None


class WizardLikeApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('Program by Lukin Alexander ©')

        self.geometry('600x250+{}+{}'.format(self.winfo_screenwidth() // 2 - 300, self.winfo_screenheight() // 2 - 300))
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

        label1 = tk.Label(self, text='Enter equipment \nData Base directory:', font='12')
        label1.grid(row=0, column=0, sticky='w', pady=30, padx=20)

        ent_db_equip = ttk.Entry(self, width=35, font='Helvetica 11')
        ent_db_equip.insert(0, 'E:/Python Projects/KAESER_Program/test.csv')
        ent_db_equip.grid(row=0, column=1, columnspan=3)

        but_ok_db_equip = ttk.Button(self, text='OK',
                                     command=lambda: self.entry_equip_get_directory(ent_db_equip.get()))
        but_ok_db_equip.grid(row=0, column=5, pady=10, padx=20)

        label2 = tk.Label(self, text='Enter SAM \nData Base directory:', font='12')
        label2.grid(row=1, column=0, sticky='w', pady=10, padx=20)

        ent_sam_equip = tk.Entry(self, width=35, font='Helvetica 11')
        ent_sam_equip.grid(row=1, column=1, columnspan=3)
        ent_sam_equip.insert(0, 'E:/Python Projects/KAESER_Program/sam.csv')

        but_ok_db_sam = ttk.Button(self, text='OK',
                                   command=lambda: self.entry_sam_get_directory(ent_sam_equip.get()))
        but_ok_db_sam.grid(row=1, column=5, pady=10, padx=20)

    @staticmethod
    def entry_equip_get_directory(entry):
        global BD_EQUIP  # TODO: do it without global
        try:
            direct_equip = func.csv_file_directory(entry)
            BD_EQUIP = direct_equip
        except FileNotFoundError:
            mb.showerror(title='Error', message='File is not found!')
        else:
            mb.showinfo(title='Success', message='Data Base has been downloaded')

    @staticmethod
    def entry_sam_get_directory(entry):
        global BD_SAM  # TODO: do it without global
        try:
            direct_equip = func.csv_file_directory(entry)
            BD_SAM = direct_equip
        except FileNotFoundError:
            mb.showerror(title='Error', message='File is not found!')
        else:
            mb.showinfo(title='Success', message='Data Base has been downloaded')


class PageStation(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        label1 = tk.Label(self, text='Compressor:', font='Helvetica 11')
        label1.grid(row=0, column=1, pady=3)

        label2 = tk.Label(self, text='Dryer:', font='Helvetica 11')
        label2.grid(row=2, column=1, pady=3)

        label3 = tk.Label(self, text='Filter, DSH:', font='Helvetica 11')
        label3.grid(row=4, column=1, pady=3)

        but_back_sp = ttk.Button(self, text='Start Page', command=lambda: controller.show_frame(StartPage))
        but_back_sp.grid(row=7, column=4, pady=20, padx=20)

        but_add1 = ttk.Button(self, text='Add', command=lambda: textbox.insert(tk.END, equip_box1.get()))
        but_add1.grid(row=1, column=0, padx=20)

        equip_box1 = AutocompleteCombobox(self, values=conf.Equipment.compressors)
        equip_box1.grid(row=1, column=1, columnspan=2)

        but_add2 = ttk.Button(self, text='Add')
        but_add2.grid(row=3, column=0, padx=20)

        equip_box2 = AutocompleteCombobox(self, values=conf.Equipment.dr_fl_dhs)
        equip_box2.grid(row=3, column=1, columnspan=2)

        but_add3 = ttk.Button(self, text='Add')
        but_add3.grid(row=5, column=0, padx=20, pady=5)

        equip_box3 = AutocompleteCombobox(self, values=conf.Equipment.dr_fl_dhs)
        equip_box3.grid(row=5, column=1, columnspan=2)

        textbox = tk.Listbox(self, width=20, height=15)
        textbox.grid(row=0, column=3, rowspan=8, padx=30, sticky='nse')

        scroll = tk.Scrollbar(self, command=textbox.yview)
        scroll.grid(row=0, column=3, rowspan=8, sticky='nse')
        textbox.config(yscrollcommand=scroll.set)

        but_get_deliv_list = ttk.Button(self, text='Delivery list',
                                        command=lambda: self.get_delivery_file(BD_EQUIP, textbox.get(0, tk.END)))
        but_get_deliv_list.grid(row=1, column=4, padx=20)

    def get_delivery_file(self, bd_file, name_list):
        try:
            func.New_Excel_creation_with_selection(bd_file, list(name_list))
        except AttributeError:
            mb.showerror(title='Error', message='Name is not exist')
        else:
            mb.showinfo(title='Success', message='Excel file has been created')


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label1 = tk.Label(self, text='SN compressors:')
        label1.grid(row=0, column=0, pady=10, padx=10)

        ent_sn_comp = ttk.Entry(self)
        ent_sn_comp.grid(row=0, column=1)
        ent_sn_comp.insert(0, '0')

        label2 = tk.Label(self, text='Another compressors:')
        label2.grid(row=1, column=0, pady=10, padx=10)

        ent_athr_comp = ttk.Entry(self)
        ent_athr_comp.grid(row=1, column=1)
        ent_athr_comp.insert(0, '0')

        label3 = tk.Label(self, text='SN units:\n(dryers, dhs, etc)')
        label3.grid(row=2, column=0, pady=10, padx=10)

        ent_sn_units = ttk.Entry(self)
        ent_sn_units.grid(row=2, column=1)
        ent_sn_units.insert(0, '0')

        label4 = tk.Label(self, text='Filters:')
        label4.grid(row=3, column=0, pady=10, padx=10)

        ent_filters = ttk.Entry(self)
        ent_filters.grid(row=3, column=1)
        ent_filters.insert(0, '0')

        label5 = tk.Label(self, text='Another units:')
        label5.grid(row=4, column=0, pady=10, padx=10)

        ent_an_units = ttk.Entry(self)
        ent_an_units.grid(row=4, column=1)
        ent_an_units.insert(0, '0')

        button1 = ttk.Button(self, text='Start Page', command=lambda: controller.show_frame(StartPage))
        button1.grid(row=4, column=2)

        button2 = ttk.Button(self, text='Page One', command=lambda: controller.show_frame(PageStation))
        button2.grid(row=5, column=2)

        button3 = ttk.Button(self, text='Calculate', command=lambda: self.get_sam_calculation(BD_SAM,
                                                    int(ent_sn_comp.get()) + int(ent_athr_comp.get()),
                                                    int(ent_sn_comp.get()) + int(ent_sn_units.get())))
        button3.grid(row=3, column=3)

    def get_sam_calculation(self, bd_file, amount_compr, sn_units):
        func.sam_calculation(bd_file, amount_compr, sn_units)
        mb.showinfo(title='Success', message='Excel file has been created')


class ChildWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()

    def init_child(self, win_title, win_geometry):
        self.title(win_title)
        self.geometry(win_geometry + '+400+300')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()


class AutocompleteCombobox(ttk.Combobox):
    def __init__(self, *args, **kwargs):
        """Use our completion list as our drop down selection menu, arrows move through menu."""
        super().__init__(*args, **kwargs)
        self._completion_list = self['values']
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)

    def autocomplete(self, delta=0):
        """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
        if delta:  # need to delete selection otherwise we would fix the current position
            self.delete(self.position, tk.END)
        else:  # set position to end so selection starts where text entry ended
            self.position = len(self.get())
        # collect hits
        _hits = []
        for element in self._completion_list:
            if element.lower().startswith(self.get().lower()):  # Match case insensitively
                _hits.append(element)
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        # now finally perform the auto completion
        if self._hits:
            self.delete(0, tk.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tk.END)

    def handle_keyrelease(self, event):
        """event handler for the keyrelease event on this widget"""
        if event.keysym == "BackSpace":
            self.delete(self.index(tk.INSERT), tk.END)
            self.position = self.index(tk.END)
        if event.keysym == "Left":
            if self.position < self.index(tk.END):  # delete the selection
                self.delete(self.position, tk.END)
            else:
                self.position = self.position - 1  # delete one character
                self.delete(self.position, tk.END)
        if event.keysym == "Right":
            self.position = self.index(tk.END)  # go to end (no selection)
        if len(event.keysym) == 1:
            self.autocomplete()


app = WizardLikeApp()
app.mainloop()
