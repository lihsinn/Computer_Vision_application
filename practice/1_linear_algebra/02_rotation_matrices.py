"""
線性代數進階 - 旋轉矩陣
適用於 AOI/上位機開發

學習目標：
1. 理解旋轉矩陣的原理
2. 掌握 2D 和 3D 旋轉
3. 應用於影像對齊和機械手臂控制
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d import Axes3D

# ============================================
# 第一部分：2D 旋轉矩陣
# ============================================

def rotation_matrix_2d(angle_degrees):
    """
    創建 2D 旋轉矩陣

    參數:
        angle_degrees: 旋轉角度（度）

    返回:
        2×2 旋轉矩陣
    """
    angle_rad = np.radians(angle_degrees)
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)

    R = np.array([[cos_a, -sin_a],
                  [sin_a,  cos_a]])

    return R


def demonstrate_2d_rotation():
    """示範 2D 旋轉"""
    print("=" * 50)
    print("2D 旋轉矩陣")
    print("=" * 50)

    # 原始點
    point = np.array([4, 0])
    print(f"原始點: {point}")

    # 旋轉 45 度
    R_45 = rotation_matrix_2d(45)
    print(f"\n旋轉矩陣 (45度):\n{R_45}")

    rotated_45 = np.dot(R_45, point)
    print(f"旋轉 45 度後: {rotated_45}")
    print(f"長度保持不變: {np.linalg.norm(point):.4f} -> {np.linalg.norm(rotated_45):.4f}")

    # 旋轉 90 度
    R_90 = rotation_matrix_2d(90)
    rotated_90 = np.dot(R_90, point)
    print(f"\n旋轉 90 度後: {rotated_90}")

    # 旋轉 180 度
    R_180 = rotation_matrix_2d(180)
    rotated_180 = np.dot(R_180, point)
    print(f"旋轉 180 度後: {rotated_180}")

    # 旋轉矩陣性質：R^T = R^(-1)
    print(f"\n旋轉矩陣性質驗證:")
    print(f"R × R^T = I (單位矩陣):\n{np.dot(R_45, R_45.T)}")
    print(f"行列式 det(R) = 1: {np.linalg.det(R_45):.4f}")

    return R_45, rotated_45


def visualize_2d_rotation():
    """視覺化 2D 旋轉"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 左圖：旋轉點
    ax1 = axes[0]
    point = np.array([3, 1])

    # 繪製不同角度的旋轉
    angles = [0, 30, 60, 90, 120, 150, 180]
    colors = plt.cm.rainbow(np.linspace(0, 1, len(angles)))

    for i, angle in enumerate(angles):
        R = rotation_matrix_2d(angle)
        rotated = np.dot(R, point)
        ax1.arrow(0, 0, rotated[0], rotated[1], head_width=0.2, head_length=0.2,
                 fc=colors[i], ec=colors[i], label=f'{angle}°')
        ax1.plot(rotated[0], rotated[1], 'o', color=colors[i], markersize=8)

    # 繪製圓形軌跡
    circle = plt.Circle((0, 0), np.linalg.norm(point), fill=False, linestyle='--', color='gray')
    ax1.add_patch(circle)

    ax1.set_xlim(-4, 4)
    ax1.set_ylim(-4, 4)
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper right', fontsize=8)
    ax1.set_title('點的旋轉')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')

    # 右圖：旋轉矩形（模擬工件）
    ax2 = axes[1]

    # 矩形的四個角點
    rect_points = np.array([[0, 0],
                           [2, 0],
                           [2, 1],
                           [0, 1]]).T

    # 原始矩形
    ax2.plot(rect_points[0, :], rect_points[1, :], 'b-o', label='原始', linewidth=2)

    # 旋轉後的矩形
    R = rotation_matrix_2d(30)
    rotated_rect = np.dot(R, rect_points)
    ax2.plot(rotated_rect[0, :], rotated_rect[1, :], 'r-o', label='旋轉 30°', linewidth=2)

    ax2.set_xlim(-1, 3)
    ax2.set_ylim(-1, 3)
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_title('矩形旋轉（模擬工件對齊）')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\1_linear_algebra\\2d_rotation.png', dpi=100)
    print("\n2D 旋轉視覺化已儲存: 2d_rotation.png")
    plt.close()


# ============================================
# 第二部分：3D 旋轉矩陣
# ============================================

