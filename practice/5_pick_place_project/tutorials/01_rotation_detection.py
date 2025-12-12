"""
物件旋轉角度檢測練習
Object Rotation Detection for Pick and Place

學習目標：
1. 使用 OpenCV 檢測物件旋轉角度
2. 計算需要補償的旋轉角度
3. 輸出給機械手臂使用的角度資訊
4. 處理不同形狀的物件
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib import font_manager
import os

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 設定基礎路徑
BASE_PATH = r'C:\Users\Liily.Chen\Desktop\computer-vision-application\practice\5_pick_place_project'
os.makedirs(BASE_PATH, exist_ok=True)

# ============================================
# 第一部分：矩形物件旋轉角度檢測
# ============================================

def create_rotated_rectangle(angle):
    """創建一個旋轉的矩形測試影像"""
    # 創建黑色背景
    img = np.zeros((500, 500), dtype=np.uint8)

    # 矩形中心點
    center = (250, 250)

    # 矩形尺寸 (寬, 高)
    size = (150, 80)

    # 創建旋轉矩形
    rect = (center, size, angle)
    box = cv2.boxPoints(rect)
    box = np.int32(box)

    # 繪製矩形
    cv2.drawContours(img, [box], 0, 255, -1)

    return img, rect, box


def detect_rectangle_rotation(img):
    """
    檢測矩形物件的旋轉角度

    返回：
    - angle: 旋轉角度（度）
    - center: 物件中心座標
    - box: 最小外接矩形的四個角點
    """
    print("=" * 60)
    print("矩形旋轉角度檢測")
    print("=" * 60)

    # 尋找輪廓
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        print("[Error] 沒有找到物件！")
        return None, None, None

    # 取最大輪廓
    largest_contour = max(contours, key=cv2.contourArea)

    # 方法1：使用 minAreaRect（最小面積矩形）
    rect = cv2.minAreaRect(largest_contour)
    center, size, angle = rect

    # OpenCV minAreaRect 的角度處理
    # angle 範圍: [-90, 0) 或 [0, 90)
    # size[0] 是第一條邊, size[1] 是第二條邊
    width, height = size

    # 如果寬度 < 高度，表示矩形被旋轉了 90 度
    if width < height:
        angle = 90 + angle

    # 正規化到 [0, 360) 範圍
    if angle < 0:
        angle += 360

    # 獲取矩形的四個角點
    box = cv2.boxPoints(rect)
    box = np.int32(box)

    print(f"[OK]  檢測結果：")
    print(f"   物件中心：({center[0]:.1f}, {center[1]:.1f})")
    print(f"   物件尺寸：{size[0]:.1f} x {size[1]:.1f} pixels")
    print(f"   旋轉角度：{angle:.2f}°")

    return angle, center, box


def calculate_gripper_rotation(detected_angle, reference_angle=0):
    """
    計算機械手臂夾爪需要旋轉的角度

    參數：
    - detected_angle: 檢測到的物件旋轉角度
    - reference_angle: 參考角度（物件應該在的角度）

    返回：
    - compensation_angle: 需要補償的角度
    """
    # 計算需要旋轉的角度（最短路徑）
    compensation_angle = detected_angle - reference_angle

    # 正規化到 [-180, 180] 範圍
    while compensation_angle > 180:
        compensation_angle -= 360
    while compensation_angle < -180:
        compensation_angle += 360

    return compensation_angle


# ============================================
# 第二部分：複雜形狀的旋轉角度檢測
# ============================================

def create_complex_shape(angle):
    """創建一個複雜形狀（L型）的測試影像"""
    img = np.zeros((500, 500), dtype=np.uint8)

    center = np.array([250, 250])

    # 定義 L 型的點（相對於中心）
    points = np.array([
        [-60, -60],
        [60, -60],
        [60, -20],
        [20, -20],
        [20, 60],
        [-60, 60]
    ], dtype=np.float32)

    # 旋轉矩陣
    angle_rad = np.radians(angle)
    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad), np.cos(angle_rad)]
    ])

    # 旋轉點
    rotated_points = points @ rotation_matrix.T
    rotated_points += center
    rotated_points = rotated_points.astype(np.int32)

    # 繪製形狀
    cv2.fillPoly(img, [rotated_points], 255)

    return img, rotated_points


def detect_complex_shape_rotation(img):
    """
    檢測複雜形狀的旋轉角度
    使用 PCA (主成分分析) 方法
    """
    print("\n" + "=" * 60)
    print("複雜形狀旋轉角度檢測（使用 PCA）")
    print("=" * 60)

    # 尋找輪廓
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return None, None, None

    largest_contour = max(contours, key=cv2.contourArea)

    # 計算質心
    M = cv2.moments(largest_contour)
    if M["m00"] == 0:
        return None, None, None

    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    center = (cx, cy)

    # 使用 PCA 找主軸方向
    # 將輪廓點轉換為適合 PCA 的格式
    pts = largest_contour.reshape(-1, 2).astype(np.float32)

    # 計算協方差矩陣和特徵向量
    mean, eigenvectors = cv2.PCACompute(pts, mean=None)

    # 主軸方向（第一個特徵向量）
    main_direction = eigenvectors[0]

    # 計算角度
    angle = np.degrees(np.arctan2(main_direction[1], main_direction[0]))

    # 正規化角度到 [0, 360)
    if angle < 0:
        angle += 360

    # 計算主軸的端點用於視覺化
    length = 100
    p1 = (int(cx + length * main_direction[0]), int(cy + length * main_direction[1]))
    p2 = (int(cx - length * main_direction[0]), int(cy - length * main_direction[1]))

    print(f"[OK]  檢測結果：")
    print(f"   物件中心：({cx}, {cy})")
    print(f"   主軸角度：{angle:.2f}°")
    print(f"   主軸方向向量：({main_direction[0]:.3f}, {main_direction[1]:.3f})")

    return angle, center, (p1, p2)


# ============================================
# 第三部分：使用特徵點檢測旋轉
# ============================================

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

    # 添加標記點（表示物件的"前方"）
    angle_rad = np.radians(angle)
    marker_offset = np.array([90, 0])  # 標記在右側（增加距離確保在矩形外）

    # 旋轉標記位置
    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad), np.cos(angle_rad)]
    ])

    marker_pos = center + marker_offset @ rotation_matrix.T
    cv2.circle(img, tuple(marker_pos.astype(int)), 10, 255, -1)

    return img, marker_pos


def detect_rotation_with_markers(img):
    """使用標記點檢測旋轉角度"""
    print("\n" + "=" * 60)
    print("使用標記點檢測旋轉角度")
    print("=" * 60)

    # 尋找所有輪廓
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) < 2:
        print("[Error] 找不到物件或標記點！")
        return None, None, None

    # 依據面積排序
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # 最大的是主體
    main_body = contours[0]
    M = cv2.moments(main_body)
    body_cx = int(M["m10"] / M["m00"])
    body_cy = int(M["m01"] / M["m00"])
    body_center = np.array([body_cx, body_cy])

    # 第二大的是標記
    marker = contours[1]
    M_marker = cv2.moments(marker)
    marker_cx = int(M_marker["m10"] / M_marker["m00"])
    marker_cy = int(M_marker["m01"] / M_marker["m00"])
    marker_center = np.array([marker_cx, marker_cy])

    # 計算從物體中心到標記的向量
    direction_vector = marker_center - body_center

    # 計算角度
    angle = np.degrees(np.arctan2(direction_vector[1], direction_vector[0]))

    # 正規化到 [0, 360)
    if angle < 0:
        angle += 360

    print(f"[OK]  檢測結果：")
    print(f"   物件中心：({body_cx}, {body_cy})")
    print(f"   標記位置：({marker_cx}, {marker_cy})")
    print(f"   旋轉角度：{angle:.2f}°")

    return angle, (body_cx, body_cy), (marker_cx, marker_cy)


# ============================================
# 第四部分：機器人指令生成
# ============================================

def generate_robot_command(center, angle, gripper_rotation):
    """
    生成機械手臂的指令

    返回機械手臂需要的資訊：
    - 位置 (x, y)
    - 旋轉角度
    - 抓取指令
    """
    print("\n" + "=" * 60)
    print("[Robot] 機械手臂指令")
    print("=" * 60)

    # 假設相機座標到機器人座標的轉換
    # 這裡做簡單示範，實際應用需要相機標定
    PIXEL_TO_MM = 0.1  # 1 pixel = 0.1 mm

    # 座標轉換（相機中心為原點）
    robot_x = (center[0] - 250) * PIXEL_TO_MM
    robot_y = (250 - center[1]) * PIXEL_TO_MM  # Y軸反向

    print(f"[Position] 抓取位置：")
    print(f"   X = {robot_x:6.2f} mm")
    print(f"   Y = {robot_y:6.2f} mm")
    print(f"   Z = 0.00 mm  (高度由機器人控制)")

    print(f"\n [Rotation] 旋轉角度：")
    print(f"   物件角度 = {angle:.2f}°")
    print(f"   夾爪補償 = {gripper_rotation:.2f}°")
    print(f"   最終角度 = {(angle + gripper_rotation) % 360:.2f}°")

    print(f"\n[Get] 抓取指令：")
    print(f"   MOVE_TO({robot_x:.2f}, {robot_y:.2f}, 50.0)  # 移動到物件上方")
    print(f"   ROTATE_GRIPPER({gripper_rotation:.2f})       # 旋轉夾爪對齊")
    print(f"   MOVE_TO({robot_x:.2f}, {robot_y:.2f}, 0.0)   # 下降到抓取高度")
    print(f"   CLOSE_GRIPPER()                               # 關閉夾爪")
    print(f"   MOVE_TO({robot_x:.2f}, {robot_y:.2f}, 50.0)  # 提升物件")

    # 返回指令字典
    command = {
        "position": {"x": robot_x, "y": robot_y, "z": 0.0},
        "rotation": gripper_rotation,
        "action": "pick",
        "object_angle": angle
    }

    return command


# ============================================
# 第五部分：完整示範
# ============================================

def demo_rotation_detection():
    """完整的旋轉檢測示範"""
    print("\n" + "=" * 60)
    print("[Target] 物件旋轉角度檢測完整示範")
    print("=" * 60 + "\n")

    # 測試角度
    test_angles = [0, 30, 45, -60, 90]

    fig, axes = plt.subplots(3, len(test_angles), figsize=(20, 12))

    for idx, angle in enumerate(test_angles):
        print(f"\n{'='*60}")
        print(f"測試案例 {idx+1}: 旋轉 {angle}°")
        print(f"{'='*60}")

        # ===== 矩形檢測 =====
        img1, _, _ = create_rotated_rectangle(angle)
        detected_angle1, center1, box1 = detect_rectangle_rotation(img1)

        # 計算夾爪旋轉
        if detected_angle1 is not None:
            gripper_rot = calculate_gripper_rotation(detected_angle1, reference_angle=0)
            print(f"   ➡️  夾爪需要旋轉：{gripper_rot:.2f}°")

        # 視覺化
        result1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
        if box1 is not None:
            cv2.drawContours(result1, [box1], 0, (0, 255, 0), 2)
            cv2.circle(result1, (int(center1[0]), int(center1[1])), 5, (0, 0, 255), -1)

            # 繪製角度指示線
            angle_rad = np.radians(detected_angle1)
            line_length = 80
            end_x = int(center1[0] + line_length * np.cos(angle_rad))
            end_y = int(center1[1] + line_length * np.sin(angle_rad))
            cv2.arrowedLine(result1,
                          (int(center1[0]), int(center1[1])),
                          (end_x, end_y),
                          (255, 0, 0), 2)

        axes[0, idx].imshow(cv2.cvtColor(result1, cv2.COLOR_BGR2RGB))
        title1 = f'矩形\n實際:{angle}° 檢測:{detected_angle1:.1f}°' if detected_angle1 is not None else f'矩形\n實際:{angle}° 檢測:失敗'
        axes[0, idx].set_title(title1)
        axes[0, idx].axis('off')

        # ===== 複雜形狀檢測 =====
        img2, _ = create_complex_shape(angle)
        detected_angle2, center2, axis_line = detect_complex_shape_rotation(img2)

        result2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
        if axis_line is not None:
            cv2.circle(result2, center2, 5, (0, 0, 255), -1)
            cv2.line(result2, axis_line[0], axis_line[1], (0, 255, 0), 2)

        axes[1, idx].imshow(cv2.cvtColor(result2, cv2.COLOR_BGR2RGB))
        title2 = f'L型(PCA)\n實際:{angle}° 檢測:{detected_angle2:.1f}°' if detected_angle2 is not None else f'L型(PCA)\n實際:{angle}° 檢測:失敗'
        axes[1, idx].set_title(title2)
        axes[1, idx].axis('off')

        # ===== 標記點檢測 =====
        img3, _ = create_shape_with_markers(angle)
        detected_angle3, body_center, marker_pos = detect_rotation_with_markers(img3)

        result3 = cv2.cvtColor(img3, cv2.COLOR_GRAY2BGR)
        if body_center is not None:
            cv2.circle(result3, body_center, 5, (0, 0, 255), -1)
            cv2.circle(result3, marker_pos, 5, (255, 0, 0), -1)
            cv2.line(result3, body_center, marker_pos, (0, 255, 0), 2)

        axes[2, idx].imshow(cv2.cvtColor(result3, cv2.COLOR_BGR2RGB))
        title3 = f'標記點法\n實際:{angle}° 檢測:{detected_angle3:.1f}°' if detected_angle3 is not None else f'標記點法\n實際:{angle}° 檢測:失敗'
        axes[2, idx].set_title(title3)
        axes[2, idx].axis('off')

    plt.suptitle('三種旋轉角度檢測方法比較', fontsize=16, fontweight='bold')
    plt.tight_layout()

    # 儲存圖片
    output_path = os.path.join(BASE_PATH, 'rotation_detection_demo.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n[OK]  結果已儲存到: {output_path}")
    plt.show()

    # 生成機器人指令範例
    print("\n" + "=" * 60)
    print("生成機器人指令範例")
    print("=" * 60)

    test_img, _, _ = create_rotated_rectangle(37)
    angle, center, box = detect_rectangle_rotation(test_img)

    if angle is not None:
        gripper_rotation = calculate_gripper_rotation(angle, reference_angle=0)
        command = generate_robot_command(center, angle, gripper_rotation)
        print(f"\n[Commad] 指令字典：")
        print(f"{command}")


# ============================================
# 練習題
# ============================================

def exercises():
    """練習題"""
    print("\n" + "=" * 60)
    print("[Practice]  練習題")
    print("=" * 60)

    print("""
    練習 1: 多物件檢測
    - 創建包含多個旋轉物件的影像
    - 檢測每個物件的位置和角度
    - 規劃抓取順序（由近到遠）

    練習 2: 實時影片處理
    - 使用 Webcam 拍攝旋轉的物件
    - 實時顯示檢測到的角度
    - 加上 Kalman Filter 平滑角度變化

    練習 3: 不規則形狀
    - 檢測非對稱物件的方向
    - 使用輪廓特徵（長寬比、凸包等）
    - 判斷最佳抓取點和角度

    練習 4: 相機標定
    - 使用棋盤格進行相機標定
    - 計算相機內參和畸變係數
    - 實現準確的像素到機器人座標轉換

    練習 5: 整合到你的 AOI 系統
    - 在現有的 AOI 系統中加入角度檢測
    - 將檢測結果傳送給機械手臂模擬器
    - 讓機械手臂根據角度調整抓取姿態
    """)


# ============================================
# 主程式
# ============================================

if __name__ == "__main__":
    print("物件旋轉角度檢測教學")
    print("Object Rotation Detection for Robotic Pick and Place\n")

    # 執行完整示範
    demo_rotation_detection()

    # 顯示練習題
    exercises()

    print("\n" + "=" * 60)
    print("[OK]  教學完成！")
    print("=" * 60)
    print("\n下一步：")
    print("1. 嘗試練習題")
    print("2. 整合到你的 AOI 系統")
    print("3. 學習 Drake 進行機械手臂運動規劃")
