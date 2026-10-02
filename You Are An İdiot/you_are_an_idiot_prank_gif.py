import os
import random
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import pygame

# ==========================================================
# YOU ARE AN IDIOT - SAFE PRANK
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------
# KLASÖRLER / DOSYALAR
# ----------------------------------------------------------

GIF_DIR = os.path.join(
    BASE_DIR,
    "Assets",
    "Gifs"
)

SOUND_DIR = os.path.join(
    BASE_DIR,
    "Assets",
    "Sounds"
)

MAIN_SOUND_FILE = os.path.join(
    SOUND_DIR,
    "you-are-an-idiot.wav"
)

ERROR_SOUND_FILE = os.path.join(
    SOUND_DIR,
    "error.wav"
)

# ==========================================================
# AYARLAR
# ==========================================================

MAX_WINDOWS = 100

WINDOW_W = 360
WINDOW_H = 260

# Yeni pencere açma aralığı
SPAWN_DELAY = 120

# Ortak güncelleme hızı
UPDATE_DELAY = 35

# GIF frame değiştirme aralığı
GIF_EVERY = 2

# Hareket hızı
MOVE_SPEED_MIN = 7
MOVE_SPEED_MAX = 14

# ==========================================================
# GIFLERİ BUL
# ==========================================================

if not os.path.isdir(GIF_DIR):
    print()
    print("HATA: GIF klasörü bulunamadı!")
    print()
    print(GIF_DIR)
    print()
    input("Enter'a bas...")
    raise SystemExit

gif_files = []

for filename in os.listdir(GIF_DIR):

    if filename.lower().endswith(".gif"):

        full_path = os.path.join(
            GIF_DIR,
            filename
        )

        gif_files.append(full_path)

# ==========================================================
# DOSYALARI KONTROL ET
# ==========================================================

if not gif_files:

    print()
    print("HATA: Assets/Gifs içinde hiç GIF yok!")
    print()
    input("Enter'a bas...")
    raise SystemExit


if not os.path.isfile(MAIN_SOUND_FILE):

    print()
    print("HATA: Ana ses bulunamadı!")
    print()
    print(MAIN_SOUND_FILE)
    print()
    input("Enter'a bas...")
    raise SystemExit


if not os.path.isfile(ERROR_SOUND_FILE):

    print()
    print("HATA: error.wav bulunamadı!")
    print()
    print(ERROR_SOUND_FILE)
    print()
    input("Enter'a bas...")
    raise SystemExit

# ==========================================================
# BİLGİ
# ==========================================================

print()
print("==========================================")
print("       YOU ARE AN IDIOT SAFE PRANK")
print("==========================================")
print()
print("Bulunan GIF sayısı:", len(gif_files))
print()

for gif in gif_files:
    print("GIF:", os.path.basename(gif))

print()
print("Ana ses:", os.path.basename(MAIN_SOUND_FILE))
print("Hata sesi:", os.path.basename(ERROR_SOUND_FILE))
print()
print("ESC = ÇIKIŞ")
print()

# ==========================================================
# PYGAME SES
# ==========================================================

pygame.mixer.init()

# Aynı anda birden fazla error.wav çalabilsin
pygame.mixer.set_num_channels(32)

# Ana ses
pygame.mixer.music.load(
    MAIN_SOUND_FILE
)

pygame.mixer.music.play(-1)

# Error sesi
error_sound = pygame.mixer.Sound(
    ERROR_SOUND_FILE
)

# ==========================================================
# TKINTER
# ==========================================================

root = tk.Tk()
root.withdraw()

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

running = True

# Tüm pencere bilgileri
prank_windows = []

# Son kullanılan GIF
last_gif = None

# GIF cache
gif_cache = {}

# Ortak sayaç
global_tick = 0

# ==========================================================
# RAINBOW ARKA PLAN
# ==========================================================

rainbow = tk.Toplevel(root)

rainbow.overrideredirect(True)

rainbow.geometry(
    f"{screen_w}x{screen_h}+0+0"
)

rainbow.configure(
    bg="#ff0000"
)

rainbow.attributes(
    "-topmost",
    True
)

