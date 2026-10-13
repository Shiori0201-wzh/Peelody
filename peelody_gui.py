from peelody import validate_input,run_separation
from pathlib import Path
import tkinter as tk
from tkinter import ttk,filedialog,messagebox
import threading
import time
from queue import Queue,Empty
  
def main():
  window = tk.Tk()
  window.title("Peelody V1.1")
  window.geometry("580x540")
  title_label = ttk.Label(
    window,
    text="Peelody Audio Separator",
    font=("Segoe UI", 22, "bold"),
  )
  title_label.pack(pady=35)
  
  status_label = ttk.Label(
    window,
    text="尚未操作",
  )
  status_label.pack(pady=10)

  selected_audio_path = tk.StringVar(value="")
  selected_output_dir = tk.StringVar(value="")
  task_running = tk.BooleanVar(value=False)
  
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

  output_label = ttk.Label(
    window,
    text="输出目录：默认 outputs",
    wraplength=430
  )
  output_label.pack(pady=5)

  def choose_output_dir():
    folder = filedialog.askdirectory(
      parent=window,
      title="选择输出目录"
    )
    
    if folder:
      selected_output_dir.set(folder)
      output_label.config(text=f"输出目录：{folder}")

  output_button=ttk.Button(
    window,
    text="选择输出目录",
    command=choose_output_dir
  )
  output_button.pack(pady=5)

  def restore_default_output():
    selected_output_dir.set("")
    output_label.config(text="输出目录：默认outputs")

  reset_output_button=ttk.Button(
    window,
    text="恢复默认",
    command=restore_default_output
  )
  reset_output_button.pack(pady=5)
  
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
  task_label = ttk.Label(
    window,
    text="模拟任务未开始",
    wraplength=430,
    justify="center"
  )
  task_label.pack(pady=8)
  
  def worker(input_path,custom_output_dir):
    try:
      result_dir = run_separation(input_path,custom_output_dir)
    except Exception as error:
      task_queue.put(("error",str(error)))
    else:
      task_queue.put(("success",str(result_dir)))
      
  def check_task():
    try:
      result_type,message = task_queue.get_nowait()
    except Empty:
      window.after(100,check_task)
      return
    if result_type=="success":
      task_label.config(text=f"分离完成 输出目录为:{message}")
    elif result_type=="error":
      task_label.config(text=f"分离失败:{message}")
    task_running.set(False)
    
    ttk_button.config(state="normal")
    check_button.config(state="normal")
    demo_button.config(state="normal")
    output_button.config(state="normal")
    reset_output_button.config(state="normal")

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
    output_text = selected_output_dir.get()

    if output_text:
      custom_output_dir = Path(output_text)
    else:
      custom_output_dir = None
    
    task_running.set(True)
    
    ttk_button.config(state="disabled")
    check_button.config(state="disabled")
    demo_button.config(state="disabled")
    output_button.config(state="disabled")
    reset_output_button.config(state="disabled")
    
    task_label.config(text="正在分离音频...")
    
    threading.Thread(
      target=worker,
      args=(input_path,custom_output_dir),
      daemon=False
    ).start()
    
    window.after(100,check_task)
  
  demo_button = ttk.Button(
    window,
    text="开始分离",
    command=start_demo
  )
  demo_button.pack(pady=8)

  def on_close():
    if task_running.get():
      messagebox.showwarning(
        "任务运行中",
        "请等待当前任务完成后再关闭窗口。",
        parent=window
      )
      return
    window.destroy()
  window.protocol("WM_DELETE_WINDOW",on_close)
  window.mainloop()

if __name__ == "__main__":
  main()