def rotation_matrix_x(angle_degrees):
    """繞 X 軸旋轉"""
    angle_rad = np.radians(angle_degrees)
    return np.array([[1, 0, 0],
                     [0, np.cos(angle_rad), -np.sin(angle_rad)],
                     [0, np.sin(angle_rad),  np.cos(angle_rad)]])


def rotation_matrix_y(angle_degrees):
    """繞 Y 軸旋轉"""
    angle_rad = np.radians(angle_degrees)
    return np.array([[ np.cos(angle_rad), 0, np.sin(angle_rad)],
                     [ 0, 1, 0],
                     [-np.sin(angle_rad), 0, np.cos(angle_rad)]])


def rotation_matrix_z(angle_degrees):
    """繞 Z 軸旋轉"""
    angle_rad = np.radians(angle_degrees)
    return np.array([[np.cos(angle_rad), -np.sin(angle_rad), 0],
                     [np.sin(angle_rad),  np.cos(angle_rad), 0],
                     [0, 0, 1]])


def demonstrate_3d_rotation():
    """示範 3D 旋轉"""
    print("\n" + "=" * 50)
    print("3D 旋轉矩陣")
    print("=" * 50)

    # 原始點
    point = np.array([1, 0, 0])
    print(f"原始點: {point}")

    # 繞 Z 軸旋轉 90 度
    Rz = rotation_matrix_z(90)
    print(f"\n繞 Z 軸旋轉矩陣 (90度):\n{Rz}")
    rotated_z = np.dot(Rz, point)
    print(f"旋轉後: {rotated_z}")

    # 繞 Y 軸旋轉 90 度
    Ry = rotation_matrix_y(90)
    print(f"\n繞 Y 軸旋轉矩陣 (90度):\n{Ry}")
    rotated_y = np.dot(Ry, point)
    print(f"旋轉後: {rotated_y}")

    # 組合旋轉：先繞 Z 再繞 Y
    R_combined = np.dot(Ry, Rz)
    print(f"\n組合旋轉矩陣 (先 Z 後 Y):\n{R_combined}")
    rotated_combined = np.dot(R_combined, point)
    print(f"組合旋轉後: {rotated_combined}")

    # 注意：旋轉順序很重要！
    R_reversed = np.dot(Rz, Ry)
    rotated_reversed = np.dot(R_reversed, point)
    print(f"\n反向組合 (先 Y 後 Z):\n{R_reversed}")
    print(f"反向組合旋轉後: {rotated_reversed}")
    print(f"兩個結果相同嗎？ {np.allclose(rotated_combined, rotated_reversed)}")

    return Rz, Ry, R_combined


def visualize_3d_rotation():
    """視覺化 3D 旋轉"""
    fig = plt.figure(figsize=(15, 5))

    # 原始座標軸
    origin = np.array([0, 0, 0])
    x_axis = np.array([1, 0, 0])
    y_axis = np.array([0, 1, 0])
    z_axis = np.array([0, 0, 1])

    # 繞 Z 軸旋轉
    ax1 = fig.add_subplot(131, projection='3d')
    Rz = rotation_matrix_z(45)
    draw_axes(ax1, origin, x_axis, y_axis, z_axis, 'Original')
    draw_axes(ax1, origin, np.dot(Rz, x_axis), np.dot(Rz, y_axis), np.dot(Rz, z_axis),
             'Rotated', linestyle='--')
    ax1.set_title('繞 Z 軸旋轉 45°')

    # 繞 Y 軸旋轉
    ax2 = fig.add_subplot(132, projection='3d')
    Ry = rotation_matrix_y(45)
    draw_axes(ax2, origin, x_axis, y_axis, z_axis, 'Original')
    draw_axes(ax2, origin, np.dot(Ry, x_axis), np.dot(Ry, y_axis), np.dot(Ry, z_axis),
             'Rotated', linestyle='--')
    ax2.set_title('繞 Y 軸旋轉 45°')

    # 繞 X 軸旋轉
    ax3 = fig.add_subplot(133, projection='3d')
    Rx = rotation_matrix_x(45)
    draw_axes(ax3, origin, x_axis, y_axis, z_axis, 'Original')
    draw_axes(ax3, origin, np.dot(Rx, x_axis), np.dot(Rx, y_axis), np.dot(Rx, z_axis),
             'Rotated', linestyle='--')
    ax3.set_title('繞 X 軸旋轉 45°')

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\1_linear_algebra\\3d_rotation.png', dpi=100)
    print("\n3D 旋轉視覺化已儲存: 3d_rotation.png")
    plt.close()


