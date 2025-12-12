"""詳細的角度測試"""
import numpy as np
import cv2

def test_angle(input_angle):
    """測試角度檢測"""
    print(f"\n{'='*60}")
    print(f"輸入角度: {input_angle}°")

    # 創建矩形
    img = np.zeros((500, 500), dtype=np.uint8)
    center = (250, 250)
    size = (150, 80)  # 寬 > 高

    # 方法 A: 使用 OpenCV 的 boxPoints
    rect = (center, size, input_angle)
    box = cv2.boxPoints(rect)
    box = np.int32(box)
    cv2.drawContours(img, [box], 0, 255, -1)

    print(f"創建矩形的四個角點:")
    for i, pt in enumerate(box):
        print(f"  P{i}: ({pt[0]}, {pt[1]})")

    # 檢測
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detected_rect = cv2.minAreaRect(contours[0])
    det_center, det_size, det_angle = detected_rect

    print(f"\nOpenCV minAreaRect 輸出:")
    print(f"  angle: {det_angle:.2f}°")
    print(f"  size: ({det_size[0]:.1f}, {det_size[1]:.1f})")

    # 檢測到的角點
    detected_box = cv2.boxPoints(detected_rect)
    print(f"\n檢測到的矩形角點:")
    for i, pt in enumerate(detected_box):
        print(f"  P{i}: ({pt[0]:.1f}, {pt[1]:.1f})")

    # 方法 1: 直接使用 OpenCV 角度
    angle_method1 = det_angle
    if det_angle < 0:
        angle_method1 += 360

    # 方法 2: 從角點計算（不修正 Y）
    vec2 = detected_box[1] - detected_box[0]
    angle_method2 = np.degrees(np.arctan2(vec2[1], vec2[0]))
    if angle_method2 < 0:
        angle_method2 += 360

    # 方法 3: 從角點計算（修正 Y）
    vec3 = detected_box[1] - detected_box[0]
    angle_method3 = np.degrees(np.arctan2(-vec3[1], vec3[0]))
    if angle_method3 < 0:
        angle_method3 += 360

    # 方法 4: 考慮寬高
    width, height = det_size
    angle_method4 = det_angle
    if width < height:
        angle_method4 = 90 + det_angle
    if angle_method4 < 0:
        angle_method4 += 360

    print(f"\n檢測結果比較:")
    print(f"  輸入角度:          {input_angle:.2f}°")
    print(f"  方法1 (OpenCV):    {angle_method1:.2f}°  誤差: {abs(angle_method1 - input_angle):.2f}°")
    print(f"  方法2 (角點):      {angle_method2:.2f}°  誤差: {abs(angle_method2 - input_angle):.2f}°")
    print(f"  方法3 (角點+Y修正): {angle_method3:.2f}°  誤差: {abs(angle_method3 - input_angle):.2f}°")
    print(f"  方法4 (寬高調整):   {angle_method4:.2f}°  誤差: {abs(angle_method4 - input_angle):.2f}°")

    # 找出最佳方法
    errors = [
        abs(angle_method1 - input_angle),
        abs(angle_method2 - input_angle),
        abs(angle_method3 - input_angle),
        abs(angle_method4 - input_angle)
    ]
    best_idx = errors.index(min(errors))
    methods = ["OpenCV 原始", "角點", "角點+Y修正", "寬高調整"]
    print(f"\n最佳方法: {methods[best_idx]} (誤差: {errors[best_idx]:.2f}°)")

    return errors[best_idx]

# 測試多個角度
print("="*60)
print("詳細角度檢測測試")
print("="*60)

test_angles = [0, 15, 30, 45, 60, 75, 90, -15, -30, -45]
for angle in test_angles:
    test_angle(angle)

print(f"\n{'='*60}")
print("測試完成")
print("="*60)
