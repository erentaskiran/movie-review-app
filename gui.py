import tkinter as tk
from tkinter import ttk


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


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Startpage", font=LARGEFONT)

        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Page 1",
                             command=lambda: controller.show_frame(Page1))

        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Page 2",
                             command=lambda: controller.show_frame(Page2))

        button2.grid(row=2, column=1, padx=10, pady=10)


class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Başlık
        label = ttk.Label(self, text="Film Değerlendir",
                          font=("Arial", 18, "bold"))
        label.grid(row=0, column=0, columnspan=6, pady=10, sticky="w")

        # Form alanları
        ttk.Label(self, text="Film ismi:").grid(
            row=1, column=0, sticky="w", padx=10, pady=5)
        ttk.Entry(self).grid(row=1, column=1, columnspan=4,
                             sticky="we", padx=10, pady=5)

        ttk.Label(self, text="Film türü:").grid(
            row=2, column=0, sticky="w", padx=10, pady=5)
        ttk.Entry(self).grid(row=2, column=1, columnspan=4,
                             sticky="we", padx=10, pady=5)

        ttk.Label(self, text="İzlenme durumu:").grid(
            row=3, column=0, sticky="w", padx=10, pady=5)
        ttk.Entry(self).grid(row=3, column=1, columnspan=4,
                             sticky="we", padx=10, pady=5)

        ttk.Label(self, text="Puan aralığı:").grid(
            row=4, column=0, sticky="w", padx=10, pady=5)
        ttk.Entry(self).grid(row=4, column=1, sticky="we", padx=10, pady=5)
        ttk.Label(self, text="En düşük").grid(
            row=4, column=2, sticky="w", padx=5)
        ttk.Entry(self).grid(row=4, column=3, sticky="we", padx=10, pady=5)
        ttk.Label(self, text="En yüksek").grid(
            row=4, column=4, sticky="w", padx=5)

        # Etiketler bölümü
        ttk.Label(self, text="Etiketler:").grid(
            row=5, column=0, sticky="w", padx=10, pady=5)
        for i in range(6):
            ttk.Button(self, text="Gene").grid(
                row=5, column=i + 1, padx=5, pady=5)

        # Film kutusu
        frame = tk.Frame(self, bg="lightgray",
                         highlightbackground="blue", highlightthickness=2)
        frame.grid(row=6, column=0, columnspan=6,
                   padx=10, pady=10, sticky="we")

        tk.Canvas(frame, bg="red", width=100, height=100).grid(
            row=0, column=0, padx=10, pady=10)
        ttk.Label(frame, text="En düşük").grid(
            row=0, column=1, sticky="w", padx=10)
        ttk.Label(frame, text="En düşük").grid(
            row=1, column=1, sticky="w", padx=10)
        ttk.Label(frame, text="En düşük").grid(
            row=2, column=1, sticky="w", padx=10)

        # Geçiş düğmeleri
        button1 = ttk.Button(self, text="StartPage",
                             command=lambda: controller.show_frame(StartPage))
        button1.grid(row=7, column=0, padx=10, pady=10)

        button2 = ttk.Button(self, text="Page 2",
                             command=lambda: controller.show_frame(Page2))
        button2.grid(row=7, column=1, padx=10, pady=10)

        # Grid ayarları
        for i in range(6):
            self.grid_columnconfigure(i, weight=1)


class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Başlık
        label = ttk.Label(self, text="Film Ekle", font=("Arial", 18, "bold"))
        label.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        # Form alanları
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

        # Oluştur düğmesi
        button_create = ttk.Button(
            self, text="Oluştur", command=self.create_action)
        button_create.grid(row=4, column=2, padx=20, pady=10, sticky="w")

        # Geçiş düğmeleri
        button1 = ttk.Button(self, text="Page 1",
                             command=lambda: controller.show_frame(Page1))
        button1.grid(row=8, column=0, padx=10, pady=10)

        button2 = ttk.Button(self, text="StartPage",
                             command=lambda: controller.show_frame(StartPage))
        button2.grid(row=8, column=1, padx=10, pady=10)

        # Grid ayarları
        self.grid_columnconfigure(1, weight=1)

    def create_action(self):
        # Oluştur düğmesine basıldığında yapılacak işlemler
        print("Film bilgileri oluşturuldu!")


# Driver Code
app = tkinterApp()
app.mainloop()
