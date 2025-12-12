"""
線性代數基礎 - 向量與矩陣
適用於 AOI/上位機開發

學習目標：
1. 理解向量的基本操作
2. 掌握矩陣運算
3. 應用於實際 AOI 場景
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ============================================
# 第一部分：向量基礎
# ============================================

def vector_basics():
    """向量的基本操作"""
    print("=" * 50)
    print("向量基礎操作")
    print("=" * 50)

    # 創建向量（代表 AOI 中的一個點座標）
    point_a = np.array([100, 200])  # (x, y) 像素座標
    point_b = np.array([300, 400])

    print(f"點 A 座標: {point_a}")
    print(f"點 B 座標: {point_b}")

    # 向量加法（平移）
    translation = np.array([50, -30])
    point_a_shifted = point_a + translation
    print(f"\n點 A 平移後: {point_a_shifted}")

    # 向量減法（計算方向向量）
    direction = point_b - point_a
    print(f"\nA 到 B 的方向向量: {direction}")

    # 向量長度（距離）
    distance = np.linalg.norm(direction)
    print(f"A 到 B 的距離: {distance:.2f} 像素")

    # 單位向量（方向）
    unit_vector = direction / distance
    print(f"單位方向向量: {unit_vector}")

    # 點積（判斷角度）
    v1 = np.array([1, 0])
    v2 = np.array([1, 1])
    dot_product = np.dot(v1, v2)
    angle = np.arccos(dot_product / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    print(f"\n向量 {v1} 和 {v2} 的夾角: {np.degrees(angle):.2f}度")

    return point_a, point_b, direction


def visualize_vectors():
    """視覺化向量運算"""
    plt.figure(figsize=(10, 5))

    # 原始向量
    origin = np.array([0, 0])
    v1 = np.array([3, 2])
    v2 = np.array([1, 3])

    # 繪製向量
    plt.subplot(1, 2, 1)
    plt.quiver(*origin, *v1, angles='xy', scale_units='xy', scale=1, color='r', label='v1', width=0.006)
    plt.quiver(*origin, *v2, angles='xy', scale_units='xy', scale=1, color='b', label='v2', width=0.006)
    plt.quiver(*origin, *(v1+v2), angles='xy', scale_units='xy', scale=1, color='g', label='v1+v2', width=0.006)
    plt.xlim(-1, 5)
    plt.ylim(-1, 6)
    plt.grid(True)
    plt.legend()
    plt.title('向量加法')
    plt.xlabel('x')
    plt.ylabel('y')

    # 縮放
    plt.subplot(1, 2, 2)
    plt.quiver(*origin, *v1, angles='xy', scale_units='xy', scale=1, color='r', label='v1', width=0.006)
    plt.quiver(*origin, *(v1*2), angles='xy', scale_units='xy', scale=1, color='b', label='v1*2', width=0.006)
    plt.quiver(*origin, *(v1*0.5), angles='xy', scale_units='xy', scale=1, color='g', label='v1*0.5', width=0.006)
    plt.xlim(-1, 7)
    plt.ylim(-1, 5)
    plt.grid(True)
    plt.legend()
    plt.title('向量縮放')
    plt.xlabel('x')
    plt.ylabel('y')

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\1_linear_algebra\\vectors_visualization.png', dpi=100)
    print("\n向量視覺化圖已儲存: vectors_visualization.png")
    plt.close()


# ============================================
# 第二部分：矩陣基礎
# ============================================

def matrix_basics():
    """矩陣的基本操作"""
    print("\n" + "=" * 50)
    print("矩陣基礎操作")
    print("=" * 50)

    # 創建矩陣（代表影像或變換）
    A = np.array([[1, 2],
                  [3, 4]])
    B = np.array([[5, 6],
                  [7, 8]])

    print(f"矩陣 A:\n{A}")
    print(f"\n矩陣 B:\n{B}")

    # 矩陣加法
    print(f"\nA + B:\n{A + B}")

    # 矩陣乘法（變換組合）
    print(f"\nA × B:\n{np.dot(A, B)}")

    # 轉置（常用於資料處理）
    print(f"\nA 的轉置:\n{A.T}")

    # 逆矩陣（反向變換）
    if np.linalg.det(A) != 0:
        A_inv = np.linalg.inv(A)
        print(f"\nA 的逆矩陣:\n{A_inv}")
        print(f"\n驗證 A × A⁻¹ = I:\n{np.dot(A, A_inv)}")

    # 矩陣乘向量（應用變換）
    v = np.array([10, 20])
    transformed = np.dot(A, v)
    print(f"\n向量 {v} 經過變換 A 後: {transformed}")

    return A, B


def matrix_for_image_processing():
    """矩陣在影像處理中的應用"""
    print("\n" + "=" * 50)
    print("矩陣應用：影像處理")
    print("=" * 50)

    # 創建簡單的影像矩陣（灰階值）
    image = np.array([[100, 150, 200],
                      [120, 170, 210],
                      [110, 160, 190]], dtype=np.uint8)

    print(f"原始影像（3×3像素）:\n{image}")

    # 影像增強：對比度調整
    contrast_factor = 1.5
    enhanced = np.clip(image * contrast_factor, 0, 255).astype(np.uint8)
    print(f"\n增強對比度後:\n{enhanced}")

    # 影像濾波：平均濾波器（模糊）
    kernel = np.ones((3, 3)) / 9
    print(f"\n平均濾波核:\n{kernel}")

    # 銳化濾波器
    sharpen_kernel = np.array([[ 0, -1,  0],
                               [-1,  5, -1],
                               [ 0, -1,  0]])
    print(f"\n銳化濾波核:\n{sharpen_kernel}")

    return image, kernel


# ============================================
# 第三部分：AOI 實際應用
# ============================================

def aoi_coordinate_transform():
    """AOI 中的座標變換"""
    print("\n" + "=" * 50)
    print("AOI 應用：座標系統轉換")
    print("=" * 50)

    # 影像座標系（像素）
    image_point = np.array([640, 480])  # 中心點
    print(f"影像座標（像素）: {image_point}")

    # 轉換到機器座標系（mm）
    # 假設：1像素 = 0.01mm，原點在影像中心
    pixel_to_mm = 0.01
    image_center = np.array([640, 480])
    machine_point = (image_point - image_center) * pixel_to_mm
    print(f"機器座標（mm）: {machine_point}")

    # 變換矩陣：旋轉 + 平移
    angle = np.radians(30)  # 旋轉30度
    rotation = np.array([[np.cos(angle), -np.sin(angle)],
                        [np.sin(angle),  np.cos(angle)]])

    rotated_point = np.dot(rotation, machine_point)
    print(f"旋轉30度後: {rotated_point}")

    # 加上偏移
    offset = np.array([100, 50])
    final_point = rotated_point + offset
    print(f"最終機器座標: {final_point}")

    return final_point


def calculate_defect_features():
    """計算瑕疵特徵（使用矩陣）"""
    print("\n" + "=" * 50)
    print("AOI 應用：瑕疵特徵計算")
    print("=" * 50)

    # 瑕疵的像素座標列表
    defect_pixels = np.array([
        [100, 200],
        [101, 200],
        [102, 200],
        [100, 201],
        [101, 201],
        [102, 201]
    ])

    print(f"瑕疵像素座標:\n{defect_pixels}")

    # 計算中心點（質心）
    centroid = np.mean(defect_pixels, axis=0)
    print(f"\n瑕疵中心: {centroid}")

    # 計算面積（像素數）
    area = len(defect_pixels)
    print(f"瑕疵面積: {area} 像素")

    # 計算邊界框
    min_coords = np.min(defect_pixels, axis=0)
    max_coords = np.max(defect_pixels, axis=0)
    bbox_size = max_coords - min_coords + 1
    print(f"邊界框: {min_coords} 到 {max_coords}")
    print(f"邊界框尺寸: {bbox_size}")

    # 計算方向（主軸）
    centered = defect_pixels - centroid
    covariance = np.dot(centered.T, centered) / len(defect_pixels)
    eigenvalues, eigenvectors = np.linalg.eig(covariance)
    main_direction = eigenvectors[:, np.argmax(eigenvalues)]
    angle = np.degrees(np.arctan2(main_direction[1], main_direction[0]))
    print(f"主軸方向: {angle:.2f}度")

    return centroid, area, angle


# ============================================
# 練習題
# ============================================

def exercises():
    """練習題"""
    print("\n" + "=" * 50)
    print("練習題")
    print("=" * 50)

    print("""
    練習 1: 計算兩點距離
    - 給定影像上兩個瑕疵的座標 A(150, 200) 和 B(450, 600)
    - 計算它們之間的距離（像素）
    - 提示: 使用 np.linalg.norm()

    練習 2: 座標變換
    - 有一個點 P(100, 100) 在影像座標系中
    - 將其旋轉45度
    - 然後平移 (50, -30)
    - 求最終座標

    練習 3: 多點質心計算
    - 給定一組點的座標（自己創建5-10個點）
    - 計算這些點的質心
    - 計算每個點到質心的平均距離

    練習 4: 矩陣變換組合
    - 創建一個縮放矩陣（放大2倍）
    - 創建一個旋轉矩陣（旋轉90度）
    - 將兩個變換組合成一個矩陣
    - 應用到向量 (10, 20) 上
    """)

    # 練習 1 解答區（讓學習者自己填寫）
    print("\n# 練習 1 解答：")
    A = np.array([150, 200])
    B = np.array([450, 600])
    # 在這裡寫你的代碼
    distance = None  # 計算距離
    # print(f"距離: {distance}")

    print("\n# 練習 2 解答：")
    P = np.array([100, 100])
    # 在這裡寫你的代碼

    print("\n# 練習 3 解答：")
    # 在這裡寫你的代碼

    print("\n# 練習 4 解答：")
    # 在這裡寫你的代碼


# ============================================
# 主程式
# ============================================

if __name__ == "__main__":
    print("線性代數基礎教學 - 向量與矩陣\n")

    # 執行所有示範
    vector_basics()
    visualize_vectors()
    matrix_basics()
    matrix_for_image_processing()
    aoi_coordinate_transform()
    calculate_defect_features()
    exercises()

    print("\n" + "=" * 50)
    print("教學完成！")
    print("=" * 50)
    print("\n下一步：學習 02_rotation_matrices.py（旋轉矩陣）")
