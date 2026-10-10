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
  
  status_label = ttk.Label(
    window,
    text="尚未操作",
  )
  status_label.pack(pady=10)

  def on_test_click():
      status_label.config(text="按钮点击成功")
 
  test_button = ttk.Button(
    window,
    text="测试按钮",
    command=on_test_click
  )
  test_button.pack(pady=10)
  window.mainloop()

if __name__ == "__main__":
  main()

