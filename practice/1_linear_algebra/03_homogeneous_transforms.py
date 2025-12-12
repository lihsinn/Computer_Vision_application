"""
線性代數進階 - 齊次變換
適用於 AOI/上位機開發

學習目標：
1. 理解齊次座標系統
2. 掌握齊次變換矩陣
3. 應用於複雜的座標變換鏈
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ============================================
# 第一部分：為什麼需要齊次座標
# ============================================

def why_homogeneous_coordinates():
    """解釋為什麼需要齊次座標"""
    print("=" * 50)
    print("為什麼需要齊次座標？")
    print("=" * 50)

    print("""
    問題：用矩陣表示平移

    旋轉可以用矩陣表示：
    [x']   [cos θ  -sin θ] [x]
    [y'] = [sin θ   cos θ] [y]

    但是平移不行：
    [x']   [x]   [tx]
    [y'] = [y] + [ty]  <- 這是加法，不是矩陣乘法！

    解決方案：齊次座標
    - 2D 點 (x, y) -> (x, y, 1)
    - 3D 點 (x, y, z) -> (x, y, z, 1)

    現在可以用矩陣統一表示旋轉和平移：
    [x']   [cos θ  -sin θ  tx] [x]
    [y'] = [sin θ   cos θ  ty] [y]
    [1 ]   [0      0       1 ] [1]
    """)

    # 示範
    print("\n實際示範：")
    point = np.array([10, 20])
    print(f"原始點 (2D): {point}")

    # 轉為齊次座標
    point_h = np.array([10, 20, 1])
    print(f"齊次座標: {point_h}")

    # 平移矩陣
    tx, ty = 5, -3
    T = np.array([[1, 0, tx],
                  [0, 1, ty],
                  [0, 0, 1]])

    print(f"\n平移矩陣:\n{T}")

    # 應用變換
    transformed = np.dot(T, point_h)
    print(f"變換後 (齊次): {transformed}")
    print(f"變換後 (2D): ({transformed[0]}, {transformed[1]})")

    return T, point_h, transformed


# ============================================
# 第二部分：2D 齊次變換矩陣
# ============================================

def create_translation_matrix_2d(tx, ty):
    """創建 2D 平移矩陣"""
    return np.array([[1, 0, tx],
                     [0, 1, ty],
                     [0, 0, 1]])


def create_rotation_matrix_2d_homogeneous(angle_degrees):
    """創建 2D 旋轉矩陣（齊次形式）"""
    angle_rad = np.radians(angle_degrees)
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)

    return np.array([[cos_a, -sin_a, 0],
                     [sin_a,  cos_a, 0],
                     [0,      0,     1]])


def create_scale_matrix_2d(sx, sy):
    """創建 2D 縮放矩陣"""
    return np.array([[sx, 0,  0],
                     [0,  sy, 0],
                     [0,  0,  1]])


def demonstrate_2d_transforms():
    """示範 2D 齊次變換"""
    print("\n" + "=" * 50)
    print("2D 齊次變換矩陣")
    print("=" * 50)

    # 原始點
    point = np.array([100, 100, 1])
    print(f"原始點: ({point[0]}, {point[1]})")

    # 1. 平移
    T = create_translation_matrix_2d(50, -30)
    print(f"\n1. 平移矩陣 (tx=50, ty=-30):\n{T}")
    p1 = np.dot(T, point)
    print(f"   結果: ({p1[0]}, {p1[1]})")

    # 2. 旋轉
    R = create_rotation_matrix_2d_homogeneous(45)
    print(f"\n2. 旋轉矩陣 (45度):\n{R}")
    p2 = np.dot(R, point)
    print(f"   結果: ({p2[0]:.2f}, {p2[1]:.2f})")

    # 3. 縮放
    S = create_scale_matrix_2d(1.5, 0.8)
    print(f"\n3. 縮放矩陣 (sx=1.5, sy=0.8):\n{S}")
    p3 = np.dot(S, point)
    print(f"   結果: ({p3[0]}, {p3[1]})")

    # 4. 組合變換：先旋轉、再縮放、最後平移
    combined = np.dot(T, np.dot(S, R))
    print(f"\n4. 組合變換矩陣 (先旋轉、再縮放、後平移):\n{combined}")
    p4 = np.dot(combined, point)
    print(f"   結果: ({p4[0]:.2f}, {p4[1]:.2f})")

    # 驗證：分步計算應該得到相同結果
    p4_step = np.dot(R, point)
    p4_step = np.dot(S, p4_step)
    p4_step = np.dot(T, p4_step)
    print(f"   驗證（分步）: ({p4_step[0]:.2f}, {p4_step[1]:.2f})")

    return T, R, S, combined


def visualize_2d_homogeneous_transforms():
    """視覺化 2D 齊次變換"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))

    # 原始矩形
    rect = np.array([[0, 0, 1],
                     [2, 0, 1],
                     [2, 1, 1],
                     [0, 1, 1],
                     [0, 0, 1]]).T

    # 1. 平移
    ax1 = axes[0, 0]
    T = create_translation_matrix_2d(1, 0.5)
    rect_t = np.dot(T, rect)
    ax1.plot(rect[0, :], rect[1, :], 'b-', linewidth=2, label='原始')
    ax1.plot(rect_t[0, :], rect_t[1, :], 'r--', linewidth=2, label='平移')
    ax1.set_xlim(-1, 4)
    ax1.set_ylim(-1, 3)
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_title('平移變換')

    # 2. 旋轉（繞原點）
    ax2 = axes[0, 1]
    R = create_rotation_matrix_2d_homogeneous(30)
    rect_r = np.dot(R, rect)
    ax2.plot(rect[0, :], rect[1, :], 'b-', linewidth=2, label='原始')
    ax2.plot(rect_r[0, :], rect_r[1, :], 'r--', linewidth=2, label='旋轉')
    ax2.set_xlim(-1, 3)
    ax2.set_ylim(-1, 3)
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_title('旋轉變換（繞原點）')

    # 3. 繞中心點旋轉
    ax3 = axes[1, 0]
    center = np.array([1, 0.5, 1])  # 矩形中心

    # 步驟：平移到原點 -> 旋轉 -> 平移回去
    T1 = create_translation_matrix_2d(-center[0], -center[1])
    R = create_rotation_matrix_2d_homogeneous(45)
    T2 = create_translation_matrix_2d(center[0], center[1])
    combined = np.dot(T2, np.dot(R, T1))

    rect_rc = np.dot(combined, rect)
    ax3.plot(rect[0, :], rect[1, :], 'b-', linewidth=2, label='原始')
    ax3.plot(rect_rc[0, :], rect_rc[1, :], 'r--', linewidth=2, label='繞中心旋轉')
    ax3.plot(center[0], center[1], 'go', markersize=8, label='旋轉中心')
    ax3.set_xlim(-1, 3)
    ax3.set_ylim(-1, 3)
    ax3.set_aspect('equal')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    ax3.set_title('旋轉變換（繞中心點）')

    # 4. 複雜組合
    ax4 = axes[1, 1]
    T = create_translation_matrix_2d(0.5, 0.3)
    R = create_rotation_matrix_2d_homogeneous(20)
    S = create_scale_matrix_2d(1.2, 0.8)
    complex_transform = np.dot(T, np.dot(R, S))

    rect_c = np.dot(complex_transform, rect)
    ax4.plot(rect[0, :], rect[1, :], 'b-', linewidth=2, label='原始')
    ax4.plot(rect_c[0, :], rect_c[1, :], 'r--', linewidth=2, label='縮放+旋轉+平移')
    ax4.set_xlim(-1, 4)
    ax4.set_ylim(-1, 3)
    ax4.set_aspect('equal')
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    ax4.set_title('組合變換')

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\1_linear_algebra\\homogeneous_2d.png', dpi=100)
    print("\n2D 齊次變換視覺化已儲存: homogeneous_2d.png")
    plt.close()


# ============================================
# 第三部分：3D 齊次變換矩陣
# ============================================

def create_translation_matrix_3d(tx, ty, tz):
    """創建 3D 平移矩陣"""
    return np.array([[1, 0, 0, tx],
                     [0, 1, 0, ty],
                     [0, 0, 1, tz],
                     [0, 0, 0, 1]])


def create_rotation_matrix_3d_x(angle_degrees):
    """創建 3D 旋轉矩陣（繞 X 軸）"""
    angle_rad = np.radians(angle_degrees)
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)

    return np.array([[1, 0,      0,     0],
                     [0, cos_a, -sin_a, 0],
                     [0, sin_a,  cos_a, 0],
                     [0, 0,      0,     1]])


def create_rotation_matrix_3d_y(angle_degrees):
    """創建 3D 旋轉矩陣（繞 Y 軸）"""
    angle_rad = np.radians(angle_degrees)
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)

    return np.array([[ cos_a, 0, sin_a, 0],
                     [ 0,     1, 0,     0],
                     [-sin_a, 0, cos_a, 0],
                     [ 0,     0, 0,     1]])


def create_rotation_matrix_3d_z(angle_degrees):
    """創建 3D 旋轉矩陣（繞 Z 軸）"""
    angle_rad = np.radians(angle_degrees)
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)

    return np.array([[cos_a, -sin_a, 0, 0],
                     [sin_a,  cos_a, 0, 0],
                     [0,      0,     1, 0],
                     [0,      0,     0, 1]])


def demonstrate_3d_transforms():
    """示範 3D 齊次變換"""
    print("\n" + "=" * 50)
    print("3D 齊次變換矩陣")
    print("=" * 50)

    # 原始點
    point = np.array([1, 2, 3, 1])
    print(f"原始點: ({point[0]}, {point[1]}, {point[2]})")

    # 平移
    T = create_translation_matrix_3d(10, 20, 30)
    print(f"\n平移矩陣:\n{T}")
    p_t = np.dot(T, point)
    print(f"平移後: ({p_t[0]}, {p_t[1]}, {p_t[2]})")

    # 旋轉
    Rz = create_rotation_matrix_3d_z(90)
    print(f"\n繞 Z 軸旋轉 90 度:\n{Rz}")
    p_r = np.dot(Rz, point)
    print(f"旋轉後: ({p_r[0]:.2f}, {p_r[1]:.2f}, {p_r[2]:.2f})")

    # 組合：先旋轉後平移
    combined = np.dot(T, Rz)
    print(f"\n組合變換 (先旋轉後平移):\n{combined}")
    p_c = np.dot(combined, point)
    print(f"組合後: ({p_c[0]:.2f}, {p_c[1]:.2f}, {p_c[2]:.2f})")

    return T, Rz, combined


# ============================================
# 第四部分：逆變換
# ============================================

def demonstrate_inverse_transforms():
    """示範逆變換"""
    print("\n" + "=" * 50)
    print("逆變換")
    print("=" * 50)

    # 原始點
    point = np.array([100, 200, 1])
    print(f"原始點: ({point[0]}, {point[1]})")

    # 正向變換：旋轉 30 度 + 平移 (50, 30)
    R = create_rotation_matrix_2d_homogeneous(30)
    T = create_translation_matrix_2d(50, 30)
    forward = np.dot(T, R)

    print(f"\n正向變換矩陣:\n{forward}")

    transformed = np.dot(forward, point)
    print(f"變換後: ({transformed[0]:.2f}, {transformed[1]:.2f})")

    # 逆變換
    inverse = np.linalg.inv(forward)
    print(f"\n逆變換矩陣:\n{inverse}")

    recovered = np.dot(inverse, transformed)
    print(f"逆變換後（應該回到原點）: ({recovered[0]:.2f}, {recovered[1]:.2f})")

    # 驗證
    identity = np.dot(forward, inverse)
    print(f"\n驗證 T × T⁻¹ = I:\n{identity}")

    return forward, inverse


# ============================================
# 第五部分：實際應用
# ============================================

def multi_coordinate_system():
    """多重座標系統轉換（AOI 中常見）"""
    print("\n" + "=" * 50)
    print("實際應用：多重座標系統")
    print("=" * 50)

    print("""
    AOI 系統中的座標系統鏈：
    1. 影像座標系（Image） -> 像素單位
    2. 相機座標系（Camera） -> mm 單位
    3. 工作台座標系（Table） -> mm 單位
    4. 世界座標系（World） -> mm 單位（基準）
    """)

    # 1. 影像座標系中的點（像素）
    point_image = np.array([640, 480, 1])  # 影像中心
    print(f"\n1. 影像座標: ({point_image[0]}, {point_image[1]}) 像素")

    # 2. 影像 -> 相機座標系
    # 轉換：平移到原點，然後縮放（像素 -> mm）
    pixel_size = 0.01  # 1 像素 = 0.01 mm
    image_center = np.array([640, 480])

    T_image_to_camera = np.array([
        [pixel_size, 0, -image_center[0] * pixel_size],
        [0, pixel_size, -image_center[1] * pixel_size],
        [0, 0, 1]
    ])

    point_camera = np.dot(T_image_to_camera, point_image)
    print(f"2. 相機座標: ({point_camera[0]:.2f}, {point_camera[1]:.2f}) mm")

    # 3. 相機 -> 工作台座標系
    # 相機安裝在工作台上，有旋轉和偏移
    camera_angle = 0  # 相機沒有旋轉
    camera_offset = np.array([150, 200])  # 相機位置偏移

    R_camera = create_rotation_matrix_2d_homogeneous(camera_angle)
    T_camera_offset = create_translation_matrix_2d(camera_offset[0], camera_offset[1])
    T_camera_to_table = np.dot(T_camera_offset, R_camera)

    point_table = np.dot(T_camera_to_table, point_camera)
    print(f"3. 工作台座標: ({point_table[0]:.2f}, {point_table[1]:.2f}) mm")

    # 4. 工作台 -> 世界座標系
    # 工作台可以移動和旋轉
    table_angle = 15  # 工作台旋轉 15 度
    table_offset = np.array([1000, 500])  # 工作台位置

    R_table = create_rotation_matrix_2d_homogeneous(table_angle)
    T_table_offset = create_translation_matrix_2d(table_offset[0], table_offset[1])
    T_table_to_world = np.dot(T_table_offset, R_table)

    point_world = np.dot(T_table_to_world, point_table)
    print(f"4. 世界座標: ({point_world[0]:.2f}, {point_world[1]:.2f}) mm")

    # 組合所有變換
    T_image_to_world = np.dot(T_table_to_world, np.dot(T_camera_to_table, T_image_to_camera))
    print(f"\n組合變換矩陣（影像 -> 世界）:\n{T_image_to_world}")

    # 驗證：一步到位
    point_world_direct = np.dot(T_image_to_world, point_image)
    print(f"一步轉換驗證: ({point_world_direct[0]:.2f}, {point_world_direct[1]:.2f}) mm")

    return T_image_to_world


def robot_arm_chain():
    """機械手臂運動學鏈"""
    print("\n" + "=" * 50)
    print("實際應用：機械手臂運動學")
    print("=" * 50)

    print("""
    簡化的 3 軸機械手臂：
    - 基座 (Base)
    - 關節 1 (Joint 1) - 距離基座 L1 = 100mm
    - 關節 2 (Joint 2) - 距離關節 1 L2 = 150mm  - 末端執行器 (End Effector) - 距離關節 2 L3 = 80mm
    """)

    # 連桿長度
    L1, L2, L3 = 100, 150, 80

    # 關節角度
    theta1 = 30  # 關節 1 角度
    theta2 = 45  # 關節 2 角度
    theta3 = -20  # 關節 3 角度

    print(f"關節角度: θ1={theta1}°, θ2={theta2}°, θ3={theta3}°")

    # 變換矩陣鏈
    # 基座 -> 關節 1
    T_base_to_j1 = np.dot(
        create_translation_matrix_2d(0, L1),
        create_rotation_matrix_2d_homogeneous(theta1)
    )

    # 關節 1 -> 關節 2
    T_j1_to_j2 = np.dot(
        create_translation_matrix_2d(0, L2),
        create_rotation_matrix_2d_homogeneous(theta2)
    )

    # 關節 2 -> 末端
    T_j2_to_end = np.dot(
        create_translation_matrix_2d(0, L3),
        create_rotation_matrix_2d_homogeneous(theta3)
    )

    # 組合：基座 -> 末端
    T_base_to_end = np.dot(T_base_to_j1, np.dot(T_j1_to_j2, T_j2_to_end))

    # 末端位置（正向運動學）
    end_effector = np.dot(T_base_to_end, np.array([0, 0, 1]))
    print(f"\n末端執行器位置: ({end_effector[0]:.2f}, {end_effector[1]:.2f}) mm")

    # 末端姿態
    # 從變換矩陣中提取旋轉角度
    end_angle = np.degrees(np.arctan2(T_base_to_end[1, 0], T_base_to_end[0, 0]))
    print(f"末端執行器姿態: {end_angle:.2f}°")

    return T_base_to_end, end_effector


# ============================================
# 練習題
# ============================================

def exercises():
    """練習題"""
    print("\n" + "=" * 50)
    print("練習題")
    print("=" * 50)

    print("""
    練習 1: 繞任意點旋轉
    - 點 P(100, 100)
    - 繞點 C(50, 50) 旋轉 60 度
    - 提示：平移使 C 到原點 -> 旋轉 -> 平移回去

    練習 2: 座標系轉換
    - 影像座標 (320, 240) 像素
    - 像素大小 0.015 mm
    - 影像中心 (640, 480)
    - 相機在工作台位置 (100, 150) mm，旋轉 10 度
    - 計算在工作台座標系中的位置

    練習 3: 逆向運動學（簡化）
    - 兩關節機械手臂，L1=100mm, L2=150mm
    - 目標位置 (150, 200) mm
    - 求解關節角度（提示：使用逆變換或幾何方法）

    練習 4: 多次變換
    - 原始矩形 [(0,0), (10,0), (10,5), (0,5)]
    - 先繞 (5, 2.5) 旋轉 30 度
    - 再平移 (20, 10)
    - 再縮放 1.5 倍（繞中心）
    - 計算最終座標

    練習 5: 校準問題
    - 已知：影像中 3 個標記點的像素座標
    - 已知：這 3 個點的實際世界座標（mm）
    - 求解：影像到世界的變換矩陣
    - 提示：使用最小二乘法或 OpenCV 的 getPerspectiveTransform
    """)

    # 練習解答區
    print("\n# 練習 1 解答：")
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
    print("線性代數進階教學 - 齊次變換\n")

    # 執行所有示範
    why_homogeneous_coordinates()
    demonstrate_2d_transforms()
    visualize_2d_homogeneous_transforms()
    demonstrate_3d_transforms()
    demonstrate_inverse_transforms()
    multi_coordinate_system()
    robot_arm_chain()
    exercises()

    print("\n" + "=" * 50)
    print("線性代數部分教學完成！")
    print("=" * 50)
    print("\n下一步：進入 2_calculus_kinematics 資料夾學習微積分和運動學")
