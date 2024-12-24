import tkinter as tk
from tkinter import ttk
from controller import FilmController, setup_page1_bindings, setup_page2_bindings


LARGEFONT = ("Verdana", 35)


class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Page1, Page2):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        if cont == Page1 and hasattr(frame, 'refresh_data'):
            frame.refresh_data()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Startpage", font=LARGEFONT)

        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Değerlendirdiğim Filmler",
                             command=lambda: controller.show_frame(Page1))

        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Film değerlendir",
                             command=lambda: controller.show_frame(Page2))

        button2.grid(row=2, column=1, padx=10, pady=10)


class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Değerlendirdiğim Filmler",
                          font=("Arial", 18, "bold"))
        label.grid(row=0, column=0, columnspan=4, pady=10)

        filter_frame = ttk.LabelFrame(
            self, text="Filtreler", padding="5 5 5 5")
        filter_frame.grid(row=1, column=0, columnspan=4,
                          sticky="ew", padx=5, pady=5)

        self.name_var = tk.StringVar()
        self.type_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.min_rating_var = tk.StringVar()
        self.max_rating_var = tk.StringVar()

        ttk.Label(filter_frame, text="Film Adı:").grid(
            row=0, column=0, padx=5, pady=2)
        ttk.Entry(filter_frame, textvariable=self.name_var).grid(
            row=0, column=1, padx=5, pady=2)

        ttk.Label(filter_frame, text="Tür:").grid(
            row=0, column=2, padx=5, pady=2)
        ttk.Entry(filter_frame, textvariable=self.type_var).grid(
            row=0, column=3, padx=5, pady=2)

        ttk.Label(filter_frame, text="Durum:").grid(
            row=1, column=0, padx=5, pady=2)
        ttk.Entry(filter_frame, textvariable=self.status_var).grid(
            row=1, column=1, padx=5, pady=2)

        ttk.Label(filter_frame, text="Min Puan:").grid(
            row=1, column=2, padx=5, pady=2)
        ttk.Entry(filter_frame, textvariable=self.min_rating_var).grid(
            row=1, column=3, padx=5, pady=2)

        ttk.Label(filter_frame, text="Max Puan:").grid(
            row=2, column=0, padx=5, pady=2)
        ttk.Entry(filter_frame, textvariable=self.max_rating_var).grid(
            row=2, column=1, padx=5, pady=2)

        columns = ('name', 'type', 'status', 'rating', 'review')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')

        self.tree.heading('name', text='Film Adı')
        self.tree.heading('type', text='Tür')
        self.tree.heading('status', text='Durum')
        self.tree.heading('rating', text='Puan')
        self.tree.heading('review', text='Değerlendirme')

        self.tree.column('name', width=150)
        self.tree.column('type', width=100)
        self.tree.column('status', width=100)
        self.tree.column('rating', width=70)
        self.tree.column('review', width=200)

        scrollbar = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=2, column=0, columnspan=4,
                       sticky='nsew', padx=5, pady=5)
        scrollbar.grid(row=2, column=4, sticky='ns')

        button = ttk.Button(self, text="Ana Sayfa",
                            command=lambda: controller.show_frame(StartPage))
        button.grid(row=3, column=0, columnspan=4, pady=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.controller = controller
        setup_page1_bindings(self)

    def refresh_data(self):
        if hasattr(self, 'tree'):
            self.name_var.set('')
            self.type_var.set('')
            self.status_var.set('')
            self.min_rating_var.set('')
            self.max_rating_var.set('')

            controller = FilmController()
            films = controller.load_films()

            for item in self.tree.get_children():
                self.tree.delete(item)

            for film in films:
                self.tree.insert('', 'end', values=(
                    film.get('name', ''),
                    film.get('type', ''),
                    film.get('watch_status', ''),
                    film.get('rating', ''),
                    film.get('review', '')
                ))


class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Film Ekle", font=("Arial", 18, "bold"))
        label.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        ttk.Label(self, text="Film ismi:").grid(
            row=1, column=0, sticky="w", padx=10, pady=5)
        ttk.Entry(self).grid(row=1, column=1, sticky="we", padx=10, pady=5)

        ttk.Label(self, text="Film türü:").grid(
            row=2, column=0, sticky="w", padx=10, pady=5)
        ttk.Entry(self).grid(row=2, column=1, sticky="we", padx=10, pady=5)

        ttk.Label(self, text="İzlenme durumu:").grid(
            row=3, column=0, sticky="w", padx=10, pady=5)
        ttk.Entry(self).grid(row=3, column=1, sticky="we", padx=10, pady=5)

        ttk.Label(self, text="Film değerlendirmesi:").grid(
            row=4, column=0, sticky="w", padx=10, pady=5)
        ttk.Entry(self).grid(row=4, column=1, sticky="we", padx=10, pady=5)

        ttk.Label(self, text="Puan:").grid(
            row=5, column=0, sticky="w", padx=10, pady=5)
        ttk.Entry(self).grid(row=5, column=1, sticky="we", padx=10, pady=5)

        ttk.Label(self, text="Film türü:").grid(
            row=6, column=0, sticky="w", padx=10, pady=5)
        ttk.Entry(self).grid(row=6, column=1, sticky="we", padx=10, pady=5)

        ttk.Label(self, text="İzlenme durumu:").grid(
            row=7, column=0, sticky="w", padx=10, pady=5)
        ttk.Entry(self).grid(row=7, column=1, sticky="we", padx=10, pady=5)

        button_create = ttk.Button(
            self, text="Oluştur", command=self.create_action)
        button_create.grid(row=4, column=2, padx=20, pady=10, sticky="w")

        button1 = ttk.Button(self, text="Değerlendirdiğim Filmler",
                             command=lambda: controller.show_frame(Page1))
        button1.grid(row=8, column=0, padx=10, pady=10)

        button2 = ttk.Button(self, text="Ana sayfa",
                             command=lambda: controller.show_frame(StartPage))
        button2.grid(row=8, column=1, padx=10, pady=10)

        self.grid_columnconfigure(1, weight=1)

        setup_page2_bindings(self)

    def create_action(self):
        print("Film bilgileri oluşturuldu!")


app = tkinterApp()
app.mainloop()
