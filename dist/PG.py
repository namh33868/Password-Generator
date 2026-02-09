import random
import string
import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime
import os
from tkcalendar import DateEntry

# File lưu lịch sử
HISTORY_FILE = "password_history.json"

def load_history():
    """Tải lịch sử từ file JSON. Trả về list dict {'password': str, 'time': str}."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history):
    """Lưu lịch sử vào file JSON."""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def generate_password(length=12, use_letters=True, use_digits=True, use_special=True):
    """
    Tạo mật khẩu ngẫu nhiên (giữ nguyên từ trước).
    """
    chars = ""
    if use_letters:
        chars += string.ascii_letters
    if use_digits:
        chars += string.digits
    if use_special:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if not chars:
        return ""
    
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

class HistoryWindow:
    """
    Cửa sổ lịch sử mật khẩu với bảng Treeview và bộ lọc ngày giờ.
    """
    def __init__(self, parent):
        self.history = load_history()
        self.top = tk.Toplevel(parent)
        self.top.title("Lịch sử mật khẩu")
        self.top.geometry("600x500")
        
        # Bộ lọc ngày với DateEntry (lịch chọn ngày)
        filter_frame = tk.Frame(self.top)
        filter_frame.pack(pady=10)
        tk.Label(filter_frame, text="Lọc từ ngày:").pack(side=tk.LEFT)
        self.filter_date = DateEntry(filter_frame, width=12, date_pattern="yyyy-mm-dd")
        self.filter_date.pack(side=tk.LEFT, padx=5)
        filter_btn = tk.Button(filter_frame, text="Lọc", command=self.filter_history)
        filter_btn.pack(side=tk.LEFT, padx=5)
        clear_btn = tk.Button(filter_frame, text="Xóa hết lịch sử", command=self.clear_history)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Bảng Treeview: Thời gian, Mật khẩu, Copy
        columns = ("Thời gian", "Mật khẩu", "Copy")
        self.tree = ttk.Treeview(self.top, columns=columns, show="headings", height=20)
        self.tree.heading("Thời gian", text="Thời gian")
        self.tree.heading("Mật khẩu", text="Mật khẩu")
        self.tree.heading("Copy", text="")
        self.tree.column("Thời gian", width=150)
        self.tree.column("Mật khẩu", width=320)
        self.tree.column("Copy", width=60, anchor="center")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Nút copy mật khẩu đã chọn
        copy_btn = tk.Button(self.top, text="Copy mật khẩu đã chọn", command=self.copy_selected)
        copy_btn.pack(pady=5)

        # Bắt sự kiện click vào cột "Copy" để copy nhanh từng mật khẩu
        self.tree.bind("<Button-1>", self.on_tree_click)
        
        self.show_history()  # Hiển thị ban đầu
        
    def filter_history(self):
        """Lọc lịch sử theo ngày bắt đầu."""
        selected_date = self.filter_date.get_date()
        filtered = []
        for h in self.history:
            try:
                record_dt = datetime.strptime(h["time"], "%Y-%m-%d %H:%M:%S")
                if record_dt.date() >= selected_date:
                    filtered.append(h)
            except Exception:
                # Bỏ qua bản ghi lỗi định dạng
                continue
        self.tree.delete(*self.tree.get_children())
        for item in filtered:
            self.tree.insert("", tk.END, values=(item['time'], item['password'], "Copy"))
    
    def show_history(self):
        """Hiển thị toàn bộ lịch sử, sắp xếp mới nhất trước (đảo ngược list)."""
        self.tree.delete(*self.tree.get_children())
        sorted_history = sorted(self.history, key=lambda x: x['time'], reverse=True)
        for item in sorted_history:
            self.tree.insert("", tk.END, values=(item['time'], item['password'], "Copy"))
    
    def clear_history(self):
        """Xóa toàn bộ lịch sử và cập nhật file."""
        if messagebox.askyesno("Xác nhận", "Xóa hết lịch sử?"):
            self.history = []
            save_history(self.history)
            self.show_history()

    def copy_selected(self):
        """Copy mật khẩu của dòng đang được chọn trong bảng vào clipboard."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Hãy chọn một dòng trong bảng lịch sử!")
            return
        item = self.tree.item(selected[0])
        # values = (time, password, "Copy")
        if len(item["values"]) < 2:
            messagebox.showwarning("Thông báo", "Không tìm thấy mật khẩu ở dòng này!")
            return
        pwd = item["values"][1]
        self.top.clipboard_clear()
        self.top.clipboard_append(pwd)
        self.top.update()  # Đảm bảo clipboard được giữ sau khi đóng cửa sổ
        messagebox.showinfo("Đã copy", "Mật khẩu đã được copy vào clipboard.")

    def on_tree_click(self, event):
        """
        Xử lý click chuột trong Treeview.
        Nếu click vào cột 'Copy' của một dòng thì copy mật khẩu của dòng đó.
        """
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        column = self.tree.identify_column(event.x)  # dạng '#1', '#2', '#3'
        row_id = self.tree.identify_row(event.y)
        if column == "#3" and row_id:  # cột 'Copy'
            item = self.tree.item(row_id)
            if len(item["values"]) >= 2:
                pwd = item["values"][1]
                self.top.clipboard_clear()
                self.top.clipboard_append(pwd)
                self.top.update()
                messagebox.showinfo("Đã copy", "Mật khẩu đã được copy vào clipboard.")
            return "break"