rainbow_colors = [
    "#ff0000",
    "#ff3300",
    "#ff6600",
    "#ff9900",
    "#ffff00",
    "#99ff00",
    "#00ff00",
    "#00ff99",
    "#00ffff",
    "#0099ff",
    "#0000ff",
    "#6600ff",
    "#9900ff",
    "#ff00ff",
    "#ff0099"
]

rainbow_index = 0


def update_rainbow():

    global rainbow_index

    if not running:
        return

    try:

        rainbow.configure(
            bg=rainbow_colors[rainbow_index]
        )

        rainbow_index = (
            rainbow_index + 1
        ) % len(rainbow_colors)

    except tk.TclError:
        return

# ==========================================================
# GIF YÜKLEME
# ==========================================================

def load_gif(path):

    # Cache varsa tekrar yükleme
    if path in gif_cache:
        return gif_cache[path]

    try:

        image = Image.open(path)

        frames = []

        for frame in ImageSequence.Iterator(image):

            frame = frame.convert("RGB")

            frame.thumbnail(
                (
                    WINDOW_W - 10,
                    WINDOW_H - 35
                )
            )

            photo = ImageTk.PhotoImage(
                frame
            )

            frames.append(photo)

        if not frames:
            return None

        gif_cache[path] = frames

        return frames

    except Exception as error:

        print()
        print("GIF yükleme hatası:")
        print(path)
        print(error)
        print()

        return None

# ==========================================================
# RASTGELE GIF
# ==========================================================

def choose_gif():

    global last_gif

    # Aynı GIF arka arkaya gelmesin
    choices = [
        gif
        for gif in gif_files
        if gif != last_gif
    ]

    if not choices:
        choices = gif_files

    selected = random.choice(
        choices
    )

    last_gif = selected

    return selected

# ==========================================================
# ERROR SESİ
# ==========================================================

def play_error_sound():

    try:

        # Boş kanal bulmaya çalış
        channel = pygame.mixer.find_channel(
            True
        )

        if channel:

            channel.play(
                error_sound
            )

    except Exception as error:

        print(
            "error.wav çalınamadı:",
            error
        )

# ==========================================================
# YENİ PENCERE
# ==========================================================

def create_window():

    if not running:
        return

    if len(prank_windows) >= MAX_WINDOWS:
        return

    # ------------------------------------------------------
    # GIF
    # ------------------------------------------------------

    selected_gif = choose_gif()

    frames = load_gif(
        selected_gif
    )

    if not frames:
        return

    # ------------------------------------------------------
    # RASTGELE KONUM
    # ------------------------------------------------------

    x = random.randint(
        0,
        max(0, screen_w - WINDOW_W)
    )

    y = random.randint(
        0,
        max(0, screen_h - WINDOW_H)
    )

    # ------------------------------------------------------
    # HIZ
    # ------------------------------------------------------

    dx = random.choice([
        random.randint(
            MOVE_SPEED_MIN,
            MOVE_SPEED_MAX
        ),
        -random.randint(
            MOVE_SPEED_MIN,
            MOVE_SPEED_MAX
        )
    ])

    dy = random.choice([
        random.randint(
            MOVE_SPEED_MIN,
            MOVE_SPEED_MAX
        ),
        -random.randint(
            MOVE_SPEED_MIN,
            MOVE_SPEED_MAX
        )
    ])

    # ------------------------------------------------------
    # PENCERE
    # ------------------------------------------------------

    win = tk.Toplevel(root)

    win.title(
        "YOU ARE AN IDIOT!"
    )

    win.configure(
        bg="black"
    )

    win.geometry(
        f"{WINDOW_W}x{WINDOW_H}+"
        f"{x}+{y}"
    )

    win.attributes(
        "-topmost",
        True
    )

    # ------------------------------------------------------
    # GIF
    # ------------------------------------------------------

    label = tk.Label(
        win,
        bg="black"
    )

    label.pack(
        fill="both",
        expand=True
    )

    label.configure(
        image=frames[0]
    )

    # ------------------------------------------------------
    # LİSTEYE EKLE
    # ------------------------------------------------------

    item = {
        "window": win,
        "label": label,
        "frames": frames,
        "frame": 0,
        "x": x,
        "y": y,
        "dx": dx,
        "dy": dy
    }

    prank_windows.append(
        item
    )

    # ------------------------------------------------------
    # ERROR SESİ
    # ------------------------------------------------------

    play_error_sound()

    # ------------------------------------------------------
    # KONSOLA BİLGİ
    # ------------------------------------------------------

    print(
        f"[{len(prank_windows):03d}/{MAX_WINDOWS}]",
        "Açıldı:",
        os.path.basename(selected_gif)
    )

