import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

def select_video():
    path = filedialog.askopenfilename(filetypes=[
        ("Video files", "*.mp4 *.mov *.avi *.mkv *.cmfv"),
        ("All files", "*.*")
    ])
    if path:
        video_path.set(path)

def select_audio():
    path = filedialog.askopenfilename(filetypes=[
        ("Audio files", "*.mp3 *.wav *.aac *.cmfa"),
        ("All files", "*.*")
    ])
    if path:
        audio_path.set(path)

def merge_files():
    video = video_path.get()
    audio = audio_path.get()

    if not video or not audio:
        messagebox.showerror("Missing Files", "Please select both a video and audio file.")
        return

    output = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
    if not output:
        return

    cmd = [
        "ffmpeg",
        "-i", video,
        "-i", audio,
        "-c:v", "copy",
        "-c:a", "aac",
        "-strict", "-2",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        output
    ]

    try:
        subprocess.run(cmd, check=True)
        messagebox.showinfo("Success", f"Merged saved as:\n{output}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"FFmpeg failed:\n{e}")

# GUI Setup
root = tk.Tk()
root.title("Video + Audio Merger")
root.geometry("400x250")
root.resizable(False, False)

video_path = tk.StringVar()
audio_path = tk.StringVar()

tk.Label(root, text="Select Video File:").pack(pady=(10, 0))
tk.Entry(root, textvariable=video_path, width=50).pack()
tk.Button(root, text="Browse Video", command=select_video).pack(pady=5)

tk.Label(root, text="Select Audio File:").pack(pady=(10, 0))
tk.Entry(root, textvariable=audio_path, width=50).pack()
tk.Button(root, text="Browse Audio", command=select_audio).pack(pady=5)

tk.Button(root, text="Merge!", command=merge_files, bg="#4CAF50", fg="white", height=2, width=20).pack(pady=20)

root.mainloop()