def draw_axes(ax, origin, x, y, z, label, linestyle='-'):
    """繪製 3D 座標軸"""
    ax.quiver(*origin, *x, color='r', arrow_length_ratio=0.1, linestyle=linestyle, linewidth=2)
    ax.quiver(*origin, *y, color='g', arrow_length_ratio=0.1, linestyle=linestyle, linewidth=2)
    ax.quiver(*origin, *z, color='b', arrow_length_ratio=0.1, linestyle=linestyle, linewidth=2)
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')


# ============================================
# 第三部分：歐拉角與旋轉向量
# ============================================

def euler_angles_to_rotation_matrix(roll, pitch, yaw):
    """
    歐拉角轉旋轉矩陣 (ZYX 順序)

    參數:
        roll: 繞 X 軸旋轉角度（度）
        pitch: 繞 Y 軸旋轉角度（度）
        yaw: 繞 Z 軸旋轉角度（度）

    返回:
        3×3 旋轉矩陣
    """
    Rx = rotation_matrix_x(roll)
    Ry = rotation_matrix_y(pitch)
    Rz = rotation_matrix_z(yaw)

    # 注意順序：先 yaw(Z), 再 pitch(Y), 最後 roll(X)
    R = np.dot(Rz, np.dot(Ry, Rx))
    return R


def rotation_matrix_to_euler_angles(R):
    """
    旋轉矩陣轉歐拉角

    參數:
        R: 3×3 旋轉矩陣

    返回:
        (roll, pitch, yaw) 歐拉角（度）
    """
    sy = np.sqrt(R[0, 0]**2 + R[1, 0]**2)

    singular = sy < 1e-6

    if not singular:
        roll = np.arctan2(R[2, 1], R[2, 2])
        pitch = np.arctan2(-R[2, 0], sy)
        yaw = np.arctan2(R[1, 0], R[0, 0])
    else:
        roll = np.arctan2(-R[1, 2], R[1, 1])
        pitch = np.arctan2(-R[2, 0], sy)
        yaw = 0

    return np.degrees(roll), np.degrees(pitch), np.degrees(yaw)


def demonstrate_euler_angles():
    """示範歐拉角"""
    print("\n" + "=" * 50)
    print("歐拉角與旋轉矩陣")
    print("=" * 50)

    # 歐拉角
    roll = 30
    pitch = 45
    yaw = 60
    print(f"歐拉角 (Roll, Pitch, Yaw): ({roll}°, {pitch}°, {yaw}°)")

    # 轉換為旋轉矩陣
    R = euler_angles_to_rotation_matrix(roll, pitch, yaw)
    print(f"\n旋轉矩陣:\n{R}")

    # 轉回歐拉角
    roll_back, pitch_back, yaw_back = rotation_matrix_to_euler_angles(R)
    print(f"\n轉回歐拉角: ({roll_back:.2f}°, {pitch_back:.2f}°, {yaw_back:.2f}°)")

    # 驗證
    print(f"轉換誤差: Roll={abs(roll-roll_back):.6f}°, "
          f"Pitch={abs(pitch-pitch_back):.6f}°, Yaw={abs(yaw-yaw_back):.6f}°")

    return R


# ============================================
# 第四部分：實際應用
# ============================================

def aoi_image_alignment():
    """AOI 影像對齊應用"""
    print("\n" + "=" * 50)
    print("AOI 應用：影像對齊")
    print("=" * 50)

    # 模擬：檢測到的 Fiducial Mark（定位標記）位置
    template_marks = np.array([[100, 100],   # 理想位置
                              [500, 100]])

    detected_marks = np.array([[120, 110],   # 實際檢測位置（有偏移和旋轉）
                              [510, 130]])

    print(f"模板標記位置:\n{template_marks}")
    print(f"檢測到的標記位置:\n{detected_marks}")

    # 計算中心點
    template_center = np.mean(template_marks, axis=0)
    detected_center = np.mean(detected_marks, axis=0)

    print(f"\n模板中心: {template_center}")
    print(f"檢測中心: {detected_center}")

    # 計算旋轉角度
    template_vec = template_marks[1] - template_marks[0]
    detected_vec = detected_marks[1] - detected_marks[0]

    template_angle = np.arctan2(template_vec[1], template_vec[0])
    detected_angle = np.arctan2(detected_vec[1], detected_vec[0])
    rotation_angle = detected_angle - template_angle

    print(f"\n需要旋轉角度: {np.degrees(rotation_angle):.2f}°")
    print(f"需要平移: {detected_center - template_center}")

    # 創建校正變換
    R = rotation_matrix_2d(np.degrees(-rotation_angle))
    print(f"\n校正旋轉矩陣:\n{R}")

    return R, template_center, detected_center