# ==========================================================
# TÜM PENCERELERİ GÜNCELLE
# ==========================================================

def update_all():

    global global_tick

    if not running:
        return

    global_tick += 1

    # ------------------------------------------------------
    # RAINBOW
    # ------------------------------------------------------

    if global_tick % 2 == 0:
        update_rainbow()

    # ------------------------------------------------------
    # GIF FRAME
    # ------------------------------------------------------

    change_frame = (
        global_tick % GIF_EVERY == 0
    )

    # ------------------------------------------------------
    # PENCERELER
    # ------------------------------------------------------

    for item in prank_windows:

        try:

            win = item["window"]

            # ==============================================
            # HAREKET
            # ==============================================

            item["x"] += item["dx"]
            item["y"] += item["dy"]

            # Sol / sağ
            if item["x"] <= 0:

                item["x"] = 0

                item["dx"] = abs(
                    item["dx"]
                )

            elif (
                item["x"] + WINDOW_W
                >= screen_w
            ):

                item["x"] = (
                    screen_w - WINDOW_W
                )

                item["dx"] = -abs(
                    item["dx"]
                )

            # Üst / alt
            if item["y"] <= 0:

                item["y"] = 0

                item["dy"] = abs(
                    item["dy"]
                )

            elif (
                item["y"] + WINDOW_H
                >= screen_h
            ):

                item["y"] = (
                    screen_h - WINDOW_H
                )

                item["dy"] = -abs(
                    item["dy"]
                )

            # Konumu güncelle
            win.geometry(
                f"{WINDOW_W}x{WINDOW_H}+"
                f"{int(item['x'])}+"
                f"{int(item['y'])}"
            )

            # ==============================================
            # GIF
            # ==============================================

            if change_frame:

                frames = item["frames"]

                if len(frames) > 1:

                    item["frame"] = (
                        item["frame"] + 1
                    ) % len(frames)

                    item["label"].configure(
                        image=frames[
                            item["frame"]
                        ]
                    )

        except tk.TclError:

            pass

    # ------------------------------------------------------
    # BİR SONRAKİ GÜNCELLEME
    # ------------------------------------------------------

    root.after(
        UPDATE_DELAY,
        update_all
    )

# ==========================================================
# PENCERELERİ KADEMELİ AÇ
# ==========================================================

def spawn_windows():

    if not running:
        return

    if len(prank_windows) >= MAX_WINDOWS:
        return

    create_window()

    root.after(
        SPAWN_DELAY,
        spawn_windows
    )

# ==========================================================
# PROGRAMI KAPAT
# ==========================================================

def stop_prank(event=None):

    global running

    if not running:
        return

    running = False

    # ------------------------------------------------------
    # SES
    # ------------------------------------------------------

    try:

        pygame.mixer.music.stop()

        pygame.mixer.quit()

    except:
        pass

    # ------------------------------------------------------
    # RAINBOW
    # ------------------------------------------------------

    try:

        rainbow.destroy()

    except:
        pass

    # ------------------------------------------------------
    # PENCERELER
    # ------------------------------------------------------

    for item in prank_windows:

        try:

            item["window"].destroy()

        except:
            pass

    # ------------------------------------------------------
    # ROOT
    # ------------------------------------------------------

    try:

        root.destroy()

    except:
        pass

# ==========================================================
# ESC = ACİL ÇIKIŞ
# ==========================================================

root.bind_all(
    "<Escape>",
    stop_prank
)

# ==========================================================
# BAŞLAT
# ==========================================================

root.after(
    1000,
    spawn_windows
)

root.after(
    1000,
    update_all
)

root.mainloop()