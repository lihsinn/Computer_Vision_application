"""基本測試腳本（不需要 GUI）"""
import numpy as np
import cv2

print("測試旋轉檢測...")

# 創建測試影像
test_angle = 28.0
img = np.zeros((500, 500), dtype=np.uint8)
center = (250, 250)
size = (150, 80)
rect = (center, size, test_angle)
box = cv2.boxPoints(rect)
box = np.int32(box)
cv2.drawContours(img, [box], 0, 255, -1)

# 檢測角度
contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if len(contours) > 0:
    largest_contour = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(largest_contour)
    center, size, angle = rect

    # 處理寬高和角度
    width, height = size
    if width < height:
        angle = 90 + angle

    # 正規化到 [0, 360)
    if angle < 0:
        angle += 360

    print(f"[SUCCESS] 測試通過！")
    print(f"  實際角度：{test_angle:.2f}°")
    print(f"  檢測角度：{angle:.2f}°")
    print(f"  誤差：{abs(angle - test_angle):.2f}°")
else:
    print("[ERROR] 檢測失敗")