def robot_arm_orientation():
    """機械手臂姿態控制"""
    print("\n" + "=" * 50)
    print("機械手臂應用：末端執行器姿態")
    print("=" * 50)

    # 目標姿態（歐拉角）
    target_roll = 0
    target_pitch = 0
    target_yaw = 90

    print(f"目標姿態 (Roll, Pitch, Yaw): ({target_roll}°, {target_pitch}°, {target_yaw}°)")

    # 轉換為旋轉矩陣（用於控制器）
    R_target = euler_angles_to_rotation_matrix(target_roll, target_pitch, target_yaw)
    print(f"\n目標旋轉矩陣:\n{R_target}")

    # 當前姿態
    current_roll = 10
    current_pitch = 5
    current_yaw = 85
    print(f"\n當前姿態: ({current_roll}°, {current_pitch}°, {current_yaw}°)")

    R_current = euler_angles_to_rotation_matrix(current_roll, current_pitch, current_yaw)

    # 計算需要的旋轉（誤差）
    R_error = np.dot(R_target, R_current.T)
    error_roll, error_pitch, error_yaw = rotation_matrix_to_euler_angles(R_error)

    print(f"\n姿態誤差: ({error_roll:.2f}°, {error_pitch:.2f}°, {error_yaw:.2f}°)")

    return R_target, R_current, R_error


# ============================================
# 練習題
# ============================================

def exercises():
    """練習題"""
    print("\n" + "=" * 50)
    print("練習題")
    print("=" * 50)

    print("""
    練習 1: 計算旋轉角度
    - 兩個向量 v1 = [1, 0] 和 v2 = [0.707, 0.707]
    - 計算從 v1 旋轉到 v2 需要多少度
    - 驗證：用旋轉矩陣將 v1 旋轉後是否得到 v2

    練習 2: 影像校正
    - 影像上一條直線從 (100, 100) 到 (300, 150)
    - 理想上這條線應該是水平的
    - 計算需要旋轉多少度來校正
    - 應用旋轉後計算新的端點座標

    練習 3: 3D 姿態變換
    - 給定歐拉角 (30°, 45°, 60°)
    - 轉換為旋轉矩陣
    - 將點 (1, 1, 1) 經過此變換
    - 將結果旋轉矩陣轉回歐拉角驗證

    練習 4: 組合旋轉
    - 先繞 Z 軸旋轉 30°
    - 再繞 Y 軸旋轉 45°
    - 計算組合旋轉矩陣
    - 將其轉換為歐拉角表示
    - 驗證與直接用歐拉角 (0°, 45°, 30°) 的差異

    練習 5: 實際應用
    - 模擬一個 PCB 板在 AOI 設備上偏移了
    - 定位標記理想位置: [(0, 0), (100, 0), (100, 100), (0, 100)]
    - 實際檢測位置: [(5, 3), (103, 8), (98, 105), (-2, 98)]
    - 計算最佳旋轉和平移來對齊（提示：使用最小二乘法）
    """)

    # 練習解答區
    print("\n# 練習 1 解答：")
    v1 = np.array([1, 0])
    v2 = np.array([0.707, 0.707])
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
    print("線性代數進階教學 - 旋轉矩陣\n")

    # 執行所有示範
    demonstrate_2d_rotation()
    visualize_2d_rotation()
    demonstrate_3d_rotation()
    visualize_3d_rotation()
    demonstrate_euler_angles()
    aoi_image_alignment()
    robot_arm_orientation()
    exercises()

    print("\n" + "=" * 50)
    print("教學完成！")
    print("=" * 50)
    print("\n下一步：學習 03_homogeneous_transforms.py（齊次變換）")
