import os
import tkinter as tk
import pathlib
from tkinter import filedialog, messagebox
from pdf2image import convert_from_path
from PIL import Image
from tkinter import ttk

def convert_pdf_to_images(pdf_path, output_folder, merge_pages, output_to_folder, progress_var, current_file_var):
    try:
        folder = pathlib.Path(__file__).parent.resolve()
        print(f'{folder}/poppler/Library/bin')
        images = convert_from_path(pdf_path, poppler_path=f'{folder}/poppler/Library/bin')
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]

        if merge_pages and len(images) > 1:
            # 如果合并选项被勾选，将所有图片合并到一个文件中
            merged_image = Image.new('RGB', (images[0].width, images[0].height * len(images)))
            for i, image in enumerate(images):
                merged_image.paste(image, (0, i * images[0].height))

            merged_image.save(os.path.join(output_folder, f"{base_name}.jpg"), "JPEG")
        else:
            # 否则，根据输出到文件夹的选项进行处理
            if output_to_folder:
                output_folder = os.path.join(output_folder, f"{base_name}_images")
                os.makedirs(output_folder, exist_ok=True)

                for i, image in enumerate(images):
                    page_name = f"{base_name}.jpg" if len(images) == 1 else f"{base_name}_{i + 1}.jpg"
                    image.save(os.path.join(output_folder, page_name), "JPEG")
            else:
                for i, image in enumerate(images):
                    page_name = f"{base_name}.jpg" if len(images) == 1 else f"{base_name}_{i + 1}.jpg"
                    image.save(os.path.join(output_folder, page_name), "JPEG")

        return True
    except Exception as e:
        messagebox.showerror("错误", f"处理 {pdf_path} 时发生错误：{str(e)}")
        return False

def select_pdf_files():
    files = filedialog.askopenfilenames(filetypes=[("PDF文件", "*.pdf")])
    entry_pdf_path.delete(0, tk.END)
    entry_pdf_path.insert(0, ', '.join(files))

def select_output_folder():
    folder_path = filedialog.askdirectory()
    entry_output_folder.delete(0, tk.END)
    entry_output_folder.insert(0, folder_path)

def convert_pdfs():
    pdf_paths = entry_pdf_path.get().split(', ')
    output_folder = entry_output_folder.get()
    merge_pages = var_merge_pages.get()
    output_to_folder = var_output_to_folder.get()

    if not pdf_paths or not output_folder:
        messagebox.showerror("错误", "请选择PDF文件和输出文件夹。")
        return

    total_files = len(pdf_paths)
    success_count = 0
    failure_count = 0

    progress_window = tk.Toplevel(root)
    progress_window.title("转换进度")
    progress_window.geometry("300x100")

    progress_label = tk.Label(progress_window, text="正在处理第 1 个文件...")
    progress_label.pack(pady=10)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(progress_window, variable=progress_var, maximum=total_files * 100)
    progress_bar.pack(pady=5)

    for i, pdf_path in enumerate(pdf_paths, start=1):
        current_file_var = tk.StringVar()
        current_file_var.set(i)
        progress_label.config(text=f"正在处理第 {current_file_var.get()} 个文件...")

        if convert_pdf_to_images(pdf_path, output_folder, merge_pages, output_to_folder, progress_var, current_file_var):
            success_count += 1
        else:
            failure_count += 1

        progress_var.set(i * 100)
        root.update_idletasks()

    progress_window.destroy()

    messagebox.showinfo("完成", f"共计 {total_files} 个PDF文件，{success_count} 个成功，{failure_count} 个失败。")

# GUI设置
root = tk.Tk()
root.title("PDF转JPG转换器 by owen")

# PDF文件输入
label_pdf_path = tk.Label(root, text="PDF文件:")
label_pdf_path.grid(row=0, column=0, padx=10, pady=5)
entry_pdf_path = tk.Entry(root, width=50)
entry_pdf_path.grid(row=0, column=1, padx=10, pady=5)
btn_select_pdf = tk.Button(root, text="选择PDF文件", command=select_pdf_files)
btn_select_pdf.grid(row=0, column=2, padx=10, pady=5)

# 输出文件夹输入
label_output_folder = tk.Label(root, text="输出文件夹:")
label_output_folder.grid(row=1, column=0, padx=10, pady=5)
entry_output_folder = tk.Entry(root, width=50)
entry_output_folder.grid(row=1, column=1, padx=10, pady=5)
btn_select_output = tk.Button(root, text="选择文件夹", command=select_output_folder)
btn_select_output.grid(row=1, column=2, padx=10, pady=5)

# 合并选项
var_merge_pages = tk.BooleanVar(value=False)
chk_merge_pages = tk.Checkbutton(root, text="合并页面", variable=var_merge_pages)
chk_merge_pages.grid(row=2, column=0, pady=5)

# 输出到新建文件夹选项
var_output_to_folder = tk.BooleanVar(value=False)
chk_output_to_folder = tk.Checkbutton(root, text="输出到新建文件夹", variable=var_output_to_folder)
chk_output_to_folder.grid(row=2, column=1, pady=5)

# 转换按钮
btn_convert = tk.Button(root, text="转换为JPG", command=convert_pdfs)
btn_convert.grid(row=3, column=1, pady=10)

# 运行GUI
root.mainloop()
