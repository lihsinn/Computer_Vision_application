"""
微積分與運動學 - 速度與加速度
適用於 AOI/上位機開發

學習目標：
1. 理解位置、速度、加速度的關係
2. 掌握數值微分與積分
3. 應用於運動控制和軌跡規劃
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from scipy.interpolate import interp1d

# ============================================
# 第一部分：基本概念
# ============================================

def calculus_basics():
    """微積分基本概念"""
    print("=" * 50)
    print("微積分基本概念")
    print("=" * 50)

    print("""
    核心關係：

    位置 -> 微分 -> 速度 -> 微分 -> 加速度
    加速度 -> 積分 -> 速度 -> 積分 -> 位置

    數學表示：
    - 速度 v(t) = dx/dt = 位置的導數
    - 加速度 a(t) = dv/dt = d²x/dt² = 速度的導數

    離散系統（實際控制中）：
    - 速度 v[n] ≈ (x[n] - x[n-1]) / Δt
    - 加速度 a[n] ≈ (v[n] - v[n-1]) / Δt
    """)


# ============================================
# 第二部分：數值微分
# ============================================

def numerical_derivative():
    """數值微分示範"""
    print("\n" + "=" * 50)
    print("數值微分：計算速度和加速度")
    print("=" * 50)

    # 時間序列
    t = np.linspace(0, 10, 100)
    dt = t[1] - t[0]

    # 位置：簡諧運動 x(t) = A*sin(ωt)
    A = 100  # 振幅 (mm)
    omega = 2 * np.pi * 0.5  # 角頻率 (rad/s), 頻率 0.5 Hz
    x = A * np.sin(omega * t)

    print(f"位置函數: x(t) = {A} * sin({omega:.2f} * t)")

    # 數值微分計算速度
    v_numerical = np.gradient(x, dt)

    # 解析解（用於比較）
    v_analytical = A * omega * np.cos(omega * t)

    print(f"\n速度（解析）: v(t) = {A * omega:.2f} * cos({omega:.2f} * t)")
    print(f"最大速度（理論）: {A * omega:.2f} mm/s")
    print(f"最大速度（數值）: {np.max(np.abs(v_numerical)):.2f} mm/s")

    # 數值微分計算加速度
    a_numerical = np.gradient(v_numerical, dt)

    # 解析解
    a_analytical = -A * omega**2 * np.sin(omega * t)

    print(f"\n加速度（解析）: a(t) = {-A * omega**2:.2f} * sin({omega:.2f} * t)")
    print(f"最大加速度（理論）: {A * omega**2:.2f} mm/s²")
    print(f"最大加速度（數值）: {np.max(np.abs(a_numerical)):.2f} mm/s²")

    # 視覺化
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))

    # 位置
    axes[0].plot(t, x, 'b-', linewidth=2, label='位置')
    axes[0].set_ylabel('位置 (mm)')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    axes[0].set_title('簡諧運動：位置、速度、加速度')

    # 速度
    axes[1].plot(t, v_analytical, 'g-', linewidth=2, label='速度（解析）', alpha=0.7)
    axes[1].plot(t, v_numerical, 'r--', linewidth=1, label='速度（數值）')
    axes[1].set_ylabel('速度 (mm/s)')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    # 加速度
    axes[2].plot(t, a_analytical, 'm-', linewidth=2, label='加速度（解析）', alpha=0.7)
    axes[2].plot(t, a_numerical, 'c--', linewidth=1, label='加速度（數值）')
    axes[2].set_ylabel('加速度 (mm/s²)')
    axes[2].set_xlabel('時間 (s)')
    axes[2].grid(True, alpha=0.3)
    axes[2].legend()

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\2_calculus_kinematics\\velocity_acceleration.png', dpi=100)
    print("\n速度與加速度圖已儲存: velocity_acceleration.png")
    plt.close()

    return t, x, v_numerical, a_numerical


def finite_difference_methods():
    """不同的有限差分方法"""
    print("\n" + "=" * 50)
    print("有限差分方法比較")
    print("=" * 50)

    # 測試函數：x(t) = t²
    t = np.linspace(0, 5, 50)
    x = t**2
    dt = t[1] - t[0]

    # 解析導數：v(t) = 2t
    v_true = 2 * t

    # 1. 前向差分
    v_forward = np.zeros_like(x)
    v_forward[:-1] = (x[1:] - x[:-1]) / dt
    v_forward[-1] = v_forward[-2]

    # 2. 後向差分
    v_backward = np.zeros_like(x)
    v_backward[1:] = (x[1:] - x[:-1]) / dt
    v_backward[0] = v_backward[1]

    # 3. 中央差分（更精確）
    v_central = np.zeros_like(x)
    v_central[1:-1] = (x[2:] - x[:-2]) / (2 * dt)
    v_central[0] = v_central[1]
    v_central[-1] = v_central[-2]

    # 4. numpy.gradient（自動處理邊界）
    v_gradient = np.gradient(x, dt)

    print("方法比較（在 t=2.5 處）:")
    idx = len(t) // 2
    print(f"真實值:     {v_true[idx]:.4f}")
    print(f"前向差分:   {v_forward[idx]:.4f}, 誤差: {abs(v_forward[idx] - v_true[idx]):.4f}")
    print(f"後向差分:   {v_backward[idx]:.4f}, 誤差: {abs(v_backward[idx] - v_true[idx]):.4f}")
    print(f"中央差分:   {v_central[idx]:.4f}, 誤差: {abs(v_central[idx] - v_true[idx]):.4f}")
    print(f"np.gradient: {v_gradient[idx]:.4f}, 誤差: {abs(v_gradient[idx] - v_true[idx]):.4f}")

    print("\n建議：使用 np.gradient() 或中央差分以獲得最佳精度")

    return t, v_true, v_forward, v_backward, v_central


# ============================================
# 第三部分：數值積分
# ============================================

def numerical_integration():
    """數值積分示範"""
    print("\n" + "=" * 50)
    print("數值積分：從加速度計算速度和位置")
    print("=" * 50)

    # 時間序列
    t = np.linspace(0, 5, 100)
    dt = t[1] - t[0]

    # 加速度：常數加速 -> 等加速運動
    a = 10 * np.ones_like(t)  # 10 mm/s²
    a[t > 2.5] = -10  # 2.5秒後減速

    print("加速度模式:")
    print(f"  0-2.5s: a = +10 mm/s² (加速)")
    print(f"  2.5-5s: a = -10 mm/s² (減速)")

    # 積分計算速度（初速度 = 0）
    v = integrate.cumtrapz(a, t, initial=0)

    # 積分計算位置（初位置 = 0）
    x = integrate.cumtrapz(v, t, initial=0)

    print(f"\n最大速度: {np.max(v):.2f} mm/s (在 t={t[np.argmax(v)]:.2f}s)")
    print(f"最終位置: {x[-1]:.2f} mm")
    print(f"最終速度: {v[-1]:.2f} mm/s (應該接近 0)")

    # 視覺化
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))

    axes[0].plot(t, a, 'r-', linewidth=2)
    axes[0].set_ylabel('加速度 (mm/s²)')
    axes[0].grid(True, alpha=0.3)
    axes[0].set_title('等加速運動：加速 -> 減速')
    axes[0].axhline(y=0, color='k', linestyle='--', alpha=0.3)

    axes[1].plot(t, v, 'g-', linewidth=2)
    axes[1].set_ylabel('速度 (mm/s)')
    axes[1].grid(True, alpha=0.3)
    axes[1].axhline(y=0, color='k', linestyle='--', alpha=0.3)

    axes[2].plot(t, x, 'b-', linewidth=2)
    axes[2].set_ylabel('位置 (mm)')
    axes[2].set_xlabel('時間 (s)')
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\2_calculus_kinematics\\integration.png', dpi=100)
    print("\n積分圖已儲存: integration.png")
    plt.close()

    return t, a, v, x


# ============================================
# 第四部分：運動學應用
# ============================================

def motion_profile_trapezoidal():
    """梯形速度曲線（常用於運動控制）"""
    print("\n" + "=" * 50)
    print("運動學應用：梯形速度曲線")
    print("=" * 50)

    # 運動參數
    distance = 1000  # 總距離 (mm)
    v_max = 200      # 最大速度 (mm/s)
    a_max = 100      # 最大加速度 (mm/s²)

    print(f"運動參數:")
    print(f"  總距離: {distance} mm")
    print(f"  最大速度: {v_max} mm/s")
    print(f"  最大加速度: {a_max} mm/s²")

    # 計算時間段
    t_accel = v_max / a_max  # 加速時間
    d_accel = 0.5 * a_max * t_accel**2  # 加速距離

    # 檢查是否能達到最大速度
    if 2 * d_accel > distance:
        # 三角形曲線（無恆速段）
        print("\n採用三角形速度曲線（距離太短，無法達到最大速度）")
        t_accel = np.sqrt(distance / a_max)
        v_max_actual = a_max * t_accel
        t_const = 0
        t_decel = t_accel
    else:
        # 梯形曲線
        print("\n採用梯形速度曲線")
        v_max_actual = v_max
        d_const = distance - 2 * d_accel  # 恆速距離
        t_const = d_const / v_max  # 恆速時間
        t_decel = t_accel

    t_total = t_accel + t_const + t_decel
    print(f"  加速時間: {t_accel:.2f}s")
    print(f"  恆速時間: {t_const:.2f}s")
    print(f"  減速時間: {t_decel:.2f}s")
    print(f"  總時間: {t_total:.2f}s")

    # 生成運動曲線
    n_points = 500
    t = np.linspace(0, t_total, n_points)
    v = np.zeros(n_points)
    x = np.zeros(n_points)
    a = np.zeros(n_points)

    for i, ti in enumerate(t):
        if ti < t_accel:
            # 加速階段
            a[i] = a_max
            v[i] = a_max * ti
            x[i] = 0.5 * a_max * ti**2
        elif ti < t_accel + t_const:
            # 恆速階段
            a[i] = 0
            v[i] = v_max_actual
            x[i] = d_accel + v_max_actual * (ti - t_accel)
        else:
            # 減速階段
            t_from_decel = ti - t_accel - t_const
            a[i] = -a_max
            v[i] = v_max_actual - a_max * t_from_decel
            x[i] = d_accel + v_max_actual * t_const + v_max_actual * t_from_decel - 0.5 * a_max * t_from_decel**2

    # 視覺化
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))

    # 加速度
    axes[0].plot(t, a, 'r-', linewidth=2)
    axes[0].axvline(x=t_accel, color='g', linestyle='--', alpha=0.5, label='加速結束')
    axes[0].axvline(x=t_accel+t_const, color='b', linestyle='--', alpha=0.5, label='恆速結束')
    axes[0].set_ylabel('加速度 (mm/s²)')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    axes[0].set_title('梯形速度曲線（運動控制標準）')

    # 速度
    axes[1].plot(t, v, 'g-', linewidth=2)
    axes[1].axvline(x=t_accel, color='g', linestyle='--', alpha=0.5)
    axes[1].axvline(x=t_accel+t_const, color='b', linestyle='--', alpha=0.5)
    axes[1].axhline(y=v_max_actual, color='orange', linestyle=':', alpha=0.5, label=f'最大速度 {v_max_actual:.1f}')
    axes[1].set_ylabel('速度 (mm/s)')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    # 位置
    axes[2].plot(t, x, 'b-', linewidth=2)
    axes[2].axvline(x=t_accel, color='g', linestyle='--', alpha=0.5)
    axes[2].axvline(x=t_accel+t_const, color='b', linestyle='--', alpha=0.5)
    axes[2].axhline(y=distance, color='orange', linestyle=':', alpha=0.5, label=f'目標 {distance}')
    axes[2].set_ylabel('位置 (mm)')
    axes[2].set_xlabel('時間 (s)')
    axes[2].grid(True, alpha=0.3)
    axes[2].legend()

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\2_calculus_kinematics\\trapezoidal_profile.png', dpi=100)
    print("\n梯形曲線圖已儲存: trapezoidal_profile.png")
    plt.close()

    return t, x, v, a


def point_to_point_motion():
    """點對點運動規劃"""
    print("\n" + "=" * 50)
    print("點對點運動規劃")
    print("=" * 50)

    # 起點和終點
    start = np.array([0, 0])
    end = np.array([500, 300])

    print(f"起點: {start}")
    print(f"終點: {end}")

    # 計算距離和方向
    direction = end - start
    distance = np.linalg.norm(direction)
    unit_dir = direction / distance

    print(f"距離: {distance:.2f} mm")
    print(f"方向向量: {unit_dir}")

    # 使用梯形速度曲線
    v_max = 200
    a_max = 100

    # 生成 1D 運動曲線
    t_accel = v_max / a_max
    d_accel = 0.5 * a_max * t_accel**2

    if 2 * d_accel > distance:
        t_accel = np.sqrt(distance / a_max)
        v_max_actual = a_max * t_accel
        t_const = 0
    else:
        v_max_actual = v_max
        d_const = distance - 2 * d_accel
        t_const = d_const / v_max

    t_total = 2 * t_accel + t_const
    t = np.linspace(0, t_total, 200)

    # 沿軌跡的 1D 位置
    s = np.zeros(len(t))
    for i, ti in enumerate(t):
        if ti < t_accel:
            s[i] = 0.5 * a_max * ti**2
        elif ti < t_accel + t_const:
            s[i] = d_accel + v_max_actual * (ti - t_accel)
        else:
            t_from_decel = ti - t_accel - t_const
            s[i] = d_accel + v_max_actual * t_const + v_max_actual * t_from_decel - 0.5 * a_max * t_from_decel**2

    # 轉換為 2D 軌跡
    trajectory = start + np.outer(s, unit_dir)

    # 視覺化
    plt.figure(figsize=(10, 6))
    plt.plot(trajectory[:, 0], trajectory[:, 1], 'b-', linewidth=2, label='軌跡')
    plt.plot(start[0], start[1], 'go', markersize=10, label='起點')
    plt.plot(end[0], end[1], 'ro', markersize=10, label='終點')

    # 標記幾個中間點
    markers = [0, len(t)//4, len(t)//2, 3*len(t)//4, -1]
    for i in markers:
        plt.plot(trajectory[i, 0], trajectory[i, 1], 'ko', markersize=5)
        plt.text(trajectory[i, 0], trajectory[i, 1]+20, f't={t[i]:.2f}s', ha='center')

    plt.grid(True, alpha=0.3)
    plt.xlabel('X (mm)')
    plt.ylabel('Y (mm)')
    plt.title('2D 點對點運動')
    plt.legend()
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\2_calculus_kinematics\\point_to_point.png', dpi=100)
    print("\n點對點運動圖已儲存: point_to_point.png")
    plt.close()

    return t, trajectory


# ============================================
# 練習題
# ============================================

def exercises():
    """練習題"""
    print("\n" + "=" * 50)
    print("練習題")
    print("=" * 50)

    print("""
    練習 1: 數值微分
    - 給定位置數據: t = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
                    x = [0, 5, 18, 38, 65, 98]
    - 計算各時刻的速度（使用中央差分）
    - 計算各時刻的加速度

    練習 2: 數值積分
    - 給定速度曲線: v(t) = 50 * sin(πt) mm/s, t ∈ [0, 2]
    - 計算 2 秒後的總位移
    - 繪製位置-時間圖

    練習 3: 梯形曲線設計
    - 設計一個運動曲線，參數：
      - 距離: 2000 mm
      - 最大速度: 300 mm/s
      - 最大加速度: 150 mm/s²
    - 計算總時間
    - 繪製 a-v-x 三合一圖

    練習 4: 軌跡規劃
    - 規劃從 (100, 100) 到 (400, 300) 的運動
    - 使用 S 曲線（加速度連續變化，比梯形更平滑）
    - 提示: 可以用 jerk（加加速度）來實現

    練習 5: 實際應用
    - AOI 檢測需要掃描一個 1000×800 mm 的 PCB
    - 採用蛇形路徑（往返掃描）
    - 每行間距 50 mm
    - 最大速度 400 mm/s，加速度 200 mm/s²
    - 計算總檢測時間
    """)

    # 練習解答區
    print("\n# 練習 1 解答：")
    t_data = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    x_data = np.array([0, 5, 18, 38, 65, 98])
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
    print("微積分與運動學教學 - 速度與加速度\n")

    # 執行所有示範
    calculus_basics()
    numerical_derivative()
    finite_difference_methods()
    numerical_integration()
    motion_profile_trapezoidal()
    point_to_point_motion()
    exercises()

    print("\n" + "=" * 50)
    print("教學完成！")
    print("=" * 50)
    print("\n下一步：學習 02_pid_controller.py（PID 控制器）")
