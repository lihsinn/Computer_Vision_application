"""測試標記點檢測"""
import numpy as np
import cv2

def create_shape_with_markers(angle):
    """創建帶有標記點的物件"""
    img = np.zeros((500, 500), dtype=np.uint8)
    center = np.array([250, 250])

    # 矩形主體
    size = (120, 80)
    rect = ((float(center[0]), float(center[1])), size, angle)
    box = cv2.boxPoints(rect)
    box = np.int32(box)
    cv2.drawContours(img, [box], 0, 200, -1)

    # 添加標記點
    angle_rad = np.radians(angle)
    marker_offset = np.array([90, 0])  # 在右側
    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad), np.cos(angle_rad)]
    ])
    marker_pos = center + marker_offset @ rotation_matrix.T
    cv2.circle(img, tuple(marker_pos.astype(int)), 10, 255, -1)

    return img, marker_pos

# 測試
print("測試標記點檢測...")
img, expected_marker = create_shape_with_markers(30)

# 尋找輪廓
contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print(f"找到 {len(contours)} 個輪廓")

if len(contours) >= 2:
    # 按面積排序
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for i, cnt in enumerate(contours[:3]):  # 顯示前3個
        area = cv2.contourArea(cnt)
        M = cv2.moments(cnt)
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            print(f"  輪廓 {i+1}: 面積={area:.0f}, 中心=({cx}, {cy})")

    print("\n[SUCCESS] 標記點檢測可以正常工作！")
else:
    print(f"\n[ERROR] 只找到 {len(contours)} 個輪廓，需要至少 2 個")
    print("標記點可能在矩形內部或與矩形合併了")
