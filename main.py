import os
import time
import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# 引入協作同學負責編寫的邊緣強化模組
import processor

class ImageEnhanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("刻度影像邊緣強化系統 - 多人演算法效能評測")
        self.root.geometry("860x540")

        self.image_path = "TAP.jpg"
        self.current_display = None

        # 頂部控制與設定區
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=10)

        # 演算法選擇下拉選單
        tk.Label(self.control_frame, text="選擇協作者演算法:", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        self.algo_combobox = ttk.Combobox(
            self.control_frame,
            values=[
                "預設演算法 (processor.enhance_edges)",
                "同學 A: Unsharp Masking",
                "同學 B: Laplacian 高通濾波",
                "同學 C: Sobel 梯度強化"
            ],
            state="readonly",
            width=32,
            font=("Arial", 10)
        )
        self.algo_combobox.current(0)
        self.algo_combobox.pack(side=tk.LEFT, padx=5)

        # 執行按鈕
        self.run_btn = tk.Button(
            self.control_frame,
            text="🚀 執行評測並計時",
            command=self.handle_processing,
            font=("Arial", 11, "bold"),
            bg="#2ea44f",
            fg="white",
            padx=10,
            pady=3
        )
        self.run_btn.pack(side=tk.LEFT, padx=5)

        # 還原原圖按鈕
        self.reset_btn = tk.Button(
            self.control_frame,
            text="還原原圖",
            command=self.load_original_image,
            font=("Arial", 11),
            padx=8,
            pady=3
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)

        # 狀態與耗時顯示看板
        self.status_label = tk.Label(
            root,
            text="尚未執行運算",
            font=("Consolas", 11, "bold"),
            fg="#0969da",
            bg="#f6f8fa",
            relief=tk.RIDGE,
            padx=10,
            pady=4
        )
        self.status_label.pack(fill=tk.X, padx=20, pady=5)

        # 影像顯示區
        self.display_label = tk.Label(root, text="載入影像中...", bg="#e0e0e0")
        self.display_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.load_original_image()

    def update_canvas(self, bgr_or_gray_img):
        """將 OpenCV 影像轉換為 Tkinter PhotoImage 並更新畫面"""
        if len(bgr_or_gray_img.shape) == 2:
            rgb_img = cv2.cvtColor(bgr_or_gray_img, cv2.COLOR_GRAY2RGB)
        else:
            rgb_img = cv2.cvtColor(bgr_or_gray_img, cv2.COLOR_BGR2RGB)

        pil_img = Image.fromarray(rgb_img)
        pil_img.thumbnail((820, 380))
        self.current_display = ImageTk.PhotoImage(pil_img)
        self.display_label.config(image=self.current_display, text="")

    def load_original_image(self):
        if not os.path.exists(self.image_path):
            messagebox.showerror("錯誤", f"找不到測試影像檔：{self.image_path}")
            return
        img = cv2.imread(self.image_path)
        self.update_canvas(img)
        self.status_label.config(text="目前顯示：原始未處理影像", fg="#57606a")

    def handle_processing(self):
        """呼叫對應同學的演算法，並計算精確耗時（毫秒）"""
        if not os.path.exists(self.image_path):
            messagebox.showerror("錯誤", "找不到測試影像！")
            return

        input_img = cv2.imread(self.image_path)
        selected_algo = self.algo_combobox.get()

        try:
            # 高精度計時開始
            start_time = time.perf_counter()

            # 依選單對應呼叫 processor.py 內不同同學的函式
            if "預設演算法" in selected_algo:
                result_img = processor.enhance_edges(input_img)
            elif "同學 A" in selected_algo:
                result_img = getattr(processor, "enhance_student_a", processor.enhance_edges)(input_img)
            elif "同學 B" in selected_algo:
                result_img = getattr(processor, "enhance_student_b", processor.enhance_edges)(input_img)
            elif "同學 C" in selected_algo:
                result_img = getattr(processor, "enhance_student_c", processor.enhance_edges)(input_img)
            else:
                result_img = processor.enhance_edges(input_img)

            # 計時結束並換算為毫秒 (ms)
            elapsed_time = (time.perf_counter() - start_time) * 1000

            # 更新畫面與時間標籤
            self.update_canvas(result_img)
            self.status_label.config(
                text=f"【{selected_algo}】 運算完成！ 耗時: {elapsed_time:.2f} ms | 影像尺寸: {input_img.shape[1]}x{input_img.shape[0]} px",
                fg="#1a7f37"
            )

        except NotImplementedError as e:
            messagebox.showwarning("未實作", str(e))
        except AttributeError as e:
            messagebox.showwarning("函式不存在", f"該同學尚未在 processor.py 中實作該對應函式！\n({str(e)})")
        except Exception as e:
            messagebox.showerror("執行錯誤", f"處理失敗：{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEnhanceApp(root)
    root.mainloop()