class PasswordGeneratorApp:
    """
    App chính với nút Lưu và Xem lịch sử.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator Pro")
        self.root.geometry("350x350")
        
        # Các phần input giống cũ
        tk.Label(root, text="Độ dài:").pack(pady=10)
        self.length_var = tk.StringVar(value="12")
        tk.Entry(root, textvariable=self.length_var).pack()
        
        self.letters_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Chữ cái", variable=self.letters_var).pack(anchor="w", padx=20)
        self.digits_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Số", variable=self.digits_var).pack(anchor="w", padx=20)
        self.special_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Đặc biệt", variable=self.special_var).pack(anchor="w", padx=20)
        
        # Nút tạo
        tk.Button(root, text="Tạo", command=self.on_generate, bg="lightgreen").pack(pady=10)
        
        # Khung hiển thị mật khẩu hiện tại + nút copy
        current_frame = tk.Frame(root)
        current_frame.pack(pady=20)
        self.current_pwd_label = tk.Label(current_frame, text="Chưa tạo", fg="red", font=("Arial", 14))
        self.current_pwd_label.pack(side=tk.LEFT, padx=5)
        self.copy_current_btn = tk.Button(current_frame, text="Copy", command=self.copy_current_password, state=tk.DISABLED)
        self.copy_current_btn.pack(side=tk.LEFT, padx=5)
        
        # Nút Lưu và Lịch sử
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        self.save_btn = tk.Button(btn_frame, text="Lưu mật khẩu", command=self.save_password, state=tk.DISABLED, bg="orange")
        self.save_btn.pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Xem lịch sử", command=self.show_history).pack(side=tk.LEFT, padx=5)

        # Gợi ý xem clipboard ở dưới cùng
        hint_label = tk.Label(root, text="Bấm Win + V để xem clipboard", fg="green")
        hint_label.pack(pady=5, side=tk.BOTTOM)
    
    def on_generate(self):
        """Tạo và hiển thị mật khẩu."""
        try:
            length = int(self.length_var.get())
            pwd = generate_password(length, self.letters_var.get(), self.digits_var.get(), self.special_var.get())
            if pwd:
                self.current_pwd_label.config(text=pwd, fg="green")
                self.save_btn.config(state=tk.NORMAL)  # Kích hoạt nút lưu
                self.current_password = pwd  # Lưu tạm để nút lưu dùng
                self.copy_current_btn.config(state=tk.NORMAL)  # Cho phép copy nhanh
            else:
                messagebox.showerror("Lỗi", "Chọn ít nhất một loại!")
        except ValueError:
            messagebox.showerror("Lỗi", "Độ dài phải là số!")
    
    def save_password(self):
        """Lưu mật khẩu hiện tại vào lịch sử với timestamp."""
        history = load_history()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Định dạng ngày giờ
        history.append({"password": self.current_password, "time": timestamp})
        save_history(history)
        messagebox.showinfo("Thành công", "Đã lưu mật khẩu!")
        self.save_btn.config(state=tk.DISABLED)  # Vô hiệu hóa sau lưu
    
    def copy_current_password(self):
        """Copy mật khẩu hiện tại đang hiển thị vào clipboard."""
        if not hasattr(self, "current_password"):
            messagebox.showwarning("Thông báo", "Chưa có mật khẩu để copy!")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.current_password)
        self.root.update()
        messagebox.showinfo("Đã copy", "Mật khẩu hiện tại đã được copy vào clipboard. Có thể bấm Win + v để xem clipboard.")
    
    def show_history(self):
        """Mở cửa sổ lịch sử."""
        HistoryWindow(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
