import tkinter as tk
from tkinter import messagebox

# Ana pencere oluşturma
arayuz = tk.Tk()
arayuz.title("Para Simulatorü")
arayuz.geometry("400x350")

# Giriş ekranı bileşenleri
kullanici_adi = tk.Label(arayuz, text="Kullanıcı Adı:")
kullanici_adi.place(x=20, y=20)
kullanici_adigiris = tk.Entry(arayuz)
kullanici_adigiris.place(x=100, y=20)

sifre = tk.Label(arayuz, text="Şifre:")
sifre.place(x=20, y=60)
sifregiris = tk.Entry(arayuz, show="*")
sifregiris.place(x=100, y=60)

# Global değişkenler
kullanicilar = {}
current_user = None

def toggle_sifre():
    if sifregiris.cget("show") == "":
        sifregiris.config(show="*")
        sifre_goster_btn.config(text="Şifre Göster")
    else:
        sifregiris.config(show="")
        sifre_goster_btn.config(text="Şifre Gizle")

def open_kayit_window():
    if getattr(open_kayit_window, "window_open", False):
        return

    win = tk.Toplevel(arayuz)
    win.title("Kayıt Ol")
    win.geometry("350x300")
    open_kayit_window.window_open = True

    tk.Label(win, text="Kullanıcı Adı:").place(x=20, y=20)
    user_entry = tk.Entry(win)
    user_entry.place(x=130, y=20)

    tk.Label(win, text="E-posta:").place(x=20, y=60)
    email_entry = tk.Entry(win)
    email_entry.place(x=130, y=60)

    tk.Label(win, text="Şifre:").place(x=20, y=100)
    pass_entry = tk.Entry(win, show="*")
    pass_entry.place(x=130, y=100)

    tk.Label(win, text="Şifre (Tekrar):").place(x=20, y=140)
    pass2_entry = tk.Entry(win, show="*")
    pass2_entry.place(x=130, y=140)

    def kayit_et():
        user = user_entry.get().strip()
        email = email_entry.get().strip()
        p1 = pass_entry.get()
        p2 = pass2_entry.get()

        if not user or not p1 or not p2:
            messagebox.showwarning("Hata", "Lütfen tüm alanları doldurun.")
            return
        if p1 != p2:
            messagebox.showwarning("Hata", "Şifreler eşleşmiyor.")
            return
        if user in kullanicilar:
            messagebox.showwarning("Hata", "Bu kullanıcı adı zaten kayıtlı.")
            return

        kullanicilar[user] = {"email": email, "sifre": p1, "bakiye": 0, "games": []}
        messagebox.showinfo("Başarılı", "Kayıt başarılı.")
        win.destroy()

    def on_close():
        open_kayit_window.window_open = False
        win.destroy()

    tk.Button(win, text="Kayıt Ol", command=kayit_et).place(x=130, y=200)
    win.protocol("WM_DELETE_WINDOW", on_close)

def giris_yap():
    global current_user
    user = kullanici_adigiris.get().strip()
    p = sifregiris.get()
    
    if not user or not p:
        messagebox.showwarning("Hata", "Lütfen kullanıcı adı ve şifre girin.")
        return
    if user not in kullanicilar or kullanicilar[user]["sifre"] != p:
        messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış.")
        return
        
    current_user = user
    open_main_menu()

