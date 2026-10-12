from peelody import validate_input
from pathlib import Path
import tkinter as tk
from tkinter import ttk,filedialog
import threading
import time
from queue import Queue,Empty
  
def main():
  window = tk.Tk()
  window.title("Peelody V1.1")
  window.geometry("500x420")
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

  selected_audio_path = tk.StringVar(value="")
  
  def choose_audio():
    audio_path = filedialog.askopenfilename(
       parent=window,
       title="选择音频文件",
       filetypes=[
         ("音频文件",("*.wav","*.mp3")),
         ("所有文件","*.*")
       ]
    )

    if audio_path:
      selected_audio_path.set(audio_path)
      status_label.config(text=Path(audio_path).name)
    
  ttk_button = ttk.Button(
    window,
    text="选择音频",
    command=choose_audio
  )
  ttk_button.pack(pady=10)

  def prepare_separation():
    audio_arg = selected_audio_path.get()
    if not audio_arg:
      status_label.config(text="请先选择音频")
      return
    try:
      input_path = validate_input(audio_arg)
    except(FileNotFoundError,ValueError) as error:
      status_label.config(text=f"Error:{error}")
    else:
      status_label.config(text=f"输入检查通过:{input_path.name}")

  check_button = ttk.Button(
    window,
    text="检查输入",
    command=prepare_separation
  )
  check_button.pack(pady=10)
  
  task_queue = Queue()
  task_label = ttk.Label(window,text="模拟任务未开始")
  task_label.pack(pady=8)
  def worker(input_path):
    time.sleep(3)
    task_queue.put(("success",f"模拟完成:{input_path.name}"))
  def check_task():
    try:
      result_type,message = task_queue.get_nowait()
    except Empty:
      window.after(100,check_task)
      return
    if result_type=="success":
      task_label.config(text=message)
    elif result_type=="error":
      task_label.config(text=f"任务失败:{message}")
    demo_button.config(state="normal")

  def start_demo():
    audio_arg = selected_audio_path.get()
    if not audio_arg:
      task_label.config(text="未选择音频")
      return
    try:
      input_path = validate_input(audio_arg)
    except (FileNotFoundError,ValueError) as error:
      task_label.config(text=f"Error: {error}")
      return
    demo_button.config(state="disabled")
    task_label.config(text="模拟任务运行中...")
    threading.Thread(
      target=worker,
      args=(input_path,),
      daemon=True
    ).start()
    window.after(100,check_task)

  demo_button = ttk.Button(
    window,
    text="模拟耗时任务",
    command=start_demo
  )
  demo_button.pack(pady=8)
  
  window.mainloop()

if __name__ == "__main__":
  main()
