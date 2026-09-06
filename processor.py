import cv2
import numpy as np

def enhance_edges(image: np.ndarray) -> np.ndarray:
    """
    利用非銳化濾鏡 (Unsharp Masking) 與高通核心強化刻度邊緣
    """
    # 1. 轉灰階
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. 高斯模糊提取低頻基底
    gaussian = cv2.GaussianBlur(gray, (0, 0), sigmaX=3)

    # 3. 原始影像減去模糊影像取得細節邊緣，疊加回原圖
    unsharp = cv2.addWeighted(gray, 1.8, gaussian, -0.8, 0)

    # 4. （選用）搭配拉普拉斯運算子二次強化刻度邊界
    kernel = np.array([[ 0, -1,  0],
                       [-1,  5, -1],
                       [ 0, -1,  0]], dtype=np.float32)
    sharpened = cv2.filter2D(unsharp, -1, kernel)

    return sharpened
