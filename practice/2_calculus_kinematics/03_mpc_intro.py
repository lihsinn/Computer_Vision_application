"""
模型預測控制 (MPC) 入門
適用於 AOI/上位機開發

學習目標：
1. 理解 MPC 基本原理
2. 實現簡單的 MPC 控制器
3. 了解 MPC 與 PID 的區別
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# ============================================
# 第一部分：MPC 基本原理
# ============================================

def mpc_theory():
    """MPC 控制原理"""
    print("=" * 50)
    print("模型預測控制 (MPC) 原理")
    print("=" * 50)

    print("""
    MPC 核心概念：

    1. 模型 (Model)：
       - 使用系統的數學模型來預測未來行為
       - 例：x[k+1] = A*x[k] + B*u[k]

    2. 預測 (Prediction)：
       - 根據當前狀態和未來控制序列，預測未來 N 步的輸出
       - 預測時域 (Prediction Horizon)：通常 10-50 步

    3. 優化 (Optimization)：
       - 找到最優的控制序列，使得成本函數最小化
       - 成本函數通常包含：追蹤誤差 + 控制能量

    4. 滾動時域 (Receding Horizon)：
       - 每個時刻重新計算最優控制序列
       - 只執行第一步控制，然後重複

    MPC vs PID：

    PID：
    - 優點：簡單、快速、不需要模型
    - 缺點：無法處理約束、無法預見未來

    MPC：
    - 優點：可以處理約束、多變量、預測未來
    - 缺點：計算量大、需要準確模型

    典型應用：
    - 軌跡追蹤（AOI 掃描路徑）
    - 多軸協同控制
    - 有約束的控制（速度限制、加速度限制）
    """)


# ============================================
# 第二部分：簡單 MPC 實現
# ============================================

class SimpleMPC:
    """簡單的 MPC 控制器（1D 系統）"""

    def __init__(self, A, B, Q, R, N=10, u_min=-np.inf, u_max=np.inf):
        """
        初始化 MPC 控制器

        參數:
            A: 狀態轉移矩陣 (scalar 或 matrix)
            B: 控制輸入矩陣 (scalar 或 matrix)
            Q: 狀態權重 (越大越重視追蹤精度)
            R: 控制權重 (越大越重視控制能量)
            N: 預測時域
            u_min, u_max: 控制輸入約束
        """
        self.A = np.atleast_1d(A)
        self.B = np.atleast_1d(B)
        self.Q = Q
        self.R = R
        self.N = N
        self.u_min = u_min
        self.u_max = u_max

    def predict(self, x0, u_sequence):
        """
        預測未來 N 步的狀態

        參數:
            x0: 當前狀態
            u_sequence: 未來控制序列 (長度 N)

        返回:
            x_predicted: 預測的狀態序列 (長度 N+1)
        """
        x_predicted = [x0]
        x = x0

        for u in u_sequence:
            x_next = self.A * x + self.B * u
            x_predicted.append(x_next)
            x = x_next

        return np.array(x_predicted)

    def cost_function(self, u_sequence, x0, setpoint):
        """
        成本函數

        J = Σ Q*(x[k] - r)² + R*u[k]²

        參數:
            u_sequence: 控制序列
            x0: 當前狀態
            setpoint: 目標值

        返回:
            cost: 總成本
        """
        # 預測未來狀態
        x_predicted = self.predict(x0, u_sequence)

        # 計算成本
        tracking_error = np.sum(self.Q * (x_predicted[1:] - setpoint)**2)
        control_effort = np.sum(self.R * u_sequence**2)

        return tracking_error + control_effort

    def compute_control(self, x0, setpoint, u_init=None):
        """
        計算最優控制

        參數:
            x0: 當前狀態
            setpoint: 目標值
            u_init: 初始控制序列猜測

        返回:
            u_optimal: 最優控制（第一步）
            u_sequence: 完整的最優控制序列
        """
        # 初始猜測
        if u_init is None:
            u_init = np.zeros(self.N)

        # 約束
        bounds = [(self.u_min, self.u_max)] * self.N

        # 優化
        result = minimize(
            lambda u: self.cost_function(u, x0, setpoint),
            u_init,
            bounds=bounds,
            method='SLSQP'
        )

        u_sequence = result.x

        return u_sequence[0], u_sequence


def demonstrate_simple_mpc():
    """示範簡單 MPC"""
    print("\n" + "=" * 50)
    print("簡單 MPC 示範")
    print("=" * 50)

    # 系統模型：一階系統
    # x[k+1] = 0.9*x[k] + 0.1*u[k]
    A = 0.9
    B = 0.1

    # MPC 參數
    Q = 10    # 追蹤權重
    R = 0.1   # 控制權重
    N = 15    # 預測時域

    # 創建 MPC 控制器
    mpc = SimpleMPC(A, B, Q, R, N, u_min=-10, u_max=10)

    # 模擬
    dt = 0.1
    t_end = 10
    t = np.arange(0, t_end, dt)

    setpoint = 5.0
    x = 0.0  # 初始狀態

    # 記錄
    states = []
    controls = []

    print("開始 MPC 控制模擬...")

    for i in range(len(t)):
        # MPC 計算控制
        u, u_seq = mpc.compute_control(x, setpoint)

        # 應用控制（實際系統）
        x_next = A * x + B * u

        # 記錄
        states.append(x)
        controls.append(u)

        # 更新狀態
        x = x_next

    states = np.array(states)
    controls = np.array(controls)

    # 視覺化
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    # 狀態
    axes[0].plot(t, states, 'b-', linewidth=2, label='實際狀態')
    axes[0].axhline(y=setpoint, color='r', linestyle='--', label='目標值')
    axes[0].set_ylabel('狀態')
    axes[0].set_title(f'MPC 控制 (Q={Q}, R={R}, N={N})')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # 控制
    axes[1].plot(t, controls, 'g-', linewidth=2, label='控制輸入')
    axes[1].axhline(y=10, color='r', linestyle=':', alpha=0.5, label='上限')
    axes[1].axhline(y=-10, color='r', linestyle=':', alpha=0.5, label='下限')
    axes[1].set_xlabel('時間 (s)')
    axes[1].set_ylabel('控制輸入')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\2_calculus_kinematics\\simple_mpc.png', dpi=100)
    print("簡單 MPC 圖已儲存: simple_mpc.png")
    plt.close()

    return t, states, controls


# ============================================
# 第三部分：MPC vs PID 比較
# ============================================

def compare_mpc_pid():
    """比較 MPC 和 PID"""
    print("\n" + "=" * 50)
    print("MPC vs PID 比較")
    print("=" * 50)

    # 系統
    A = 0.95
    B = 0.05

    # 模擬參數
    dt = 0.1
    t_end = 10
    t = np.arange(0, t_end, dt)

    # 階梯目標值
    setpoints = np.zeros_like(t)
    setpoints[t >= 1] = 5.0
    setpoints[t >= 5] = -3.0

    # ===== PID 控制 =====
    from pid_controller_module import PIDController  # 假設已經有 PID 類別

    # 簡單實現 PID（如果沒有模組）
    class SimplePID:
        def __init__(self, Kp, Ki, Kd):
            self.Kp = Kp
            self.Ki = Ki
            self.Kd = Kd
            self.integral = 0
            self.prev_error = 0

        def compute(self, error, dt):
            self.integral += error * dt
            derivative = (error - self.prev_error) / dt
            self.prev_error = error
            return self.Kp * error + self.Ki * self.integral + self.Kd * derivative

    pid = SimplePID(Kp=2.0, Ki=0.5, Kd=0.5)

    x_pid = 0.0
    states_pid = []
    controls_pid = []

    for i in range(len(t)):
        error = setpoints[i] - x_pid
        u = pid.compute(error, dt)
        u = np.clip(u, -10, 10)  # 控制限制
        x_pid = A * x_pid + B * u

        states_pid.append(x_pid)
        controls_pid.append(u)

    # ===== MPC 控制 =====
    mpc = SimpleMPC(A, B, Q=10, R=0.1, N=15, u_min=-10, u_max=10)

    x_mpc = 0.0
    states_mpc = []
    controls_mpc = []

    for i in range(len(t)):
        u, _ = mpc.compute_control(x_mpc, setpoints[i])
        x_mpc = A * x_mpc + B * u

        states_mpc.append(x_mpc)
        controls_mpc.append(u)

    # 視覺化比較
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    # 狀態
    axes[0].plot(t, setpoints, 'k--', linewidth=2, label='目標值', alpha=0.7)
    axes[0].plot(t, states_pid, 'b-', linewidth=2, label='PID')
    axes[0].plot(t, states_mpc, 'r-', linewidth=2, label='MPC')
    axes[0].set_ylabel('狀態')
    axes[0].set_title('MPC vs PID 比較')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # 控制
    axes[1].plot(t, controls_pid, 'b-', linewidth=2, label='PID 控制')
    axes[1].plot(t, controls_mpc, 'r-', linewidth=2, label='MPC 控制')
    axes[1].axhline(y=10, color='k', linestyle=':', alpha=0.3)
    axes[1].axhline(y=-10, color='k', linestyle=':', alpha=0.3)
    axes[1].set_xlabel('時間 (s)')
    axes[1].set_ylabel('控制輸入')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\2_calculus_kinematics\\mpc_vs_pid.png', dpi=100)
    print("MPC vs PID 比較圖已儲存: mpc_vs_pid.png")
    print("\n觀察：MPC 在處理約束和目標變化時通常更平滑")
    plt.close()


# ============================================
# 第四部分：軌跡追蹤 MPC
# ============================================

def trajectory_tracking_mpc():
    """軌跡追蹤 MPC（AOI 應用）"""
    print("\n" + "=" * 50)
    print("軌跡追蹤 MPC")
    print("=" * 50)

    # 目標軌跡：圓形
    t_traj = np.linspace(0, 2*np.pi, 200)
    radius = 100
    x_ref = radius * np.cos(t_traj)
    y_ref = radius * np.sin(t_traj)

    print(f"目標軌跡：半徑 {radius}mm 的圓")

    # 簡單的 2D 運動模型（雙積分器）
    # 狀態: [x, vx, y, vy]
    # 控制: [ax, ay]
    dt = 0.1

    A = np.array([[1, dt, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, dt],
                  [0, 0, 0, 1]])

    B = np.array([[0.5*dt**2, 0],
                  [dt, 0],
                  [0, 0.5*dt**2],
                  [0, dt]])

    # 成本矩陣
    Q = np.diag([100, 1, 100, 1])  # 重視位置追蹤
    R = np.diag([0.1, 0.1])         # 控制能量權重

    N = 10  # 預測時域

    # 初始狀態
    state = np.array([radius, 0, 0, 2*np.pi*radius/len(t_traj)])  # [x, vx, y, vy]

    # 模擬
    states = [state.copy()]
    controls = []

    print("開始軌跡追蹤模擬...")

    for i in range(len(t_traj) - 1):
        # 當前參考點
        ref_state = np.array([x_ref[i], 0, y_ref[i], 0])

        # 簡化的 MPC：使用 LQR 風格的控制
        # 誤差
        error = ref_state - state

        # 簡單的比例控制（模擬 MPC）
        # 真實 MPC 會優化未來 N 步
        K = np.array([[10, 2, 0, 0],
                      [0, 0, 10, 2]])  # 反饋增益

        control = K @ error

        # 限制加速度
        control = np.clip(control, -50, 50)

        # 更新狀態
        state = A @ state + B @ control

        states.append(state.copy())
        controls.append(control)

    states = np.array(states)
    controls = np.array(controls)

    # 視覺化
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 軌跡
    axes[0].plot(x_ref, y_ref, 'r--', linewidth=2, label='參考軌跡')
    axes[0].plot(states[:, 0], states[:, 2], 'b-', linewidth=2, label='實際軌跡')
    axes[0].plot(states[0, 0], states[0, 2], 'go', markersize=10, label='起點')
    axes[0].plot(states[-1, 0], states[-1, 2], 'ro', markersize=10, label='終點')
    axes[0].set_xlabel('X (mm)')
    axes[0].set_ylabel('Y (mm)')
    axes[0].set_title('軌跡追蹤')
    axes[0].axis('equal')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # 追蹤誤差
    errors = np.sqrt((states[:-1, 0] - x_ref[:-1])**2 + (states[:-1, 2] - y_ref[:-1])**2)
    axes[1].plot(errors, 'b-', linewidth=2)
    axes[1].set_xlabel('步數')
    axes[1].set_ylabel('追蹤誤差 (mm)')
    axes[1].set_title('追蹤精度')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\2_calculus_kinematics\\trajectory_tracking.png', dpi=100)
    print("軌跡追蹤圖已儲存: trajectory_tracking.png")
    print(f"平均追蹤誤差: {np.mean(errors):.2f} mm")
    print(f"最大追蹤誤差: {np.max(errors):.2f} mm")
    plt.close()


# ============================================
# 第五部分：MPC 調試參數
# ============================================

def mpc_parameter_tuning():
    """MPC 參數調試示範"""
    print("\n" + "=" * 50)
    print("MPC 參數調試")
    print("=" * 50)

    print("""
    MPC 主要調試參數：

    1. 預測時域 N (Prediction Horizon)：
       - 太小：短視，性能差
       - 太大：計算量大，可能不穩定
       - 建議：10-30 步，取決於系統動態

    2. 狀態權重 Q：
       - 越大：越重視追蹤精度
       - 可以是對角矩陣，不同狀態不同權重
       - 例：位置比速度重要 -> Q = diag([100, 1])

    3. 控制權重 R：
       - 越大：越重視控制能量（更平滑）
       - 太大：反應慢
       - 太小：控制劇烈變化

    4. 約束：
       - 控制量約束：如最大加速度
       - 狀態約束：如最大速度
       - 約束越緊，優化越難

    調試建議：
    1. 先不加約束，調整 Q 和 R 達到基本性能
    2. 增加 Q/R 比值 -> 更快追蹤，但控制更激進
    3. 減少 Q/R 比值 -> 更平滑，但追蹤慢
    4. 最後加入約束，確保實際可行性
    """)

    # 示範不同參數的效果
    A = 0.9
    B = 0.1

    dt = 0.1
    t = np.arange(0, 5, dt)
    setpoint = 5.0

    configs = [
        {'Q': 1, 'R': 1, 'label': 'Q=1, R=1 (平衡)'},
        {'Q': 10, 'R': 0.1, 'label': 'Q=10, R=0.1 (快速追蹤)'},
        {'Q': 1, 'R': 10, 'label': 'Q=1, R=10 (平滑控制)'},
    ]

    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    for config in configs:
        mpc = SimpleMPC(A, B, Q=config['Q'], R=config['R'], N=10)

        x = 0.0
        states = []
        controls = []

        for _ in t:
            u, _ = mpc.compute_control(x, setpoint)
            x = A * x + B * u

            states.append(x)
            controls.append(u)

        axes[0].plot(t, states, linewidth=2, label=config['label'])
        axes[1].plot(t, controls, linewidth=2, label=config['label'])

    axes[0].axhline(y=setpoint, color='k', linestyle='--', alpha=0.5)
    axes[0].set_ylabel('狀態')
    axes[0].set_title('MPC 參數調試效果')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].set_xlabel('時間 (s)')
    axes[1].set_ylabel('控制輸入')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\2_calculus_kinematics\\mpc_tuning.png', dpi=100)
    print("MPC 參數調試圖已儲存: mpc_tuning.png")
    plt.close()


# ============================================
# 練習題
# ============================================

def exercises():
    """練習題"""
    print("\n" + "=" * 50)
    print("練習題")
    print("=" * 50)

    print("""
    練習 1: 實現基本 MPC
    - 系統：x[k+1] = 0.8*x[k] + 0.2*u[k]
    - 目標：從 x=0 控制到 x=10
    - 約束：-5 ≤ u ≤ 5
    - 調整 Q、R、N 以達到最佳性能

    練習 2: MPC with 約束
    - 在練習 1 基礎上，增加狀態約束：x ≤ 12
    - 觀察約束如何影響控制策略
    - 比較有無約束的差異

    練習 3: 多變量 MPC
    - 2D 點到點運動控制
    - 狀態：[x, y, vx, vy]
    - 控制：[ax, ay]
    - 從 (0, 0) 移動到 (100, 80)
    - 速度限制：|v| ≤ 50 mm/s

    練習 4: 參考軌跡追蹤
    - 追蹤一個正弦波軌跡
    - y_ref(t) = 50*sin(2π*0.1*t)
    - 計算追蹤誤差（RMSE）
    - 嘗試不同的 N 值，觀察效果

    練習 5: MPC vs PID 實戰
    - 設計一個有速度和加速度限制的定位系統
    - 分別用 MPC 和 PID 實現
    - 比較：
      - 響應時間
      - 超調量
      - 能否滿足約束
      - 計算時間
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
    print("模型預測控制 (MPC) 入門教學\n")

    # 執行所有示範
    mpc_theory()
    demonstrate_simple_mpc()
    compare_mpc_pid()
    trajectory_tracking_mpc()
    mpc_parameter_tuning()
    exercises()

    print("\n" + "=" * 50)
    print("微積分與運動學部分教學完成！")
    print("=" * 50)
    print("\n下一步：進入 3_image_processing 資料夾學習 OpenCV")
