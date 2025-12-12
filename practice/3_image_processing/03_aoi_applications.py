"""
OpenCV AOI 應用
適用於 AOI/上位機開發

學習目標：
1. 瑕疵檢測
2. 尺寸測量
3. 定位標記檢測
4. 影像對齊
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt

# ============================================
# 第一部分：瑕疵檢測
# ============================================

def defect_detection():
    """瑕疵檢測示範"""
    print("=" * 50)
    print("瑕疵檢測")
    print("=" * 50)

    print("""
    瑕疵檢測流程：
    1. 影像預處理（降噪、增強）
    2. 背景建模或模板匹配
    3. 差異檢測
    4. 閾值處理
    5. 形態學操作
    6. 輪廓分析
    """)

    # 創建理想樣本（模板）
    template = np.ones((300, 400), dtype=np.uint8) * 200
    cv2.rectangle(template, (50, 50), (150, 150), 180, -1)
    cv2.rectangle(template, (200, 50), (350, 150), 180, -1)
    cv2.rectangle(template, (50, 170), (150, 270), 180, -1)
    cv2.rectangle(template, (200, 170), (350, 270), 180, -1)

    # 創建待檢測影像（含瑕疵）
    test_img = template.copy()

    # 加入瑕疵
    # 瑕疵 1：污點
    cv2.circle(test_img, (100, 100), 15, 100, -1)

    # 瑕疵 2：刮痕
    cv2.line(test_img, (250, 60), (320, 140), 120, 2)

    # 瑕疵 3：缺陷
    cv2.circle(test_img, (100, 220), 20, 255, -1)

    # 瑕疵檢測：差異法
    diff = cv2.absdiff(template, test_img)

    # 閾值處理
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    # 形態學操作去除小雜訊
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # 尋找瑕疵輪廓
    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 標記瑕疵
    result = cv2.cvtColor(test_img, cv2.COLOR_GRAY2BGR)

    defect_count = 0
    print(f"\n檢測到 {len(contours)} 個瑕疵：")

    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)

        # 過濾太小的區域
        if area < 50:
            continue

        defect_count += 1

        # 邊界框
        x, y, w, h = cv2.boundingRect(cnt)

        # 繪製
        cv2.drawContours(result, [cnt], -1, (0, 0, 255), 2)
        cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(result, f'D{defect_count}', (x, y-5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        print(f"  瑕疵 {defect_count}: 位置=({x}, {y}), 面積={area:.0f}")

    # 視覺化
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    axes[0, 0].imshow(template, cmap='gray')
    axes[0, 0].set_title('理想樣本（模板）')
    axes[0, 0].axis('off')

    axes[0, 1].imshow(test_img, cmap='gray')
    axes[0, 1].set_title('待檢測影像')
    axes[0, 1].axis('off')

    axes[0, 2].imshow(diff, cmap='gray')
    axes[0, 2].set_title('差異圖')
    axes[0, 2].axis('off')

    axes[1, 0].imshow(thresh, cmap='gray')
    axes[1, 0].set_title('閾值處理')
    axes[1, 0].axis('off')

    axes[1, 1].imshow(cleaned, cmap='gray')
    axes[1, 1].set_title('形態學清理')
    axes[1, 1].axis('off')

    axes[1, 2].imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    axes[1, 2].set_title(f'檢測結果 ({defect_count} 瑕疵)')
    axes[1, 2].axis('off')

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\3_image_processing\\aoi\\defect_detection.png', dpi=100)
    print("\n瑕疵檢測範例已儲存: defect_detection.png")
    plt.close()

    return result, defect_count


# ============================================
# 第二部分：尺寸測量
# ============================================

def dimension_measurement():
    """尺寸測量"""
    print("\n" + "=" * 50)
    print("尺寸測量")
    print("=" * 50)

    print("""
    尺寸測量步驟：
    1. 影像校準（像素 -> 實際單位）
    2. 邊緣檢測
    3. 輪廓提取
    4. 特徵點檢測
    5. 距離計算

    校準方法：
    - 已知尺寸的標準件
    - 像素/mm 比例
    """)

    # 創建測試影像
    img = np.zeros((500, 600), dtype=np.uint8)

    # 繪製待測物體（矩形和圓形）
    cv2.rectangle(img, (100, 100), (300, 250), 255, -1)
    cv2.circle(img, (450, 200), 80, 255, -1)

    # 校準參數（假設：1 像素 = 0.1 mm）
    pixel_to_mm = 0.1

    # 邊緣檢測
    edges = cv2.Canny(img, 50, 150)

    # 尋找輪廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 創建結果影像
    result = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    print(f"\n測量結果（校準係數: {pixel_to_mm} mm/pixel）：")

    for i, cnt in enumerate(contours):
        # 邊界框
        x, y, w, h = cv2.boundingRect(cnt)

        # 計算實際尺寸
        width_mm = w * pixel_to_mm
        height_mm = h * pixel_to_mm

        # 如果是圓形，計算直徑
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)

        # 圓度判斷
        if perimeter > 0:
            circularity = 4 * np.pi * area / (perimeter ** 2)
        else:
            circularity = 0

        # 繪製測量線
        cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # 寬度標註
        cv2.line(result, (x, y-10), (x+w, y-10), (255, 0, 0), 2)
        cv2.putText(result, f'{width_mm:.1f}mm', (x+w//2-30, y-15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # 高度標註
        cv2.line(result, (x-10, y), (x-10, y+h), (255, 0, 0), 2)
        cv2.putText(result, f'{height_mm:.1f}mm', (x-60, y+h//2),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        print(f"  物體 {i+1}:")
        print(f"    寬度: {width_mm:.2f} mm ({w} pixels)")
        print(f"    高度: {height_mm:.2f} mm ({h} pixels)")
        print(f"    面積: {area * pixel_to_mm**2:.2f} mm²")

        if circularity > 0.8:
            diameter_mm = 2 * np.sqrt(area / np.pi) * pixel_to_mm
            print(f"    形狀: 圓形, 直徑: {diameter_mm:.2f} mm")
        else:
            print(f"    形狀: 矩形")

    # 視覺化
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(img, cmap='gray')
    axes[0].set_title('原始影像')
    axes[0].axis('off')

    axes[1].imshow(edges, cmap='gray')
    axes[1].set_title('邊緣檢測')
    axes[1].axis('off')

    axes[2].imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    axes[2].set_title('尺寸測量結果')
    axes[2].axis('off')

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\3_image_processing\\aoi\\dimension_measurement.png', dpi=100)
    print("\n尺寸測量範例已儲存: dimension_measurement.png")
    plt.close()

    return result


# ============================================
# 第三部分：定位標記檢測 (Fiducial Mark)
# ============================================

def fiducial_detection():
    """定位標記檢測"""
    print("\n" + "=" * 50)
    print("定位標記檢測")
    print("=" * 50)

    print("""
    定位標記（Fiducial Mark）用途：
    1. PCB 對齊
    2. 工件定位
    3. 座標校正

    常見標記類型：
    - 圓形標記
    - 十字標記
    - 方形標記
    """)

    # 創建包含定位標記的影像
    img = np.ones((600, 800), dtype=np.uint8) * 200

    # PCB 區域
    cv2.rectangle(img, (100, 100), (700, 500), 180, -1)

    # 定位標記（四角）
    marks = [
        (150, 150),  # 左上
        (650, 150),  # 右上
        (150, 450),  # 左下
        (650, 450),  # 右下
    ]

    for mx, my in marks:
        # 圓形標記
        cv2.circle(img, (mx, my), 20, 50, -1)
        cv2.circle(img, (mx, my), 10, 200, -1)

    # 檢測定位標記
    # 使用 Hough 圓檢測
    img_blur = cv2.GaussianBlur(img, (5, 5), 1.5)
    circles = cv2.HoughCircles(
        img_blur,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=100,
        param1=100,
        param2=30,
        minRadius=5,
        maxRadius=25
    )

    # 創建結果影像
    result = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    detected_marks = []

    if circles is not None:
        circles = np.uint16(np.around(circles))
        print(f"\n檢測到 {len(circles[0])} 個定位標記：")

        for i, circle in enumerate(circles[0, :]):
            cx, cy, r = circle

            # 繪製檢測結果
            cv2.circle(result, (cx, cy), r, (0, 255, 0), 2)
            cv2.circle(result, (cx, cy), 2, (0, 0, 255), 3)
            cv2.putText(result, f'M{i+1}', (cx+15, cy),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

            detected_marks.append((cx, cy))
            print(f"  標記 {i+1}: 位置=({cx}, {cy}), 半徑={r}")

        # 計算旋轉角度（如果檢測到至少兩個標記）
        if len(detected_marks) >= 2:
            # 使用前兩個點計算角度
            p1, p2 = detected_marks[0], detected_marks[1]
            angle = np.degrees(np.arctan2(p2[1] - p1[1], p2[0] - p1[0]))
            print(f"\n工件旋轉角度: {angle:.2f}°")

            # 繪製連線
            cv2.line(result, p1, p2, (255, 255, 0), 2)

    # 視覺化
    plt.figure(figsize=(12, 8))
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.title('定位標記檢測')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\3_image_processing\\aoi\\fiducial_detection.png', dpi=100)
    print("\n定位標記檢測範例已儲存: fiducial_detection.png")
    plt.close()

    return result, detected_marks


# ============================================
# 第四部分：影像對齊
# ============================================

def image_alignment():
    """影像對齊"""
    print("\n" + "=" * 50)
    print("影像對齊")
    print("=" * 50)

    print("""
    影像對齊步驟：
    1. 特徵點檢測（定位標記或角點）
    2. 對應點匹配
    3. 變換矩陣計算
    4. 影像變換

    變換類型：
    - 平移
    - 旋轉
    - 縮放
    - 透視變換
    """)

    # 創建參考影像（模板）
    template = np.ones((400, 500), dtype=np.uint8) * 200
    cv2.rectangle(template, (100, 100), (400, 300), 100, -1)
    cv2.circle(template, (250, 200), 50, 150, -1)

    # 定位標記
    template_marks = np.float32([
        [120, 120],
        [380, 120],
        [120, 280],
        [380, 280]
    ])

    for pt in template_marks:
        cv2.circle(template, tuple(pt.astype(int)), 8, 50, -1)

    # 創建待對齊影像（有平移和旋轉）
    # 旋轉 15 度
    angle = 15
    center = (250, 200)
    M_rot = cv2.getRotationMatrix2D(center, angle, 1.0)

    # 先旋轉
    test_img = cv2.warpAffine(template, M_rot, (500, 400))

    # 再平移
    M_trans = np.float32([[1, 0, 30], [0, 1, 20]])
    test_img = cv2.warpAffine(test_img, M_trans, (500, 400))

    # 檢測到的標記（模擬）
    test_marks = cv2.transform(template_marks.reshape(-1, 1, 2), M_rot).reshape(-1, 2)
    test_marks += np.array([30, 20])  # 加上平移

    # 計算變換矩陣
    M_align = cv2.getPerspectiveTransform(test_marks, template_marks)

    # 對齊影像
    aligned = cv2.warpPerspective(test_img, M_align, (500, 400))

    # 視覺化
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # 參考影像
    axes[0, 0].imshow(template, cmap='gray')
    for i, pt in enumerate(template_marks):
        axes[0, 0].plot(pt[0], pt[1], 'ro', markersize=8)
        axes[0, 0].text(pt[0]+10, pt[1], f'T{i+1}', color='red')
    axes[0, 0].set_title('參考影像（模板）')
    axes[0, 0].axis('off')

    # 待對齊影像
    axes[0, 1].imshow(test_img, cmap='gray')
    for i, pt in enumerate(test_marks):
        axes[0, 1].plot(pt[0], pt[1], 'bo', markersize=8)
        axes[0, 1].text(pt[0]+10, pt[1], f'S{i+1}', color='blue')
    axes[0, 1].set_title(f'待對齊影像（旋轉{angle}°+平移）')
    axes[0, 1].axis('off')

    # 對齊後
    axes[1, 0].imshow(aligned, cmap='gray')
    axes[1, 0].set_title('對齊後影像')
    axes[1, 0].axis('off')

    # 差異圖
    diff = cv2.absdiff(template, aligned)
    axes[1, 1].imshow(diff, cmap='hot')
    axes[1, 1].set_title('對齊誤差')
    axes[1, 1].axis('off')

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\3_image_processing\\aoi\\image_alignment.png', dpi=100)
    print("影像對齊範例已儲存: image_alignment.png")
    print(f"對齊後平均誤差: {np.mean(diff):.2f}")
    plt.close()

    return aligned


# ============================================
# 練習題
# ============================================

def exercises():
    """練習題"""
    print("\n" + "=" * 50)
    print("練習題")
    print("=" * 50)

    print("""
    練習 1: 進階瑕疵檢測
    - 創建包含多種瑕疵的測試影像
    - 實現瑕疵分類（污點、刮痕、缺陷）
    - 根據面積、形狀特徵分類
    - 生成檢測報告

    練習 2: 精密測量
    - 創建一個複雜零件影像
    - 實現多點測量（多個尺寸）
    - 計算公差（與標準值比較）
    - 判定合格/不合格

    練習 3: 自動校準
    - 創建包含標準網格的校準板
    - 檢測網格交點
    - 計算畸變矯正參數
    - 應用畸變矯正

    練習 4: 模板匹配
    - 創建一個包含多個相同元件的 PCB 影像
    - 使用模板匹配找出所有元件
    - 計算元件位置和旋轉角度
    - 檢查元件是否缺失

    練習 5: 完整 AOI 流程
    - 整合所有功能
    - 實現：影像獲取 -> 對齊 -> 檢測 -> 測量 -> 報告
    - 處理實際影像（可以自己創建模擬影像）
    - 輸出 HTML 檢測報告
    """)


# ============================================
# 主程式
# ============================================

if __name__ == "__main__":
    print("AOI 影像應用教學\n")

    # 執行所有示範
    defect_detection()
    dimension_measurement()
    fiducial_detection()
    image_alignment()
    exercises()

    print("\n" + "=" * 50)
    print("AOI 應用教學完成！")
    print("=" * 50)
    print("\n恭喜完成影像處理部分！")
    print("下一步：進入 4_control_theory 資料夾學習控制理論")
