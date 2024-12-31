import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Görselleri işlemek için
import json
import os

jsonfile = "films.json"
USERS_FILE = "users.json"


def show_movie_details(movie):
    # Yeni pencere (Popup)
    details_window = tk.Toplevel(root)
    details_window.title(movie["name"])
    details_window.geometry("600x900")
    details_window.configure(bg="#1c1c1c")

    # Film Bannerı
    img = Image.open(movie["banner"])
    img = img.resize((300, 200), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)

    img_label = tk.Label(details_window, image=img, bg="#1c1c1c")
    img_label.image = img  # Referansı tutmak için
    img_label.pack(pady=10)

    # Film İsmi
    name_label = tk.Label(details_window, text=movie["name"], bg="#1c1c1c", fg="white",
                          font=("Arial", 16, "bold"))
    name_label.pack(pady=5)

    # Film Açıklaması
    description_label = tk.Label(details_window, text=movie.get("description", "Açıklama bulunamadı."),
                                 bg="#1c1c1c", fg="white", font=("Arial", 12), wraplength=500, justify="left")
    description_label.pack(pady=5)

    # Değerlendirmeler
    reviews_label = tk.Label(details_window, text="Değerlendirmeler:", bg="#1c1c1c", fg="white",
                             font=("Arial", 14, "bold"))
    reviews_label.pack(pady=5)

    print(movie)
    # Yorum ve Puanları Listele
    if "reviews" in movie and movie["reviews"]:

        for review in movie["reviews"]:
            print("asd")
            review_text = f"Puan: {
                review['rating']}/5\nYorum: {review['comment']}"
            review_label = tk.Label(details_window, text=review_text, bg="#2e2e2e", fg="white",
                                    font=("Arial", 12), wraplength=500, justify="left", padx=10, pady=10)
            review_label.pack(pady=5, fill=tk.BOTH, expand=True)
    else:
        review_label = tk.Label(details_window, text="Henüz bir değerlendirme yapılmadı.", bg="#2e2e2e", fg="white",
                                font=("Arial", 12), wraplength=500, justify="left", padx=10, pady=10)
        review_label.pack(pady=10, fill=tk.BOTH, expand=True)


def update_watchlist():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    for movie in movies:
        if (movie["status"] == "İzlenecek"):
            add_movie(movie["name"], movie["banner"],
                      movie["description"], movie["reviews"], movie["status"])


# JSON dosyasını yükle
def load_movies_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data


movies = load_movies_from_json(jsonfile)

# JSON dosyasına kaydetme


def save_movies(movies):
    with open(jsonfile, "w") as file:
        json.dump(movies, file, indent=4)


