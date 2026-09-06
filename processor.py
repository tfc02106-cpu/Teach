import cv2
import numpy as np

# 預設通用接口（原協作成果）
def enhance_edges(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gaussian = cv2.GaussianBlur(gray, (0, 0), sigmaX=3)
    unsharp = cv2.addWeighted(gray, 1.8, gaussian, -0.8, 0)
    kernel = np.array([[ 0, -1,  0],
                       [-1,  5, -1],
                       [ 0, -1,  0]], dtype=np.float32)
    return cv2.filter2D(unsharp, -1, kernel)

# 同學 A：專注輕量化快速運算（Unsharp Masking）
def enhance_student_a(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, (3, 3))
    return cv2.addWeighted(gray, 1.5, blur, -0.5, 0)

# 同學 B：拉普拉斯高通二階微分（輪廓強烈，適合微小刻度）
def enhance_student_b(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_16S, ksize=3)
    laplacian = cv2.convertScaleAbs(laplacian)
    return cv2.addWeighted(gray, 1.0, laplacian, -0.7, 0)

# 同學 C：Sobel 梯度強化（著重垂直刻度線偵測）
def enhance_student_c(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grad_x = cv2.Sobel(gray, cv2.CV_16S, 1, 0, ksize=3)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    return cv2.bitwise_not(abs_grad_x)
