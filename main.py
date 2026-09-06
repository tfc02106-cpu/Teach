
import os
import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# 引入協作同學負責編寫的邊緣強化模組
import processor

class ImageEnhanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("刻度影像邊緣強化系統")
        self.root.geometry("820x460")

        self.image_path = "TAP.jpg"
        self.current_display = None

        # 頂部操作按鈕區
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=10)

        # 協作功能按鈕：點擊後執行同學寫的函式
        self.run_btn = tk.Button(
            self.btn_frame,
            text="執行邊緣強化 (由協作同學實作)",
            command=self.handle_processing,
            font=("Arial", 12, "bold"),
            bg="#2ea44f",
            fg="white",
            padx=10,
            pady=5
        )
        self.run_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(
            self.btn_frame,
            text="還原原始影像",
            command=self.load_original_image,
            font=("Arial", 12),
            padx=10,
            pady=5
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)

        # 影像顯示區
        self.display_label = tk.Label(root, text="載入影像中...", bg="#e0e0e0")
        self.display_label.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.load_original_image()

    def update_canvas(self, bgr_or_gray_img):
        """將 OpenCV 影像轉換為 Tkinter PhotoImage 並更新畫面"""
        if len(bgr_or_gray_img.shape) == 2:
            rgb_img = cv2.cvtColor(bgr_or_gray_img, cv2.COLOR_GRAY2RGB)
        else:
            rgb_img = cv2.cvtColor(bgr_or_gray_img, cv2.COLOR_BGR2RGB)

        pil_img = Image.fromarray(rgb_img)
        # 依視窗比例縮放顯示
        pil_img.thumbnail((780, 360))
        self.current_display = ImageTk.PhotoImage(pil_img)
        self.display_label.config(image=self.current_display, text="")

    def load_original_image(self):
        if not os.path.exists(self.image_path):
            messagebox.showerror("錯誤", f"找不到測試影像檔：{self.image_path}")
            return
        img = cv2.imread(self.image_path)
        self.update_canvas(img)

    def handle_processing(self):
        """呼叫同學的演算法，並將回傳結果更新到畫面上"""
        if not os.path.exists(self.image_path):
            return
        
        input_img = cv2.imread(self.image_path)
        
        # 執行同學寫的邊緣強化函式
        try:
            result_img = processor.enhance_edges(input_img)
            self.update_canvas(result_img)
        except NotImplementedError as e:
            messagebox.showwarning("提示", str(e))
        except Exception as e:
            messagebox.showerror("錯誤", f"處理失敗：{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEnhanceApp(root)
    root.mainloop()