def open_review_movies():
    # Yeni pencere (Popup)
    review_window = tk.Toplevel(root)
    review_window.title("Değerlendir")
    review_window.geometry("600x800")
    review_window.configure(bg="#1c1c1c")

    # Başlık
    title_label = tk.Label(review_window, text="Dizi/Film Değerlendir",
                           bg="#1c1c1c", fg="white", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Search Bar
    search_frame = tk.Frame(review_window, bg="#2e2e2e")
    search_frame.pack(pady=10, padx=10, fill=tk.X)

    search_label = tk.Label(search_frame, text="Ara:",
                            bg="#2e2e2e", fg="white", font=("Arial", 12))
    search_label.pack(side=tk.LEFT, padx=5)

    search_entry = tk.Entry(search_frame, font=("Arial", 12), width=40)
    search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

    search_button = tk.Button(search_frame, text="Ara", bg="#4b4b4b", fg="white", font=("Arial", 10, "bold"),
                              command=lambda: search_movie(search_entry.get()))
    search_button.pack(side=tk.LEFT, padx=5)

    # Film/Dizi Listesi
    movie_listbox = tk.Listbox(review_window, font=("Arial", 12), bg="#2e2e2e",
                               fg="white", selectbackground="#4b4b4b", height=10)
    movie_listbox.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

    # Film/Dizi Bilgileri
    details_frame = tk.Frame(review_window, bg="#1c1c1c")
    details_frame.pack(pady=10, padx=10, fill=tk.X)

    banner_label = tk.Label(details_frame, text="Film Afişi",
                            bg="#2e2e2e", fg="white", font=("Arial", 12), width=40, height=10)
    banner_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

    name_label = tk.Label(details_frame, text="Film Adı:",
                          bg="#1c1c1c", fg="white", font=("Arial", 12))
    name_label.grid(row=0, column=1, sticky="w", padx=5)

    name_value = tk.Label(details_frame, text="", bg="#1c1c1c",
                          fg="white", font=("Arial", 12, "bold"))
    name_value.grid(row=0, column=2, sticky="w", padx=5)

    # Yorum ve Puan Girişi
    input_frame = tk.Frame(review_window, bg="#1c1c1c")
    input_frame.pack(pady=10, padx=10, fill=tk.X)

    comment_label = tk.Label(input_frame, text="Yorum:",
                             bg="#1c1c1c", fg="white", font=("Arial", 12))
    comment_label.grid(row=0, column=0, sticky="w", padx=5)

    comment_entry = tk.Text(input_frame, font=(
        "Arial", 12), height=5, width=40, wrap="word")
    comment_entry.grid(row=0, column=1, padx=5, pady=5)

    rating_label = tk.Label(input_frame, text="Puan (1-5):",
                            bg="#1c1c1c", fg="white", font=("Arial", 12))
    rating_label.grid(row=1, column=0, sticky="w", padx=5)

    rating_entry = tk.Entry(input_frame, font=("Arial", 12), width=5)
    rating_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

    # Film Seçim ve Değerlendirme İşlevleri
    def load_movie_details(index):
        movie = movies[index]
        name_value.config(text=movie["name"])
        img = Image.open("image.png")  # Örnek resim dosyası, güncelle
        img = img.resize((140, 140), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        banner_label.config(image=img)
        banner_label.image = img  # Referansı sakla

    def submit_review():
        try:
            rating = int(rating_entry.get())
            if 1 <= rating <= 5:
                # Check if a movie is selected
                selected_index = movie_listbox.curselection()
                if selected_index:
                    # Seçilen film indeksini al
                    index = selected_index[0]
                    global movies
                    movie = movies[index]

                    # Kullanıcı bilgilerini ve yorumu al
                    comment = comment_entry.get("1.0", tk.END).strip()

                    # Yeni yorumu oluştur ve filmin "reviews" alanına ekle
                    new_review = {
                        "rating": rating,
                        "comment": comment
                    }
                    movie["reviews"].append(new_review)

                    # JSON dosyasını güncelle
                    save_movies(movies)

                    # Başarı mesajı ve pencereyi kapatma
                    messagebox.showinfo(
                        "Başarılı", "Değerlendirme kaydedildi!")
                    review_window.destroy()
                    movies = load_movies_from_json(jsonfile)
                else:
                    messagebox.showerror("Hata", "Lütfen bir film seçin.")
            else:
                messagebox.showerror(
                    "Hata", "Puan 1 ile 5 arasında olmalıdır!")
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli bir puan girin!")

    def search_movie(query):
        movie_listbox.delete(0, tk.END)
        for i, movie in enumerate(movies):
            if query.lower() in movie["name"].lower():
                movie_listbox.insert(tk.END, movie["name"])

    # Değerlendirme Butonu
    submit_button = tk.Button(review_window, text="Değerlendirmeyi Kaydet", bg="#4b4b4b", fg="white",
                              font=("Arial", 10, "bold"), command=submit_review)
    submit_button.pack(pady=10)

    # Listeyi ilk başlatma
    for movie in movies:
        movie_listbox.insert(tk.END, movie["name"])

    # Listbox'tan film seçimi
    movie_listbox.bind("<<ListboxSelect>>", lambda e: load_movie_details(
        movie_listbox.curselection()[0]))


def open_watched_movies():
    # Yeni pencere (Popup)
    watched_window = tk.Toplevel(root)
    watched_window.title("İzlenenler")
    watched_window.geometry("900x900")
    watched_window.configure(bg="#1c1c1c")

    # Başlık
    title_label = tk.Label(watched_window, text="İzlenen Filmler/Diziler", bg="#1c1c1c", fg="white",
                           font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Search Bar
    search_frame = tk.Frame(watched_window, bg="#2e2e2e")
    search_frame.pack(pady=10, padx=10, fill=tk.X)

    search_label = tk.Label(search_frame, text="Ara:",
                            bg="#2e2e2e", fg="white", font=("Arial", 12))
    search_label.pack(side=tk.LEFT, padx=5)

    search_entry = tk.Entry(search_frame, font=("Arial", 12), width=40)
    search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

    search_button = tk.Button(search_frame, text="Ara", bg="#4b4b4b", fg="white", font=("Arial", 10, "bold"),
                              command=lambda: search_watched_movies(search_entry.get()))
    search_button.pack(side=tk.LEFT, padx=5)

    # İzlenenler Container
    watched_frame = tk.Frame(
        watched_window, bg="#2e2e2e", width=850, height=500)
    watched_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    # Canvas ve Scrollbar
    canvas = tk.Canvas(watched_frame, bg="#2e2e2e", highlightthickness=0)
    scrollbar = ttk.Scrollbar(
        watched_frame, orient="horizontal", command=canvas.xview)
    scrollable_frame = tk.Frame(canvas, bg="#2e2e2e")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(xscrollcommand=scrollbar.set)

    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    # İzlenenleri Ekle
    def add_watched_movie(title, image_path, reviews=[]):
        # Kart çerçevesi
        movie_card = tk.Frame(scrollable_frame, bg="#3a3a3a",
                              width=150, height=220, relief=tk.RAISED, bd=2)
        movie_card.pack(side=tk.LEFT, padx=10, pady=10)

        # Film Bannerı
        img = Image.open(image_path)
        img = img.resize((140, 140), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)

        img_label = tk.Label(movie_card, image=img, bg="#3a3a3a")
        img_label.image = img
        img_label.pack(pady=5)

        # Film İsmi
        movie_label = tk.Label(movie_card, text=title, bg="#3a3a3a", fg="white", font=(
            "Arial", 12, "bold"), wraplength=140)
        movie_label.pack(pady=5)

        # Tıklanabilirlik: Tüm kart yüzeyi için
        movie_card.bind("<Button-1>", lambda event, movie={
            "name": title, "banner": image_path, "description": "Örnek açıklama", "reviews": reviews}: show_movie_details(movie))

    def search_watched_movies(query):
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        for movie in movies:
            if movie["status"] == "İzlendi" and query.lower() in movie["name"].lower():
                add_watched_movie(movie["name"], "image.png", movie["reviews"])

    for movie in movies:
        if movie["status"] == "İzlendi":
            add_watched_movie(movie["name"], "image.png", movie["reviews"])


# Dizi/Film Yönet Popup Penceresi
    # Yeni pencere (Popup)
def open_movie_manager():
    # Yeni pencere (Popup)
    manager_window = tk.Toplevel(root)
    manager_window.title("Dizi/Film Yönet")
    manager_window.geometry("600x800")
    manager_window.configure(bg="#1c1c1c")

    # Başlık
    title_label = tk.Label(manager_window, text="Dizi/Film Yönet",
                           bg="#1c1c1c", fg="white", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Search Bar
    search_frame = tk.Frame(manager_window, bg="#2e2e2e")
    search_frame.pack(pady=10, padx=10, fill=tk.X)

    search_label = tk.Label(search_frame, text="Ara:",
                            bg="#2e2e2e", fg="white", font=("Arial", 12))
    search_label.pack(side=tk.LEFT, padx=5)

    search_entry = tk.Entry(search_frame, font=("Arial", 12), width=40)
    search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

    search_button = tk.Button(search_frame, text="Ara", bg="#4b4b4b", fg="white", font=("Arial", 10, "bold"),
                              command=lambda: search_movie(search_entry.get()))
    search_button.pack(side=tk.LEFT, padx=5)

    # Arama sonucu ve durum seçimi
    movie_frame = tk.Frame(manager_window, bg="#1c1c1c")
    movie_frame.pack(pady=10, padx=10, fill=tk.X)

    movie_label = tk.Label(movie_frame, text="Film/Dizi Adı:",
                           bg="#1c1c1c", fg="white", font=("Arial", 12))
    movie_label.grid(row=0, column=0, sticky="w", padx=5)

    movie_name = tk.Entry(movie_frame, font=("Arial", 12), width=30)
    movie_name.grid(row=0, column=1, padx=5, pady=5)

    status_label = tk.Label(movie_frame, text="Durum:",
                            bg="#1c1c1c", fg="white", font=("Arial", 12))
    status_label.grid(row=1, column=0, sticky="w", padx=5)

    status_var = tk.StringVar(value="İzlenecek")
    status_menu = ttk.Combobox(movie_frame, textvariable=status_var, font=("Arial", 12), state="readonly",
                               values=["İzlendi", "İzlenecek", "İzleniyor"])
    status_menu.grid(row=1, column=1, padx=5, pady=5)

    # Liste
    list_frame = tk.Frame(manager_window, bg="#1c1c1c")
    list_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    list_label = tk.Label(list_frame, text="Eklenen Filmler/Diziler:",
                          bg="#1c1c1c", fg="white", font=("Arial", 12))
    list_label.pack(anchor="w", padx=5, pady=5)

    movie_listbox = tk.Listbox(list_frame, font=(
        "Arial", 12), bg="#2e2e2e", fg="white", selectbackground="#4b4b4b")
    movie_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # İşlevsel butonlar
    button_frame = tk.Frame(manager_window, bg="#1c1c1c")
    button_frame.pack(pady=10, padx=10, fill=tk.X)

    add_button = tk.Button(button_frame, text="Ekle", bg="#4b4b4b", fg="white", font=("Arial", 10, "bold"),
                           command=lambda: add_movie(movie_name.get(), status_var.get()))
    add_button.pack(side=tk.LEFT, padx=5)

    delete_button = tk.Button(button_frame, text="Sil", bg="#4b4b4b", fg="white", font=("Arial", 10, "bold"),
                              command=lambda: delete_movie(movie_listbox.curselection()))
    delete_button.pack(side=tk.LEFT, padx=5)

    update_button = tk.Button(button_frame, text="Güncelle", bg="#4b4b4b", fg="white", font=("Arial", 10, "bold"),
                              command=lambda: update_movie(movie_listbox.curselection(), movie_name.get(), status_var.get()))
    update_button.pack(side=tk.LEFT, padx=5)

    # Mevcut filmleri listbox'a ekleme
    for movie in movies:
        movie_listbox.insert(tk.END, f"{movie['name']} ({movie['status']})")

    selected = -1
    # İşlevler

    def add_movie(name, status):
        # Kart çerçevesi
        if name:
            movies.append({"name": name, "status": status,
                          "banner": "image.png", "reviews": [], "description": ""})
            save_movies(movies)  # JSON'a kaydet
            movie_listbox.insert(tk.END, f"{name} ({status})")
            movie_name.delete(0, tk.END)
            update_watchlist()  # Ana sayfayı güncelle

    def delete_movie(selection):
        if selection:
            index = selection[0]
            del movies[index]
            save_movies(movies)  # JSON'a kaydet
            movie_listbox.delete(index)
            update_watchlist()  # Ana sayfayı güncelle

    def search_movie(name):
        query = name.lower()
        movie_listbox.delete(0, tk.END)
        for movie in movies:
            if query in movie["name"].lower():
                movie_listbox.insert(
                    tk.END, f"{movie['name']} ({movie['status']})")

    def update_movie(selection, name, status):
        if selection and name:
            index = selection[0]
            movies[index] = {"name": name, "status": status,
                             "banner": "image.png", "reviews": movies[index]["reviews"], "description": movies[index]["description"]}
            save_movies(movies)  # JSON'a kaydet
            movie_listbox.delete(index)
            movie_listbox.insert(index, f"{name} ({status})")
            update_watchlist()  # Ana sayfayı güncelle
            movie_listbox.selection_set(index)  # Odaklanma kaybolmasın

    def on_movie_select(event):
        try:
            selection = movie_listbox.curselection()
            if selection:
                index = selection[0]
                selected_movie = movies[index]
                movie_name.delete(0, tk.END)  # Adı temizle
                movie_name.insert(0, selected_movie["name"])  # Yeni adı ekle
                status_var.set(selected_movie["status"])  # Durumu seç
        except IndexError:
            pass

    def on_status_change(*args):
        selection = movie_listbox.curselection()
        if selection:
            update_movie(selection, movie_name.get(), status_var.get())


# Combobox değişikliklerini izlemek için Trace ekleniyor
    status_var.trace_add("write", on_status_change)

    movie_listbox.bind("<<ListboxSelect>>", on_movie_select)


def LoginRegisterPage():

    pencere = tk.Tk()
    pencere.title("Giriş Ekranı")
    pencere.geometry("600x500")
    pencere.configure(bg="#e6f7ff")

    # Resmin dosya yolunu kontrol edin
    arka_plan_resmi = Image.open("kraket.JPG")
    arka_plan_resmi = arka_plan_resmi.resize(
        (600, 500), Image.Resampling.LANCZOS)  # Boyutlandırma
    resim = ImageTk.PhotoImage(arka_plan_resmi)

    sag_frame = tk.Frame(pencere, bg="white", width=600,
                         height=500, bd=10, relief="solid")
    sag_frame.place(x=0, y=0)

    arka_plan_label = tk.Label(sag_frame, image=resim)
    arka_plan_label.image = resim
    # Resmi frame'in tamamına yay
    arka_plan_label.place(x=0, y=0, relwidth=1, relheight=1)

    giris_yap_label = tk.Label(sag_frame, text="Giriş Yap",
                               bg="black", fg="#ffcc00", font=("yu gothic ui", 14, "bold"))
    giris_yap_label.place(x=30, y=200)

    kullanici_adi_label = tk.Label(
        sag_frame, text="Kullanıcı Adı", bg="black", fg="white", font=("yu gothic ui", 12, "bold"))
    kullanici_adi_label.place(x=30, y=282)

    kullanici_adi_entry = tk.Entry(sag_frame, highlightthickness=0, relief=tk.FLAT,
                                   bg="black", fg="white", insertbackground="#3047ff", font=("yu gothic ui", 12))
    kullanici_adi_entry.place(x=170, y=288, width=200)

    kullanici_adi_cizgi = tk.Canvas(
        sag_frame, width=200, height=2.0, highlightthickness=0, bg="#00ffcc")
    kullanici_adi_cizgi.place(x=170, y=309)

    sifre_label = tk.Label(sag_frame, text="Şifre", bg="black",
                           fg="white", font=("yu gothic ui", 12, "bold"))
    sifre_label.place(x=30, y=360)

    sifre_entry = tk.Entry(sag_frame, highlightthickness=0, relief=tk.FLAT, bg="black",
                           fg="white", insertbackground="#3047ff", show="*", font=("yu gothic ui", 12))
    sifre_entry.place(x=170, y=359, width=200)

    def sifre_goster_gizle():
        if sifre_entry.cget('show') == '*':
            sifre_entry.config(show='')
        else:
            sifre_entry.config(show='*')

    show_buton_resmi = Image.open("göz.JPG")
    show_resim = ImageTk.PhotoImage(show_buton_resmi)
    show_buton_label = tk.Button(sag_frame, image=show_resim, bg="white", bd=0,
                                 cursor="hand2", activebackground="white", command=sifre_goster_gizle)
    show_buton_label.image = show_resim
    show_buton_label.place(x=372, y=367)

    sifre_cizgi = tk.Canvas(sag_frame, width=200,
                            height=2.0, highlightthickness=0, bg="#00ffcc")
    sifre_cizgi.place(x=170, y=383)

    def load_users():
        try:
            with open('users.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}  # Dosya yoksa boş bir sözlük döner
        except json.JSONDecodeError:
            return {}  # JSON hatası varsa boş bir sözlük döner

    kullanici_bilgileri = load_users()

    def girisyap():
        kullanici_adi = kullanici_adi_entry.get()
        sifre = sifre_entry.get()

        if kullanici_adi in kullanici_bilgileri and kullanici_bilgileri[kullanici_adi] == sifre:
            global jsonfile, movies
            jsonfile = kullanici_adi + jsonfile

            if not os.path.exists(jsonfile):
                with open(jsonfile, "w") as f:
                    json.dump([], f)
            movies = load_movies_from_json(jsonfile)
            pencere.destroy()
            return
        else:
            messagebox.showwarning(title="Giriş Başarısız!",
                                   message="Kullanıcı Bulunamadı!")

    giris_buton_resmi = Image.open("mavibar.JPG")
    giris_buton_resmi = giris_buton_resmi.resize(
        (150, 50), Image.Resampling.LANCZOS)
    giris_resim = ImageTk.PhotoImage(giris_buton_resmi)
    giris_buton_label = tk.Button(sag_frame, text="GİRİŞ YAP", compound="center", fg="white", image=giris_resim,
                                  bg="#040405", activebackground="#040405", cursor="hand2", bd=0, command=girisyap)
    giris_buton_label.image = giris_resim
    giris_buton_label.place(x=15, y=410)

    kayit_ol_label = tk.Label(sag_frame, text="Henüz Hesabınız Yok Mu?", font=(
        "yu gothic ui", 10, "bold"), bg="black", fg="white")
    kayit_ol_label.place(x=205, y=420)

    def kayitol():
        kayitpenceresi = tk.Toplevel(pencere)
        kayitpenceresi.title("Kayıt Ekranı")
        kayitpenceresi.geometry("600x500")
        kayitpenceresi.configure(bg="#e6f7ff")

        kayit_frame = tk.Frame(kayitpenceresi, bg="#2e2e3e",
                               width="600", height="500", bd=5, relief="solid")
        kayit_frame.place(x=0, y=0)

        arka_plan_label = tk.Label(kayit_frame, image=resim)
        arka_plan_label.image = resim
        arka_plan_label.place(x=0, y=0, relwidth=1, relheight=1)

        kayit_label = tk.Label(kayit_frame, text="KAYIT OL", font=(
            "yu gothic ui", 14, "bold"), bg="black", fg="#00ffcc")
        kayit_label.place(x=30, y=200)

        kayit_kullanici_adi = tk.Label(
            kayit_frame, text="Kullanıcı Adı", bg="black", fg="#ffffff", font=("yu gothic ui", 12, "bold"))
        kayit_kullanici_adi.place(x=30, y=280)

        kayit_kullanici_adi_entry = tk.Entry(kayit_frame, highlightthickness=0, relief=tk.FLAT,
                                             bg="black", fg="#ffffff", insertbackground="#ffffff", font=("yu gothic ui", 12))
        kayit_kullanici_adi_entry.place(x=170, y=288)

        kayit_kullanici_adi_cizgi = tk.Canvas(
            kayit_frame, width=200, height=2.0, highlightthickness=0, bg="#00ffcc")
        kayit_kullanici_adi_cizgi.place(x=170, y=312)

        kayit_sifre = tk.Label(kayit_frame, text="Şifre", bg="black",
                               fg="#ffffff", font=("yu gothic ui", 12, "bold"))
        kayit_sifre.place(x=30, y=360)

        kayit_sifre_entry = tk.Entry(kayit_frame, show="*", highlightthickness=0, relief=tk.FLAT,
                                     bg="black", fg="#ffffff", insertbackground="#ffffff", font=("yu gothic ui", 12))
        kayit_sifre_entry.place(x=170, y=362, width=200)

        def kyt_sifre_goster_gizle():
            if kayit_sifre_entry.cget('show') == '*':
                kayit_sifre_entry.config(show='')
            else:
                kayit_sifre_entry.config(show='*')

        kytshow_buton_resmi = Image.open("göz.JPG")
        kytshow_resim = ImageTk.PhotoImage(kytshow_buton_resmi)
        kytshow_buton_label = tk.Button(kayit_frame, image=kytshow_resim, bg="white",
                                        bd=0, cursor="hand2", activebackground="white", command=kyt_sifre_goster_gizle)
        kytshow_buton_label.image = kytshow_resim
        kytshow_buton_label.place(x=374, y=372)

        kayit_sifre_cizgi = tk.Canvas(
            kayit_frame, width=200, height=2.0, highlightthickness=0, bg="#00ffcc")
        kayit_sifre_cizgi.place(x=170, y=390)

        def gerigel():
            kayitpenceresi.destroy()

        def load_users():
            try:
                with open('users.json', 'r', encoding='utf-8') as file:
                    return json.load(file)
            except FileNotFoundError:
                return {}  # Dosya yoksa boş bir sözlük döner
            except json.JSONDecodeError:
                return {}  # JSON hatası varsa boş bir sözlük döner

        def save_users(users):
            with open('users.json', 'w', encoding='utf-8') as file:
                json.dump(users, file, ensure_ascii=False, indent=4)

        kullanici_bilgileri = load_users()

        def kayditamamla():
            kayit_kullanici = kayit_kullanici_adi_entry.get()
            kayit_sifre = kayit_sifre_entry.get()

            if kayit_kullanici and kayit_sifre:
                if kayit_kullanici in kullanici_bilgileri:
                    messagebox.showinfo(title="Hatalı Kayıt!",
                                        message="Bu kullanıcı zaten mevcut!")
                else:
                    kullanici_bilgileri[kayit_kullanici] = kayit_sifre
                    save_users(kullanici_bilgileri)
                    messagebox.showinfo(title="Başarılı Kayıt!",
                                        message="Kullanıcı başarıyla kaydedilmiştir!")
                    kayitpenceresi.destroy()

        kayit_tamamla_resmi = Image.open("mavibar.JPG")
        kayit_tamamla_resmi = kayit_tamamla_resmi.resize(
            (150, 50), Image.Resampling.LANCZOS)
        kayit_tamamla_resim = ImageTk.PhotoImage(kayit_tamamla_resmi)
        kayit_tamamla_label = tk.Button(kayit_frame, text="KAYDI TAMAMLA", compound="center", fg="white", image=kayit_tamamla_resim,
                                        bg="#040405", activebackground="#040405", cursor="hand2", bd=0, command=kayditamamla)
        kayit_tamamla_label.image = kayit_tamamla_resim
        kayit_tamamla_label.place(x=15, y=410)

        geri_gel_resmi = Image.open("mavibar.JPG")
        geri_gel_resmi = geri_gel_resmi.resize(
            (150, 50), Image.Resampling.LANCZOS)
        geri_gel_resim = ImageTk.PhotoImage(geri_gel_resmi)
        geri_gel_label = tk.Button(kayit_frame, text="GERİ", compound="center", fg="white",
                                   image=geri_gel_resim,
                                   bg="#040405", activebackground="#040405", cursor="hand2", bd=0, command=gerigel)
        geri_gel_label.image = geri_gel_resim
        geri_gel_label.place(x=420, y=410)

    kayit_buton_resmi = Image.open("mavibar.JPG")
    kayit_buton_resmi = kayit_buton_resmi.resize(
        (150, 50), Image.Resampling.LANCZOS)
    kayit_resim = ImageTk.PhotoImage(kayit_buton_resmi)
    kayit_buton_label = tk.Button(sag_frame, text="KAYIT OL", compound="center", fg="white", image=kayit_resim,
                                  bg="#040405", activebackground="#040405", cursor="hand2", bd=0, command=kayitol)
    kayit_buton_label.image = kayit_buton_resmi
    kayit_buton_label.place(x=420, y=410)

    pencere.mainloop()


# Ana pencere
LoginRegisterPage()
if (jsonfile == "films.json"):
    os._exit(0)
root = tk.Tk()
root.title("Filmdeğerlendir")
root.geometry("900x600")
root.configure(bg="#1c1c1c")  # Arkaplan rengi (koyu tema)

# Üst menü çubuğu
menu_frame = tk.Frame(root, bg="#2e2e2e", height=50)
menu_frame.pack(side=tk.TOP, fill=tk.X)

buttons = ["Dizi/film yönet", "İzlenenler",
           "Değerlendir",  "Şanslı günümdeyim"]
for button in buttons:
    if button == "Dizi/film yönet":
        btn = tk.Button(menu_frame, text=button, bg="brown", fg="black", font=("Arial", 10, "bold"), relief=tk.GROOVE,
                        command=open_movie_manager)
    elif button == "İzlenenler":
        btn = tk.Button(menu_frame, text=button, bg="brown", fg="black", font=("Arial", 10, "bold"), relief=tk.GROOVE,
                        command=open_watched_movies)
    elif button == "Değerlendir":
        btn = tk.Button(menu_frame, text=button, bg="brown", fg="black", font=("Arial", 10, "bold"), relief=tk.GROOVE,
                        command=open_review_movies)
    else:
        btn = tk.Button(menu_frame, text=button, bg="brown", fg="black", font=(
            "Arial", 10, "bold"), relief=tk.GROOVE)
    btn.pack(side=tk.LEFT, padx=5, pady=5)

# Watchlist Başlığı
watchlist_label = tk.Label(
    root, text="Watchlist", bg="#1c1c1c", fg="white", font=("Arial", 16, "bold"))
watchlist_label.pack(anchor="w", padx=10, pady=10)

# Watchlist Container
watchlist_frame = tk.Frame(root, bg="#2e2e2e", width=850, height=400)
watchlist_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Canvas ve Scrollbar
canvas = tk.Canvas(watchlist_frame, bg="#2e2e2e", highlightthickness=0)
scrollbar = ttk.Scrollbar(
    watchlist_frame, orient="horizontal", command=canvas.xview)
scrollable_frame = tk.Frame(canvas, bg="#2e2e2e")

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(
    scrollregion=canvas.bbox("all")))

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(xscrollcommand=scrollbar.set)

canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

# Filmleri listeye ekleme (örnek)


def add_movie(title, image_path, description="Açıklama mevcut değil", reviews=[], status=""):
    # Kart çerçevesi
    movie_card = tk.Frame(scrollable_frame, bg="#3a3a3a",
                          width=150, height=220, relief=tk.RAISED, bd=2)
    movie_card.pack(side=tk.LEFT, padx=10, pady=10)

    # Film Bannerı
    img = Image.open(image_path)
    img = img.resize((140, 140), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)

    img_label = tk.Label(movie_card, image=img, bg="#3a3a3a")
    img_label.image = img
    img_label.pack(pady=5)

    # Film İsmi
    movie_label = tk.Label(movie_card, text=title, bg="#3a3a3a", fg="white", font=(
        "Arial", 12, "bold"), wraplength=140)
    movie_label.pack(pady=5)

    # Tıklanabilirlik: Tüm kart yüzeyi için
    movie_card.bind("<Button-1>", lambda event, movie={
        "name": title, "banner": image_path, "description": description, "reviews": reviews, "status": status}: show_movie_details(movie))


update_watchlist()
root.mainloop()