def open_main_menu():
    if current_user is None:
        return
        
    win = tk.Toplevel(arayuz)
    win.title("Ana Menü - " + current_user)
    win.geometry("420x320")

    welcome = tk.Label(win, text=f"Hoşgeldin, {current_user}")
    welcome.place(x=20, y=20)

    bakiye_var = tk.StringVar()
    def update_bakiye():
        bakiye_var.set(f"Bakiye: {kullanicilar[current_user]['bakiye']} ₺")

    update_bakiye()
    bakiye_label = tk.Label(win, textvariable=bakiye_var)
    bakiye_label.place(x=20, y=50)

    # Para Kazanma
    def para_kazan():
        kullanicilar[current_user]['bakiye'] += 50
        update_bakiye()
        messagebox.showinfo("Para Kazanıldı", "Tebrikler! 50 ₺ kazandınız.")

    tk.Button(win, text="1) Para Kazanma (+50₺)", width=30, command=para_kazan).place(x=80, y=90)

    # Yemek Alma
    def open_yemek_window():
        foods = {"Hamburger": 30, "Pizza Dilimi": 45, "Kebap": 60, "Çorba": 20}
        wy = tk.Toplevel(win)
        wy.title("Yemek Al")
        wy.geometry("360x220")

        tk.Label(wy, text="Yemek seçin:").place(x=20, y=20)
        secim_var = tk.StringVar(value=list(foods.keys())[0])
        tk.OptionMenu(wy, secim_var, *foods.keys()).place(x=120, y=15)

        fiyat_var = tk.StringVar()
        def guncelle_fiyat(*args):
            fiyat_var.set(f"Fiyat: {foods[secim_var.get()]} ₺")
        guncelle_fiyat()
        secim_var.trace_add("write", guncelle_fiyat)
        tk.Label(wy, textvariable=fiyat_var).place(x=120, y=50)

        def satin_al():
            fiyat = foods[secim_var.get()]
            if kullanicilar[current_user]['bakiye'] >= fiyat:
                kullanicilar[current_user]['bakiye'] -= fiyat
                update_bakiye()
                messagebox.showinfo("Satın Alındı", f"{secim_var.get()} satın alındı. Kalan bakiye: {kullanicilar[current_user]['bakiye']} ₺")
                wy.destroy()
            else:
                messagebox.showwarning("Yetersiz Bakiye", "Paranız bu ürünü almaya yetmiyor.")

        tk.Button(wy, text="Satın Al", command=satin_al).place(x=140, y=100)

    tk.Button(win, text="2) Yemek Al", width=30, command=open_yemek_window).place(x=80, y=130)

    # Ecip Games
    def open_ecip_window():
        # Önce kayıt/giriş penceresi
        ecip_login = tk.Toplevel(win)
        ecip_login.title("Ecip Games - Giriş")
        ecip_login.geometry("350x300")

        tk.Label(ecip_login, text="Ecip Games'e Hoşgeldiniz").place(x=100, y=20)
        
        # Kayıt Formu
        tk.Label(ecip_login, text="Kullanıcı Adı:").place(x=20, y=60)
        ecip_user = tk.Entry(ecip_login)
        ecip_user.place(x=130, y=60)

        tk.Label(ecip_login, text="E-posta:").place(x=20, y=100)
        ecip_email = tk.Entry(ecip_login)
        ecip_email.place(x=130, y=100)

        tk.Label(ecip_login, text="Şifre:").place(x=20, y=140)
        ecip_pass = tk.Entry(ecip_login, show="*")
        ecip_pass.place(x=130, y=140)

        def show_game_store():
            games = {
                "Ecip Racer": 100,
                "Ecip Quest": 75,
                "Ecip Puzzle": 40,
                "Ecip Battle": 120,
                "Ecip Farm": 55
            }
            
            gw = tk.Toplevel(win)
            gw.title("Ecip Games - Mağaza")
            gw.geometry("420x320")

            tk.Label(gw, text=f"Hoş geldin, {kullanicilar[current_user]['ecip_account']['username']}").place(x=20, y=20)
            
            tk.Label(gw, text="Oyunlar:").place(x=20, y=60)
            y = 90
            
            def make_buy_fn(game, price):
                def buy():
                    if kullanicilar[current_user]['bakiye'] < price:
                        messagebox.showwarning("Yetersiz Bakiye", "Bu oyunu almaya paranız yetmiyor.")
                        return
                    kullanicilar[current_user]['bakiye'] -= price
                    kullanicilar[current_user]['games'].append({
                        "game": game,
                        "ecip_user": kullanicilar[current_user]['ecip_account']['username']
                    })
                    update_bakiye()
                    messagebox.showinfo("Satın Alındı", f"{game} satın alındı ve Ecip hesabına eklendi.")
                return buy

            for game, price in games.items():
                tk.Label(gw, text=f"{game} - {price} ₺").place(x=20, y=y)
                tk.Button(gw, text="Satın Al", command=make_buy_fn(game, price)).place(x=280, y=y-4)
                y += 35

        def ecip_kayit():
            username = ecip_user.get().strip()
            email = ecip_email.get().strip()
            password = ecip_pass.get()

            if not username or not email or not password:
                messagebox.showwarning("Hata", "Lütfen tüm alanları doldurun.")
                return

            kullanicilar[current_user]["ecip_account"] = {
                "username": username,
                "email": email,
                "password": password
            }
            messagebox.showinfo("Başarılı", "Ecip Games hesabınız oluşturuldu!")
            ecip_login.destroy()
            show_game_store()

        def ecip_giris():
            username = ecip_user.get().strip()
            password = ecip_pass.get()

            if "ecip_account" in kullanicilar[current_user]:
                stored = kullanicilar[current_user]["ecip_account"]
                if stored["username"] == username and stored["password"] == password:
                    ecip_login.destroy()
                    show_game_store()
                else:
                    messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış.")
            else:
                messagebox.showinfo("Bilgi", "Hesap bulunamadı. Lütfen kayıt olun.")

        tk.Button(ecip_login, text="Ecip'e Kayıt Ol", command=ecip_kayit).place(x=80, y=200)
        tk.Button(ecip_login, text="Ecip'e Giriş Yap", command=ecip_giris).place(x=180, y=200)

    tk.Button(win, text="3) Ecip Games", width=30, command=open_ecip_window).place(x=80, y=170)

    def cikis():
        global current_user
        win.destroy()
        current_user = None

    tk.Button(win, text="Çıkış (Oturumu Kapat)", command=cikis).place(x=140, y=240)

# Ana pencere butonları
sifre_goster_btn = tk.Button(arayuz, text="Şifre Göster", command=toggle_sifre)
sifre_goster_btn.place(x=250, y=60)

giris_butonu = tk.Button(arayuz, text="Giriş Yap", command=giris_yap)
giris_butonu.place(x=150, y=220)

kayit_butonu = tk.Button(arayuz, text="Kayıt Ol", command=open_kayit_window)
kayit_butonu.place(x=150, y=260)

# Programı başlat
arayuz.mainloop()