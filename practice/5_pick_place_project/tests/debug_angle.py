"""
角度檢測調試腳本
幫助理解 OpenCV minAreaRect 的角度定義
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt

def test_angle_detection(true_angle):
    """測試特定角度的檢測準確度"""
    print(f"\n{'='*60}")
    print(f"測試角度: {true_angle}°")
    print(f"{'='*60}")

    # 正規化輸入角度到 [0, 360)
    normalized_true_angle = true_angle % 360

    # 創建旋轉矩形
    img = np.zeros((500, 500), dtype=np.uint8)
    center = (250, 250)
    size = (150, 80)  # 寬 > 高

    rect = (center, size, true_angle)
    box = cv2.boxPoints(rect)
    box = np.int32(box)
    cv2.drawContours(img, [box], 0, 255, -1)

    # 檢測
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detected_rect = cv2.minAreaRect(contours[0])

    det_center, det_size, det_angle = detected_rect

    print(f"\nOpenCV 原始輸出:")
    print(f"  size: ({det_size[0]:.1f}, {det_size[1]:.1f})")
    print(f"  angle: {det_angle:.2f}°")

    # 方法 1: 簡單正規化
    width, height = det_size
    if width < height:
        normalized_angle1 = 90 + det_angle
    else:
        normalized_angle1 = det_angle % 360

    # 方法 2: 更精確的正規化
    # 確保角度在 [0, 360) 範圍
    if det_angle < 0:
        normalized_angle2 = det_angle + 360
    else:
        normalized_angle2 = det_angle

    # 如果寬高交換了，需要旋轉 90 度
    if width < height:
        normalized_angle2 = (normalized_angle2 + 90) % 360

    # 方法 3: OpenCV 原始 + 寬高調整（最準確）
    angle_from_points = det_angle

    # 處理寬高
    if width < height:
        angle_from_points = 90 + det_angle

    # 正規化到 [0, 360)
    if angle_from_points < 0:
        angle_from_points += 360

    # 對所有方法應用 180° 模糊性修正
    def fix_180_ambiguity(angle, true_angle):
        """修正 180° 方向模糊性"""
        error = abs(angle - true_angle)
        if error > 90:
            # 嘗試翻轉 180°
            angle_flipped = (angle + 180) % 360
            error_flipped = abs(angle_flipped - true_angle)
            if error_flipped < error:
                return angle_flipped, error_flipped
        return angle, error

    normalized_angle1, error1 = fix_180_ambiguity(normalized_angle1, normalized_true_angle)
    normalized_angle2, error2 = fix_180_ambiguity(normalized_angle2, normalized_true_angle)
    angle_from_points, error3 = fix_180_ambiguity(angle_from_points, normalized_true_angle)

    print(f"\n檢測結果比較:")
    print(f"  實際角度:          {true_angle:.2f}° (正規化: {normalized_true_angle:.2f}°)")
    print(f"  方法1 (簡單):      {normalized_angle1:.2f}°  (誤差: {error1:.2f}°)")
    print(f"  方法2 (精確):      {normalized_angle2:.2f}°  (誤差: {error2:.2f}°)")
    print(f"  方法3 (正確方法):  {angle_from_points:.2f}°  (誤差: {error3:.2f}°)")

    # 視覺化
    result = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # 繪製檢測到的矩形
    detected_box = cv2.boxPoints(detected_rect)
    detected_box = np.int32(detected_box)
    cv2.drawContours(result, [detected_box], 0, (0, 255, 0), 2)

    # 標記四個角點
    for i, pt in enumerate(detected_box):
        color = [(255, 0, 0), (0, 255, 255), (255, 0, 255), (0, 128, 255)][i]
        cv2.circle(result, tuple(pt), 8, color, -1)
        cv2.putText(result, f'P{i}', tuple(pt + 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # 繪製方向箭頭（使用方法3的角度）
    arrow_len = 80
    end_x = int(center[0] + arrow_len * np.cos(np.radians(angle_from_points)))
    end_y = int(center[1] + arrow_len * np.sin(np.radians(angle_from_points)))
    cv2.arrowedLine(result, center, (end_x, end_y), (255, 255, 0), 3)

    # 使用已經修正過的誤差
    error = error3

    # 顯示資訊
    cv2.putText(result, f'True: {true_angle:.0f}deg',
               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(result, f'Detected: {angle_from_points:.1f}deg',
               (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(result, f'Error: {error:.1f}deg',
               (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return result, angle_from_points, error


def main():
    """測試多個角度"""
    print("="*60)
    print("OpenCV 角度檢測調試工具")
    print("="*60)

    # 測試角度
    test_angles = [0, 15, 30, 45, 60, 75, 90, 120, 180, -30, -45]

    results = []
    detected_angles = []
    errors = []

    for angle in test_angles:
        result, detected, error = test_angle_detection(angle)
        results.append(result)
        detected_angles.append(detected)
        errors.append(error)

    # 顯示摘要
    print(f"\n{'='*60}")
    print("檢測摘要")
    print(f"{'='*60}")
    print(f"{'實際角度':<15} {'檢測角度':<15} {'誤差':<15} {'狀態'}")
    print("-"*60)
    for true, detected, error in zip(test_angles, detected_angles, errors):
        normalized_true = true % 360
        status = "OK" if error < 1.0 else "FAIL"
        print(f"{true:<15.1f} {detected:<15.2f} {error:<15.2f} {status}")

    # 視覺化前 6 個結果
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    for i in range(min(6, len(results))):
        axes[i].imshow(cv2.cvtColor(results[i], cv2.COLOR_BGR2RGB))
        axes[i].set_title(f'True: {test_angles[i]}°, Detected: {detected_angles[i]:.1f}°')
        axes[i].axis('off')

    plt.tight_layout()

    # 儲存
    output_path = r'C:\Users\Liily.Chen\Desktop\computer-vision-application\practice\5_pick_place_project\angle_debug_results.png'
    plt.savefig(output_path, dpi=100)
    print(f"\n結果已儲存: {output_path}")

    plt.show()

    print("\n建議:")
    print("1. 如果誤差很大，考慮使用角點方法（方法3）")
    print("2. 對於矩形物件，minAreaRect 通常很準確")
    print("3. 對於非矩形物件，考慮使用 PCA 或輪廓分析")


if __name__ == "__main__":
    main()
