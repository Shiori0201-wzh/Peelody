from pathlib import Path
import tkinter as tk
from tkinter import ttk,filedialog
  
def main():
  window = tk.Tk()
  window.title("Peelody V1.1")
  window.geometry("500x320")
  title_label = ttk.Label(
    window,
    text="Peelody Audio Separator",
    font=("Segoe UI", 22, "bold")
  )
  title_label.pack(pady=35)
  
  status_label = ttk.Label(
    window,
    text="尚未操作",
  )
  status_label.pack(pady=10)

  def choose_audio():
    audio_path = filedialog.askopenfilename(
       parent=window,
       title="选择音频文件",
       filetypes=[("音频文件"，"*.wav*.mp3")]
    )

    if audio_path:
        status_label.config(text=Path(audio_path).name)
    
  ttk_button = ttk.Button(
    window,
    text="选择音频",
    command=choose_audio
  )
  test_button.pack(pady=10)
  window.mainloop()

if __name__ == "__main__":
  main()
