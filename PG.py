import random
import string
import tkinter as tk
from tkinter import messagebox, ttk  # Import thêm cho GUI và messagebox

def generate_password(length=12, use_letters=True, use_digits=True, use_special=True):
    """
    Tạo mật khẩu ngẫu nhiên dựa trên các tùy chọn.
    
    Args:
        length (int): Độ dài mật khẩu (mặc định 12).
        use_letters (bool): Bao gồm chữ cái thường/hoa (a-z, A-Z).
        use_digits (bool): Bao gồm số (0-9).
        use_special (bool): Bao gồm ký tự đặc biệt (!@#$%^&*).
    
    Returns:
        str: Mật khẩu được tạo hoặc chuỗi rỗng nếu lỗi.
    
    Lưu ý: Sử dụng string module để lấy bộ ký tự an toàn.
    """
    chars = ""
    if use_letters:
        chars += string.ascii_letters  # Tất cả chữ cái: a-z và A-Z
    if use_digits:
        chars += string.digits  # Số từ 0-9
    if use_special:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"  # Ký tự đặc biệt phổ biến, tránh một số gây lỗi
    
    if not chars:
        return ""  # Không có ký tự nào được chọn
    
    # Tạo mật khẩu bằng cách chọn ngẫu nhiên từng ký tự
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

class PasswordGeneratorApp:
    """
    Ứng dụng GUI sử dụng Tkinter để tạo mật khẩu.
    Giao diện đơn giản với input, checkbox và button.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")  # Tiêu đề cửa sổ
        self.root.geometry("400x300")  # Kích thước cửa sổ
        
        # Label và Entry cho độ dài
        tk.Label(root, text="Độ dài mật khẩu:").pack(pady=10)
        self.length_var = tk.StringVar(value="12")
        length_entry = tk.Entry(root, textvariable=self.length_var, width=10)
        length_entry.pack()
        
        # Checkbox cho tùy chọn ký tự
        self.letters_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Chữ cái (a-z, A-Z)", variable=self.letters_var).pack(anchor="w", padx=20)
        
        self.digits_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Số (0-9)", variable=self.digits_var).pack(anchor="w", padx=20)
        
        self.special_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Ký tự đặc biệt", variable=self.special_var).pack(anchor="w", padx=20)
        
        # Nút tạo mật khẩu
        generate_btn = tk.Button(root, text="Tạo mật khẩu", command=self.on_generate, bg="lightblue")
        generate_btn.pack(pady=20)
        
        # Khu vực hiển thị mật khẩu
        self.result_label = tk.Label(root, text="Mật khẩu sẽ hiển thị ở đây", fg="blue", font=("Arial", 12))
        self.result_label.pack(pady=10)
    
    def on_generate(self):
        """Xử lý sự kiện khi nhấn nút Tạo."""
        try:
            length = int(self.length_var.get())  # Lấy độ dài từ input
            pwd = generate_password(
                length,
                self.letters_var.get(),
                self.digits_var.get(),
                self.special_var.get()
            )
            if pwd:
                self.result_label.config(text=pwd)  # Hiển thị mật khẩu
            else:
                messagebox.showerror("Lỗi", "Chọn ít nhất một loại ký tự!")  # Thông báo lỗi
        except ValueError:
            messagebox.showerror("Lỗi", "Độ dài phải là số!")  # Xử lý input không hợp lệ

if __name__ == "__main__":
    root = tk.Tk()  # Tạo cửa sổ chính
    app = PasswordGeneratorApp(root)
    root.mainloop()  # Chạy vòng lặp GUI
