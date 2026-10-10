import tkinter as tk
from tkinter import ttk
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

  window.mainloop()

if __name__ == "__main__":
  main()

