"""
OpenCV 影像操作
適用於 AOI/上位機開發

學習目標：
1. 影像濾波和降噪
2. 邊緣檢測
3. 形態學操作
4. 閾值處理
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt

# ============================================
# 第一部分：影像濾波
# ============================================

def filtering_basics():
    """濾波基礎"""
    print("=" * 50)
    print("影像濾波")
    print("=" * 50)

    print("""
    濾波目的：
    1. 降噪（去除雜訊）
    2. 平滑（模糊）
    3. 銳化（增強邊緣）

    常用濾波器：
    1. 平均濾波：簡單平滑
    2. 高斯濾波：保留邊緣的平滑
    3. 中值濾波：去除椒鹽雜訊
    4. 雙邊濾波：保留邊緣，平滑區域
    """)

    # 創建測試影像（加入雜訊）
    img = np.zeros((300, 400), dtype=np.uint8)
    cv2.rectangle(img, (100, 75), (300, 225), 200, -1)
    cv2.circle(img, (200, 150), 50, 100, -1)

    # 加入高斯雜訊
    noise = np.random.normal(0, 25, img.shape).astype(np.int16)
    noisy = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # 加入椒鹽雜訊
    salt_pepper = noisy.copy()
    num_salt = int(0.02 * salt_pepper.size)
    coords = [np.random.randint(0, i, num_salt) for i in salt_pepper.shape]
    salt_pepper[coords[0], coords[1]] = 255
    coords = [np.random.randint(0, i, num_salt) for i in salt_pepper.shape]
    salt_pepper[coords[0], coords[1]] = 0

    # 各種濾波
    blur_avg = cv2.blur(salt_pepper, (5, 5))
    blur_gauss = cv2.GaussianBlur(salt_pepper, (5, 5), 1.5)
    blur_median = cv2.medianBlur(salt_pepper, 5)
    blur_bilateral = cv2.bilateralFilter(salt_pepper, 9, 75, 75)

    # 視覺化
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('原始影像')
    axes[0, 0].axis('off')

    axes[0, 1].imshow(noisy, cmap='gray')
    axes[0, 1].set_title('高斯雜訊')
    axes[0, 1].axis('off')

    axes[0, 2].imshow(salt_pepper, cmap='gray')
    axes[0, 2].set_title('椒鹽雜訊')
    axes[0, 2].axis('off')

    axes[1, 0].imshow(blur_avg, cmap='gray')
    axes[1, 0].set_title('平均濾波 (5×5)')
    axes[1, 0].axis('off')

    axes[1, 1].imshow(blur_median, cmap='gray')
    axes[1, 1].set_title('中值濾波 (5×5) - 最適合椒鹽')
    axes[1, 1].axis('off')

    axes[1, 2].imshow(blur_bilateral, cmap='gray')
    axes[1, 2].set_title('雙邊濾波 - 保留邊緣')
    axes[1, 2].axis('off')

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\3_image_processing\\ope\\filtering.png', dpi=100)
    print("濾波範例已儲存: filtering.png")
    plt.close()

    return img, noisy, blur_median


# ============================================
# 第二部分：邊緣檢測
# ============================================

def edge_detection():
    """邊緣檢測"""
    print("\n" + "=" * 50)
    print("邊緣檢測")
    print("=" * 50)

    print("""
    邊緣檢測方法：
    1. Sobel：梯度法，可分 X、Y 方向
    2. Laplacian：二階導數
    3. Canny：多步驟，效果最好

    應用：
    - 物體輪廓提取
    - 瑕疵邊緣檢測
    - 尺寸測量
    """)

    # 創建測試影像
    img = np.ones((400, 500), dtype=np.uint8) * 100
    cv2.rectangle(img, (150, 100), (350, 300), 200, -1)
    cv2.circle(img, (250, 200), 60, 50, -1)

    # 平滑以減少雜訊
    img_blur = cv2.GaussianBlur(img, (5, 5), 1.5)

    # Sobel 邊緣檢測
    sobelx = cv2.Sobel(img_blur, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(img_blur, cv2.CV_64F, 0, 1, ksize=3)
    sobel_combined = np.sqrt(sobelx**2 + sobely**2)
    sobel_combined = np.uint8(np.clip(sobel_combined, 0, 255))

    # Laplacian 邊緣檢測
    laplacian = cv2.Laplacian(img_blur, cv2.CV_64F)
    laplacian = np.uint8(np.abs(laplacian))

    # Canny 邊緣檢測
    canny = cv2.Canny(img_blur, 50, 150)

    # 視覺化
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('原始影像')
    axes[0, 0].axis('off')

    axes[0, 1].imshow(np.abs(sobelx), cmap='gray')
    axes[0, 1].set_title('Sobel X (垂直邊緣)')
    axes[0, 1].axis('off')

    axes[0, 2].imshow(np.abs(sobely), cmap='gray')
    axes[0, 2].set_title('Sobel Y (水平邊緣)')
    axes[0, 2].axis('off')

    axes[1, 0].imshow(sobel_combined, cmap='gray')
    axes[1, 0].set_title('Sobel 組合')
    axes[1, 0].axis('off')

    axes[1, 1].imshow(laplacian, cmap='gray')
    axes[1, 1].set_title('Laplacian')
    axes[1, 1].axis('off')

    axes[1, 2].imshow(canny, cmap='gray')
    axes[1, 2].set_title('Canny（最常用）')
    axes[1, 2].axis('off')

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\3_image_processing\\ope\\edge_detection.png', dpi=100)
    print("邊緣檢測範例已儲存: edge_detection.png")
    plt.close()

    return img, canny


# ============================================
# 第三部分：形態學操作
# ============================================

def morphology_operations():
    """形態學操作"""
    print("\n" + "=" * 50)
    print("形態學操作")
    print("=" * 50)

    print("""
    基本操作：
    1. 侵蝕 (Erosion)：縮小白色區域，去除小雜點
    2. 膨脹 (Dilation)：擴大白色區域，填補小孔洞

    組合操作：
    3. 開運算 (Opening) = 侵蝕 + 膨脹：去除小物體
    4. 閉運算 (Closing) = 膨脹 + 侵蝕：填補孔洞
    5. 梯度 (Gradient)：邊緣提取
    6. Top Hat：提取亮細節
    7. Black Hat：提取暗細節

    應用：
    - 雜訊去除
    - 孔洞填補
    - 物體分離
    """)

    # 創建測試影像（含雜訊和孔洞）
    img = np.zeros((400, 500), dtype=np.uint8)

    # 主要物體
    cv2.rectangle(img, (100, 100), (250, 300), 255, -1)
    cv2.rectangle(img, (300, 150), (450, 250), 255, -1)

    # 加入雜訊（小白點）
    for _ in range(50):
        x, y = np.random.randint(0, 500), np.random.randint(0, 400)
        cv2.circle(img, (x, y), 2, 255, -1)

    # 加入孔洞（小黑點）
    for _ in range(30):
        x, y = np.random.randint(100, 450), np.random.randint(100, 300)
        cv2.circle(img, (x, y), 3, 0, -1)

    # 定義結構元素
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    # 各種形態學操作
    erosion = cv2.erode(img, kernel, iterations=1)
    dilation = cv2.dilate(img, kernel, iterations=1)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

    # 視覺化
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('原始（有雜訊和孔洞）')
    axes[0, 0].axis('off')

    axes[0, 1].imshow(erosion, cmap='gray')
    axes[0, 1].set_title('侵蝕（縮小）')
    axes[0, 1].axis('off')

    axes[0, 2].imshow(dilation, cmap='gray')
    axes[0, 2].set_title('膨脹（擴大）')
    axes[0, 2].axis('off')

    axes[1, 0].imshow(opening, cmap='gray')
    axes[1, 0].set_title('開運算（去除小雜點）')
    axes[1, 0].axis('off')

    axes[1, 1].imshow(closing, cmap='gray')
    axes[1, 1].set_title('閉運算（填補孔洞）')
    axes[1, 1].axis('off')

    axes[1, 2].imshow(gradient, cmap='gray')
    axes[1, 2].set_title('形態學梯度（輪廓）')
    axes[1, 2].axis('off')

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\3_image_processing\\ope\\morphology.png', dpi=100)
    print("形態學操作範例已儲存: morphology.png")
    plt.close()

    return img, opening, closing


# ============================================
# 第四部分：閾值處理
# ============================================

def thresholding():
    """閾值處理"""
    print("\n" + "=" * 50)
    print("閾值處理")
    print("=" * 50)

    print("""
    閾值處理：將灰階影像轉為二值影像

    方法：
    1. 固定閾值：手動設定
    2. Otsu：自動計算最佳閾值
    3. 自適應閾值：局部區域計算

    應用：
    - 物體與背景分離
    - 文字識別
    - 瑕疵檢測
    """)

    # 創建測試影像（不均勻光照）
    img = np.ones((400, 600), dtype=np.uint8) * 50

    # 左側亮區
    for x in range(300):
        for y in range(400):
            brightness = 150 + int(50 * (300 - x) / 300)
            img[y, x] = brightness

    # 右側暗區
    for x in range(300, 600):
        for y in range(400):
            brightness = 100 + int(50 * (x - 300) / 300)
            img[y, x] = brightness

    # 加入一些物體
    cv2.circle(img, (150, 200), 60, 50, -1)
    cv2.rectangle(img, (100, 100), (200, 150), 30, -1)
    cv2.circle(img, (450, 200), 60, 200, -1)
    cv2.rectangle(img, (400, 250), (500, 350), 220, -1)

    # 固定閾值
    _, thresh_fixed = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # Otsu 自動閾值
    _, thresh_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 自適應閾值（局部）
    thresh_adaptive_mean = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 51, 10
    )

    thresh_adaptive_gaussian = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 10
    )

    # 視覺化
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('原始（不均勻光照）')
    axes[0, 0].axis('off')

    axes[0, 1].imshow(thresh_fixed, cmap='gray')
    axes[0, 1].set_title('固定閾值 (127)')
    axes[0, 1].axis('off')

    axes[0, 2].imshow(thresh_otsu, cmap='gray')
    axes[0, 2].set_title('Otsu 自動閾值')
    axes[0, 2].axis('off')

    axes[1, 0].imshow(thresh_adaptive_mean, cmap='gray')
    axes[1, 0].set_title('自適應閾值（平均）')
    axes[1, 0].axis('off')

    axes[1, 1].imshow(thresh_adaptive_gaussian, cmap='gray')
    axes[1, 1].set_title('自適應閾值（高斯）- 最好')
    axes[1, 1].axis('off')

    axes[1, 2].axis('off')

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\3_image_processing\\ope\\thresholding.png', dpi=100)
    print("閾值處理範例已儲存: thresholding.png")
    plt.close()

    return img, thresh_adaptive_gaussian


# ============================================
# 第五部分：輪廓檢測
# ============================================

def contour_detection():
    """輪廓檢測"""
    print("\n" + "=" * 50)
    print("輪廓檢測")
    print("=" * 50)

    print("""
    輪廓：影像中連續的邊界點

    用途：
    1. 物體計數
    2. 形狀分析
    3. 尺寸測量
    4. 位置定位

    重要屬性：
    - 面積
    - 周長
    - 邊界框
    - 中心點
    """)

    # 創建測試影像
    img = np.zeros((400, 600), dtype=np.uint8)
    cv2.rectangle(img, (50, 50), (150, 150), 255, -1)
    cv2.circle(img, (250, 100), 50, 255, -1)
    cv2.rectangle(img, (350, 80), (500, 180), 255, -1)
    cv2.circle(img, (150, 280), 60, 255, -1)
    cv2.ellipse(img, (400, 300), (80, 50), 30, 0, 360, 255, -1)

    # 尋找輪廓
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 創建彩色影像來顯示結果
    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    print(f"\n找到 {len(contours)} 個輪廓")

    # 分析每個輪廓
    for i, cnt in enumerate(contours):
        # 面積
        area = cv2.contourArea(cnt)

        # 周長
        perimeter = cv2.arcLength(cnt, True)

        # 邊界框
        x, y, w, h = cv2.boundingRect(cnt)

        # 中心點
        M = cv2.moments(cnt)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
        else:
            cx, cy = 0, 0

        # 繪製
        cv2.drawContours(img_color, [cnt], -1, (0, 255, 0), 2)
        cv2.rectangle(img_color, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.circle(img_color, (cx, cy), 5, (0, 0, 255), -1)

        # 標記資訊
        cv2.putText(img_color, f'#{i+1}', (cx-10, cy-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        print(f"  輪廓 {i+1}: 面積={area:.0f}, 周長={perimeter:.1f}, 中心=({cx}, {cy})")

    # 視覺化
    plt.figure(figsize=(12, 6))
    plt.imshow(cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB))
    plt.title('輪廓檢測（綠色=輪廓，藍色=邊界框，紅色=中心）')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\3_image_processing\\ope\\contours.png', dpi=100)
    print("\n輪廓檢測範例已儲存: contours.png")
    plt.close()

    return img, contours


# ============================================
# 練習題
# ============================================

def exercises():
    """練習題"""
    print("\n" + "=" * 50)
    print("練習題")
    print("=" * 50)

    print("""
    練習 1: 濾波應用
    - 創建或讀取一張影像
    - 加入高斯雜訊（sigma=30）
    - 嘗試不同濾波器（平均、高斯、中值）
    - 計算 PSNR 比較效果

    練習 2: 硬幣計數
    - 創建包含多個圓形（模擬硬幣）的影像
    - 使用 Canny 邊緣檢測
    - 使用 Hough 圓檢測找出所有硬幣
    - 計算硬幣數量和大小

    練習 3: 物體分離
    - 創建包含重疊物體的二值影像
    - 使用形態學操作分離物體
    - 使用 watershed 算法
    - 計數物體數量

    練習 4: 不均勻光照處理
    - 創建光照不均的影像
    - 使用自適應閾值處理
    - 比較不同參數的效果
    - 找出最佳參數組合

    練習 5: 形狀分類
    - 創建包含矩形、圓形、三角形的影像
    - 檢測輪廓
    - 根據形狀特徵（頂點數、圓度等）分類
    - 統計各類形狀數量
    """)


# ============================================
# 主程式
# ============================================

if __name__ == "__main__":
    print("OpenCV 影像操作教學\n")

    # 執行所有示範
    filtering_basics()
    edge_detection()
    morphology_operations()
    thresholding()
    contour_detection()
    exercises()

    print("\n" + "=" * 50)
    print("教學完成！")
    print("=" * 50)
    print("\n下一步：學習 03_aoi_applications.py（AOI 實際應用）")
