"""
OpenCV 基礎
適用於 AOI/上位機開發

學習目標：
1. OpenCV 基本操作
2. 影像讀取、顯示、儲存
3. 基本影像屬性和操作
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt

# ============================================
# 第一部分：OpenCV 基礎
# ============================================

def opencv_basics():
    """OpenCV 基本概念"""
    print("=" * 50)
    print("OpenCV 基礎")
    print("=" * 50)

    print("""
    OpenCV (Open Source Computer Vision Library)

    主要功能：
    1. 影像 I/O：讀取、顯示、儲存
    2. 影像處理：濾波、變換、增強
    3. 特徵檢測：邊緣、角點、輪廓
    4. 物件偵測：分類、識別
    5. 幾何變換：旋轉、縮放、透視

    影像表示：
    - 灰階影像：2D 陣列，值範圍 0-255
    - 彩色影像：3D 陣列 (H, W, 3)，通道順序 BGR（注意！）
    - 座標系：(y, x) 或 (row, col)，原點在左上角

    常用資料型別：
    - np.uint8：0-255，最常用
    - np.float32/64：歸一化到 0-1 或任意範圍
    """)


def create_sample_images():
    """創建範例影像"""
    print("\n" + "=" * 50)
    print("創建範例影像")
    print("=" * 50)

    # 1. 全黑影像
    black = np.zeros((300, 400), dtype=np.uint8)
    print(f"黑色影像形狀: {black.shape}")
    print(f"資料型別: {black.dtype}")

    # 2. 全白影像
    white = np.ones((300, 400), dtype=np.uint8) * 255
    print(f"白色影像最大值: {white.max()}")

    # 3. 灰階漸層
    gradient = np.linspace(0, 255, 400, dtype=np.uint8)
    gradient = np.tile(gradient, (300, 1))

    # 4. 彩色影像 (BGR)
    color = np.zeros((300, 400, 3), dtype=np.uint8)
    color[:, :, 0] = 255  # 藍色通道
    color[:, 100:200, 1] = 255  # 綠色區域
    color[:, 200:300, 2] = 255  # 紅色區域

    # 5. 簡單圖案
    pattern = np.zeros((300, 400), dtype=np.uint8)
    cv2.rectangle(pattern, (50, 50), (150, 150), 255, -1)
    cv2.circle(pattern, (250, 100), 50, 128, -1)
    cv2.line(pattern, (50, 200), (350, 250), 200, 3)

    # 視覺化
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    axes[0, 0].imshow(black, cmap='gray')
    axes[0, 0].set_title('全黑')
    axes[0, 0].axis('off')

    axes[0, 1].imshow(white, cmap='gray')
    axes[0, 1].set_title('全白')
    axes[0, 1].axis('off')

    axes[0, 2].imshow(gradient, cmap='gray')
    axes[0, 2].set_title('灰階漸層')
    axes[0, 2].axis('off')

    axes[1, 0].imshow(cv2.cvtColor(color, cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title('彩色影像 (BGR->RGB)')
    axes[1, 0].axis('off')

    axes[1, 1].imshow(pattern, cmap='gray')
    axes[1, 1].set_title('簡單圖案')
    axes[1, 1].axis('off')

    axes[1, 2].axis('off')

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\3_image_processing\\sample_images.png', dpi=100)
    print("\n範例影像已儲存: sample_images.png")
    plt.close()

    # 儲存範例影像供後續使用
    cv2.imwrite('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\3_image_processing\\pattern.png', pattern)

    return black, white, gradient, color, pattern


# ============================================
# 第二部分：基本影像操作
# ============================================

def image_properties():
    """影像屬性"""
    print("\n" + "=" * 50)
    print("影像屬性")
    print("=" * 50)

    # 創建範例影像
    gray_img = np.random.randint(0, 256, (480, 640), dtype=np.uint8)
    color_img = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)

    print("灰階影像:")
    print(f"  形狀: {gray_img.shape}")
    print(f"  大小: {gray_img.size} 像素")
    print(f"  資料型別: {gray_img.dtype}")
    print(f"  維度: {gray_img.ndim}")
    print(f"  最小值: {gray_img.min()}, 最大值: {gray_img.max()}")
    print(f"  平均值: {gray_img.mean():.2f}")

    print("\n彩色影像:")
    print(f"  形狀: {color_img.shape}")
    print(f"  通道數: {color_img.shape[2]}")
    print(f"  大小: {color_img.size} 元素")

    # 通道分離
    b, g, r = cv2.split(color_img)
    print(f"\n分離通道形狀: B={b.shape}, G={g.shape}, R={r.shape}")

    # 通道合併
    merged = cv2.merge([b, g, r])
    print(f"合併後形狀: {merged.shape}")

    return gray_img, color_img


def pixel_access():
    """像素訪問"""
    print("\n" + "=" * 50)
    print("像素訪問")
    print("=" * 50)

    # 創建小影像
    img = np.zeros((5, 5), dtype=np.uint8)

    print("原始影像:")
    print(img)

    # 單一像素
    img[2, 2] = 255
    print("\n設定中心點為 255:")
    print(img)

    # 區域
    img[0:2, 0:2] = 128
    print("\n設定左上角為 128:")
    print(img)

    # 彩色影像
    color = np.zeros((5, 5, 3), dtype=np.uint8)
    color[2, 2] = [255, 0, 0]  # BGR: 藍色
    print("\n彩色影像中心點 (BGR):")
    print(f"B={color[2,2,0]}, G={color[2,2,1]}, R={color[2,2,2]}")

    # 高效訪問：避免逐像素迴圈
    print("\n效率提示:")
    print("  慢：for i in range(h): for j in range(w): img[i,j] = ...")
    print("  快：img[:] = ... (向量化操作)")

    return img


def image_roi():
    """感興趣區域 (ROI)"""
    print("\n" + "=" * 50)
    print("感興趣區域 (ROI)")
    print("=" * 50)

    # 創建影像
    img = np.ones((400, 600), dtype=np.uint8) * 50

    # 定義 ROI
    roi_x, roi_y, roi_w, roi_h = 100, 150, 200, 100
    roi = img[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

    print(f"原始影像形狀: {img.shape}")
    print(f"ROI 座標: x={roi_x}, y={roi_y}, w={roi_w}, h={roi_h}")
    print(f"ROI 形狀: {roi.shape}")

    # 修改 ROI
    roi[:] = 200

    # 繪製 ROI 框
    img_vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.rectangle(img_vis, (roi_x, roi_y), (roi_x+roi_w, roi_y+roi_h), (0, 255, 0), 2)

    plt.figure(figsize=(10, 6))
    plt.imshow(img_vis)
    plt.title('影像與 ROI')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\3_image_processing\\roi_example.png', dpi=100)
    print("ROI 範例已儲存: roi_example.png")
    plt.close()

    return img, roi


# ============================================
# 第三部分：基本繪圖
# ============================================

def drawing_functions():
    """OpenCV 繪圖函數"""
    print("\n" + "=" * 50)
    print("OpenCV 繪圖函數")
    print("=" * 50)

    # 創建畫布
    canvas = np.zeros((500, 700, 3), dtype=np.uint8)

    # 線條
    cv2.line(canvas, (50, 50), (200, 50), (0, 255, 0), 2)
    cv2.putText(canvas, 'Line', (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # 矩形
    cv2.rectangle(canvas, (250, 30), (400, 120), (255, 0, 0), 2)
    cv2.putText(canvas, 'Rectangle', (250, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # 實心矩形
    cv2.rectangle(canvas, (450, 30), (600, 120), (0, 0, 255), -1)
    cv2.putText(canvas, 'Filled', (450, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # 圓形
    cv2.circle(canvas, (125, 200), 50, (255, 255, 0), 2)
    cv2.putText(canvas, 'Circle', (100, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # 實心圓
    cv2.circle(canvas, (325, 200), 50, (255, 0, 255), -1)
    cv2.putText(canvas, 'Filled Circle', (270, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # 橢圓
    cv2.ellipse(canvas, (525, 200), (70, 40), 30, 0, 360, (0, 255, 255), 2)
    cv2.putText(canvas, 'Ellipse', (480, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # 多邊形
    pts = np.array([[125, 320], [75, 420], [175, 420]], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(canvas, [pts], True, (128, 128, 255), 2)
    cv2.putText(canvas, 'Polygon', (100, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # 文字
    cv2.putText(canvas, 'OpenCV Drawing', (250, 380),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

    # 十字標記（常用於標記點）
    cv2.drawMarker(canvas, (525, 370), (0, 255, 0), cv2.MARKER_CROSS, 20, 2)
    cv2.putText(canvas, 'Marker', (540, 375), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # 視覺化
    plt.figure(figsize=(12, 8))
    plt.imshow(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
    plt.title('OpenCV 繪圖函數')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\3_image_processing\\drawing_functions.png', dpi=100)
    print("繪圖函數範例已儲存: drawing_functions.png")
    plt.close()

    return canvas


# ============================================
# 第四部分：顏色空間轉換
# ============================================

def color_spaces():
    """顏色空間轉換"""
    print("\n" + "=" * 50)
    print("顏色空間轉換")
    print("=" * 50)

    print("""
    常用顏色空間：
    1. BGR：OpenCV 預設，適合顯示
    2. RGB：標準 RGB，matplotlib 使用
    3. GRAY：灰階，單通道
    4. HSV：色相-飽和度-明度，適合顏色偵測
    5. LAB：明度-A-B，適合顏色測量

    轉換函數：
    - cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    - cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    - cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    """)

    # 創建彩色影像
    img = np.zeros((300, 400, 3), dtype=np.uint8)
    img[:100, :, 2] = 255  # 紅色
    img[100:200, :, 1] = 255  # 綠色
    img[200:, :, 0] = 255  # 藍色

    # 轉換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 視覺化
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    axes[0, 0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('原始 (BGR->RGB for display)')
    axes[0, 0].axis('off')

    axes[0, 1].imshow(gray, cmap='gray')
    axes[0, 1].set_title('灰階 (GRAY)')
    axes[0, 1].axis('off')

    axes[0, 2].imshow(cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB))
    axes[0, 2].set_title('HSV (顯示為 RGB)')
    axes[0, 2].axis('off')

    # HSV 通道分離
    h, s, v = cv2.split(hsv)
    axes[1, 0].imshow(h, cmap='hsv')
    axes[1, 0].set_title('H (色相)')
    axes[1, 0].axis('off')

    axes[1, 1].imshow(s, cmap='gray')
    axes[1, 1].set_title('S (飽和度)')
    axes[1, 1].axis('off')

    axes[1, 2].imshow(v, cmap='gray')
    axes[1, 2].set_title('V (明度)')
    axes[1, 2].axis('off')

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\3_image_processing\\color_spaces.png', dpi=100)
    print("顏色空間轉換範例已儲存: color_spaces.png")
    plt.close()

    return img, gray, hsv


# ============================================
# 第五部分：實用技巧
# ============================================

def practical_tips():
    """實用技巧"""
    print("\n" + "=" * 50)
    print("OpenCV 實用技巧")
    print("=" * 50)

    print("""
    1. 影像讀取：
       img = cv2.imread('file.png')  # 預設 BGR
       img = cv2.imread('file.png', cv2.IMREAD_GRAYSCALE)  # 灰階
       img = cv2.imread('file.png', cv2.IMREAD_UNCHANGED)  # 包含 alpha

    2. 影像儲存：
       cv2.imwrite('output.png', img)
       cv2.imwrite('output.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 95])

    3. 影像複製（重要！）：
       img_copy = img.copy()  # 深複製
       img_view = img  # 淺複製（共享資料）

    4. 型別轉換：
       img_float = img.astype(np.float32) / 255.0  # 歸一化到 0-1
       img_uint8 = (img_float * 255).astype(np.uint8)  # 轉回 uint8

    5. 影像資訊：
       height, width = img.shape[:2]  # 適用於灰階和彩色
       channels = img.shape[2] if len(img.shape) == 3 else 1

    6. 邊界處理：
       避免越界錯誤
       x = np.clip(x, 0, width-1)
       y = np.clip(y, 0, height-1)

    7. 效能優化：
       - 避免逐像素迴圈，使用向量化操作
       - 預分配記憶體
       - 使用適當的資料型別（uint8 vs float32）
    """)


# ============================================
# 練習題
# ============================================

def exercises():
    """練習題"""
    print("\n" + "=" * 50)
    print("練習題")
    print("=" * 50)

    print("""
    練習 1: 創建棋盤圖案
    - 創建 8×8 棋盤（黑白相間）
    - 每格 50×50 像素
    - 儲存為 'chessboard.png'

    練習 2: 影像分割
    - 創建 640×480 的彩色影像
    - 分成 4 個象限，每個不同顏色
    - 在每個象限中心畫圓

    練習 3: ROI 操作
    - 讀取一張影像（或創建）
    - 選擇 ROI
    - 複製 ROI 到另一個位置
    - 在 ROI 上應用變換（如反轉顏色）

    練習 4: 顏色偵測
    - 創建一張包含多種顏色的影像
    - 轉換到 HSV 空間
    - 使用 inRange 函數偵測特定顏色（如紅色）
    - 創建遮罩並提取該顏色區域

    練習 5: 繪製座標系
    - 創建影像
    - 繪製 X-Y 座標軸（原點在中心）
    - 標記刻度（每 50 像素）
    - 在座標系上繪製一些點
    - 加上圖例和標題
    """)

    # 練習解答區
    print("\n# 練習 1 解答：")
    # 在這裡寫你的代碼

    print("\n# 練習 2 解答：")
    # 在這裡寫你的代碼

    print("\n# 練習 3 解答：")
    # 在這裡寫你的代碼

    print("\n# 練習 4 解答：")
    # 在這裡寫你的代碼

    print("\n# 練習 5 解答：")
    # 在這裡寫你的代碼


# ============================================
# 主程式
# ============================================

if __name__ == "__main__":
    print("OpenCV 基礎教學\n")

    # 執行所有示範
    opencv_basics()
    create_sample_images()
    image_properties()
    pixel_access()
    image_roi()
    drawing_functions()
    color_spaces()
    practical_tips()
    exercises()

    print("\n" + "=" * 50)
    print("教學完成！")
    print("=" * 50)
    print("\n下一步：學習 02_image_operations.py（影像操作）")
