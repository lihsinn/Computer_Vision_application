"""測試負角度修正"""
import numpy as np
import cv2

def test_angle(true_angle):
    """測試單一角度"""
    # 正規化
    normalized_true = true_angle % 360

    # 創建影像
    img = np.zeros((500, 500), dtype=np.uint8)
    center = (250, 250)
    size = (150, 80)
    rect = (center, size, true_angle)
    box = cv2.boxPoints(rect)
    box = np.int32(box)
    cv2.drawContours(img, [box], 0, 255, -1)

    # 檢測
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detected_rect = cv2.minAreaRect(contours[0])
    det_center, det_size, det_angle = detected_rect

    # 方法 3: 正確方法
    width, height = det_size
    if width < height:
        angle = 90 + det_angle
    else:
        angle = det_angle

    if angle < 0:
        angle += 360

    # 180° 模糊性修正
    error = abs(angle - normalized_true)
    if error > 90:
        angle_flipped = (angle + 180) % 360
        error_flipped = abs(angle_flipped - normalized_true)
        if error_flipped < error:
            angle = angle_flipped
            error = error_flipped

    print(f"輸入: {true_angle:6.1f}° | 正規化: {normalized_true:6.1f}° | 檢測: {angle:6.2f}° | 誤差: {error:5.2f}°")

    return error < 1.0

print("="*70)
print("負角度檢測測試")
print("="*70)
print()

test_angles = [0, -30, -45, 15, 30, 45, -60, -90]
all_pass = True

for angle in test_angles:
    passed = test_angle(angle)
    if not passed:
        all_pass = False

print()
if all_pass:
    print("[SUCCESS] 所有測試通過！")
else:
    print("[FAIL] 部分測試失敗")
