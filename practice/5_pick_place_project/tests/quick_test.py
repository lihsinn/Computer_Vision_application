"""
快速測試腳本
Quick Test for Rotation Detection
"""

import numpy as np
import cv2
import sys
import os

# Windows 編碼設定
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def quick_test():
    """快速測試單一角度檢測"""
    print("快速旋轉角度檢測測試")
    print("=" * 60)

    # 創建測試影像（旋轉 37 度）
    test_angle = 37.0
    print(f"\n創建測試影像：旋轉 {test_angle}°")

    img = np.zeros((500, 500), dtype=np.uint8)
    center = (250, 250)
    size = (150, 80)
    rect = (center, size, test_angle)
    box = cv2.boxPoints(rect)
    box = np.int32(box)
    cv2.drawContours(img, [box], 0, 255, -1)

    # 檢測角度
    print("\n開始檢測...")
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        print("[ERROR] 檢測失敗：找不到物件")
        return

    largest_contour = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(largest_contour)
    center, size, angle = rect

    # 角度正規化
    if size[0] < size[1]:
        angle = angle + 90

    print(f"\n[SUCCESS] 檢測成功！")
    print(f"   實際角度：{test_angle:.2f}°")
    print(f"   檢測角度：{angle:.2f}°")
    print(f"   誤差：{abs(angle - test_angle):.2f}°")

    # 計算機器人需要旋轉的角度
    robot_rotation = angle
    print(f"\n[ROBOT] 機器人指令：")
    print(f"   位置：({center[0]:.1f}, {center[1]:.1f})")
    print(f"   旋轉夾爪：{robot_rotation:.2f}°")

    # 視覺化
    result = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    box = cv2.boxPoints(rect)
    box = np.int32(box)
    cv2.drawContours(result, [box], 0, (0, 255, 0), 2)
    cv2.circle(result, (int(center[0]), int(center[1])), 5, (0, 0, 255), -1)

    # 繪製方向箭頭
    angle_rad = np.radians(angle)
    arrow_length = 70
    end_x = int(center[0] + arrow_length * np.cos(angle_rad))
    end_y = int(center[1] + arrow_length * np.sin(angle_rad))
    cv2.arrowedLine(result,
                   (int(center[0]), int(center[1])),
                   (end_x, end_y),
                   (255, 0, 0), 3)

    # 顯示結果
    cv2.putText(result, f'{angle:.1f} deg',
               (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
               1, (255, 255, 255), 2)

    cv2.imshow('Rotation Detection Test', result)
    print("\n按任意鍵關閉視窗...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("\n[OK] 測試完成！")
    print("\n下一步：執行完整示範")
    print("   python 01_rotation_detection.py")


if __name__ == "__main__":
    try:
        quick_test()
    except Exception as e:
        print(f"\n[ERROR] 錯誤：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
