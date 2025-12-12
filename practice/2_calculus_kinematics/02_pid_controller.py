"""
控制理論基礎 - PID 控制器
適用於 AOI/上位機開發

學習目標：
1. 理解 PID 控制原理
2. 實現基本的 PID 控制器
3. 應用於運動控制和溫度控制
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ============================================
# 第一部分：PID 基本原理
# ============================================

def pid_theory():
    """PID 控制原理"""
    print("=" * 50)
    print("PID 控制器原理")
    print("=" * 50)

    print("""
    PID = Proportional + Integral + Derivative

    控制公式:
    u(t) = Kp * e(t) + Ki * ∫e(t)dt + Kd * de(t)/dt

    其中:
    - e(t) = setpoint - measured_value  (誤差)
    - u(t) = 控制輸出

    各部分作用:
    - P (比例): 根據當前誤差調整，反應快但可能有穩態誤差
    - I (積分): 消除穩態誤差，累積歷史誤差
    - D (微分): 預測未來趨勢，減少超調和振盪

    離散形式（實際實現）:
    u[n] = Kp * e[n] + Ki * Σe[i]*Δt + Kd * (e[n] - e[n-1])/Δt
    """)


class PIDController:
    """PID 控制器類別"""

    def __init__(self, Kp, Ki, Kd, setpoint=0, output_limits=None):
        """
        初始化 PID 控制器

        參數:
            Kp: 比例增益
            Ki: 積分增益
            Kd: 微分增益
            setpoint: 目標值
            output_limits: 輸出限制 (min, max)
        """
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.output_limits = output_limits

        # 內部狀態
        self.integral = 0
        self.previous_error = 0
        self.previous_time = None

    def update(self, measured_value, dt=None):
        """
        更新 PID 控制器

        參數:
            measured_value: 當前測量值
            dt: 時間步長（秒）

        返回:
            control_output: 控制輸出
        """
        # 計算誤差
        error = self.setpoint - measured_value

        # P 項
        P = self.Kp * error

        # I 項（累積誤差）
        if dt is not None:
            self.integral += error * dt
        else:
            self.integral += error

        I = self.Ki * self.integral

        # D 項（誤差變化率）
        if dt is not None and dt > 0:
            derivative = (error - self.previous_error) / dt
        else:
            derivative = error - self.previous_error

        D = self.Kd * derivative

        # 計算輸出
        output = P + I + D

        # 限制輸出
        if self.output_limits is not None:
            output = np.clip(output, self.output_limits[0], self.output_limits[1])

            # 防止積分飽和（Anti-windup）
            # 如果輸出已經飽和，停止積分累積
            if output == self.output_limits[0] or output == self.output_limits[1]:
                self.integral -= error * (dt if dt is not None else 1)

        # 更新狀態
        self.previous_error = error

        return output

    def reset(self):
        """重置控制器狀態"""
        self.integral = 0
        self.previous_error = 0

    def set_gains(self, Kp=None, Ki=None, Kd=None):
        """調整 PID 增益"""
        if Kp is not None:
            self.Kp = Kp
        if Ki is not None:
            self.Ki = Ki
        if Kd is not None:
            self.Kd = Kd

    def get_components(self, measured_value, dt=None):
        """獲取 P、I、D 各項的值（用於分析）"""
        error = self.setpoint - measured_value

        P = self.Kp * error
        I = self.Ki * self.integral

        if dt is not None and dt > 0:
            derivative = (error - self.previous_error) / dt
        else:
            derivative = error - self.previous_error

        D = self.Kd * derivative

        return P, I, D


# ============================================
# 第二部分：模擬系統
# ============================================

class FirstOrderSystem:
    """一階系統（如溫度控制）"""

    def __init__(self, tau=1.0, initial_value=0):
        """
        參數:
            tau: 時間常數
            initial_value: 初始值
        """
        self.tau = tau
        self.value = initial_value

    def update(self, control_input, dt):
        """
        更新系統狀態

        一階系統微分方程: τ * dy/dt + y = u
        離散化: y[n+1] = y[n] + (u - y[n]) * dt / τ
        """
        self.value += (control_input - self.value) * dt / self.tau
        return self.value


class MassSpringDamper:
    """質量-彈簧-阻尼系統（如運動控制）"""

    def __init__(self, mass=1.0, damping=0.5, stiffness=1.0):
        """
        參數:
            mass: 質量
            damping: 阻尼係數
            stiffness: 剛度係數
        """
        self.m = mass
        self.c = damping
        self.k = stiffness

        self.position = 0
        self.velocity = 0

    def update(self, force, dt):
        """
        更新系統狀態

        運動方程: m*a = F - c*v - k*x
        """
        acceleration = (force - self.c * self.velocity - self.k * self.position) / self.m

        # 更新速度和位置
        self.velocity += acceleration * dt
        self.position += self.velocity * dt

        return self.position


# ============================================
# 第三部分：PID 調試示範
# ============================================

def demonstrate_p_control():
    """示範純 P 控制"""
    print("\n" + "=" * 50)
    print("P 控制（僅比例）")
    print("=" * 50)

    # 模擬參數
    dt = 0.01
    t_end = 10
    t = np.arange(0, t_end, dt)

    # 目標值
    setpoint = 100

    # 測試不同的 Kp 值
    Kp_values = [0.5, 1.0, 2.0, 4.0]

    plt.figure(figsize=(12, 6))

    for Kp in Kp_values:
        # 創建控制器和系統
        pid = PIDController(Kp=Kp, Ki=0, Kd=0, setpoint=setpoint)
        system = FirstOrderSystem(tau=1.0, initial_value=0)

        # 模擬
        output = []
        for _ in t:
            current = system.value
            control = pid.update(current, dt)
            system.update(control, dt)
            output.append(current)

        plt.plot(t, output, label=f'Kp={Kp}', linewidth=2)

    plt.axhline(y=setpoint, color='r', linestyle='--', label='目標值')
    plt.xlabel('時間 (s)')
    plt.ylabel('輸出')
    plt.title('P 控制：不同 Kp 值的響應')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\2_calculus_kinematics\\p_control.png', dpi=100)
    print("P 控制圖已儲存: p_control.png")
    print(f"觀察：Kp 越大反應越快，但可能產生超調")
    plt.close()


def demonstrate_pi_control():
    """示範 PI 控制"""
    print("\n" + "=" * 50)
    print("PI 控制（比例 + 積分）")
    print("=" * 50)

    dt = 0.01
    t_end = 10
    t = np.arange(0, t_end, dt)
    setpoint = 100

    # 比較 P 和 PI
    configs = [
        {'Kp': 1.0, 'Ki': 0, 'Kd': 0, 'label': 'P only (Kp=1.0)'},
        {'Kp': 1.0, 'Ki': 0.5, 'Kd': 0, 'label': 'PI (Kp=1.0, Ki=0.5)'},
        {'Kp': 1.0, 'Ki': 1.0, 'Kd': 0, 'label': 'PI (Kp=1.0, Ki=1.0)'},
    ]

    plt.figure(figsize=(12, 6))

    for config in configs:
        pid = PIDController(Kp=config['Kp'], Ki=config['Ki'], Kd=config['Kd'], setpoint=setpoint)
        system = FirstOrderSystem(tau=1.0, initial_value=0)

        output = []
        for _ in t:
            current = system.value
            control = pid.update(current, dt)
            system.update(control, dt)
            output.append(current)

        plt.plot(t, output, label=config['label'], linewidth=2)

    plt.axhline(y=setpoint, color='r', linestyle='--', label='目標值')
    plt.xlabel('時間 (s)')
    plt.ylabel('輸出')
    plt.title('PI 控制：消除穩態誤差')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\2_calculus_kinematics\\pi_control.png', dpi=100)
    print("PI 控制圖已儲存: pi_control.png")
    print("觀察：加入積分項（I）可以消除穩態誤差")
    plt.close()


def demonstrate_pid_control():
    """示範完整 PID 控制"""
    print("\n" + "=" * 50)
    print("PID 控制（完整）")
    print("=" * 50)

    dt = 0.01
    t_end = 5
    t = np.arange(0, t_end, dt)
    setpoint = 100

    configs = [
        {'Kp': 2.0, 'Ki': 1.0, 'Kd': 0, 'label': 'PI'},
        {'Kp': 2.0, 'Ki': 1.0, 'Kd': 0.5, 'label': 'PID (Kd=0.5)'},
        {'Kp': 2.0, 'Ki': 1.0, 'Kd': 1.0, 'label': 'PID (Kd=1.0)'},
    ]

    fig, axes = plt.subplots(2, 1, figsize=(12, 10))

    # 上圖：輸出響應
    ax1 = axes[0]
    for config in configs:
        pid = PIDController(Kp=config['Kp'], Ki=config['Ki'], Kd=config['Kd'], setpoint=setpoint)
        system = MassSpringDamper(mass=1.0, damping=0.1, stiffness=1.0)

        output = []
        for _ in t:
            current = system.position
            control = pid.update(current, dt)
            system.update(control, dt)
            output.append(current)

        ax1.plot(t, output, label=config['label'], linewidth=2)

    ax1.axhline(y=setpoint, color='r', linestyle='--', label='目標值')
    ax1.set_ylabel('位置')
    ax1.set_title('PID 控制：減少超調和振盪')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 下圖：誤差
    ax2 = axes[1]
    for config in configs:
        pid = PIDController(Kp=config['Kp'], Ki=config['Ki'], Kd=config['Kd'], setpoint=setpoint)
        system = MassSpringDamper(mass=1.0, damping=0.1, stiffness=1.0)

        errors = []
        for _ in t:
            current = system.position
            error = setpoint - current
            control = pid.update(current, dt)
            system.update(control, dt)
            errors.append(error)

        ax2.plot(t, errors, label=config['label'], linewidth=2)

    ax2.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax2.set_xlabel('時間 (s)')
    ax2.set_ylabel('誤差')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\2_calculus_kinematics\\pid_control.png', dpi=100)
    print("PID 控制圖已儲存: pid_control.png")
    print("觀察：加入微分項（D）可以減少超調和振盪")
    plt.close()


def visualize_pid_components():
    """視覺化 PID 各項貢獻"""
    print("\n" + "=" * 50)
    print("PID 各項分析")
    print("=" * 50)

    dt = 0.01
    t_end = 5
    t = np.arange(0, t_end, dt)
    setpoint = 100

    # PID 參數
    Kp, Ki, Kd = 2.0, 1.0, 0.5

    pid = PIDController(Kp=Kp, Ki=Ki, Kd=Kd, setpoint=setpoint)
    system = FirstOrderSystem(tau=0.5, initial_value=0)

    # 記錄數據
    outputs = []
    P_values = []
    I_values = []
    D_values = []
    controls = []

    for _ in t:
        current = system.value
        P, I, D = pid.get_components(current, dt)
        control = pid.update(current, dt)

        system.update(control, dt)

        outputs.append(current)
        P_values.append(P)
        I_values.append(I)
        D_values.append(D)
        controls.append(control)

    # 視覺化
    fig, axes = plt.subplots(3, 1, figsize=(12, 12))

    # 輸出響應
    axes[0].plot(t, outputs, 'b-', linewidth=2, label='實際輸出')
    axes[0].axhline(y=setpoint, color='r', linestyle='--', label='目標值')
    axes[0].set_ylabel('輸出')
    axes[0].set_title(f'PID 各項分析 (Kp={Kp}, Ki={Ki}, Kd={Kd})')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # PID 各項
    axes[1].plot(t, P_values, 'r-', linewidth=2, label='P 項')
    axes[1].plot(t, I_values, 'g-', linewidth=2, label='I 項')
    axes[1].plot(t, D_values, 'b-', linewidth=2, label='D 項')
    axes[1].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    axes[1].set_ylabel('貢獻值')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    # 控制輸出
    axes[2].plot(t, controls, 'm-', linewidth=2, label='總控制輸出 (P+I+D)')
    axes[2].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    axes[2].set_xlabel('時間 (s)')
    axes[2].set_ylabel('控制輸出')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\2_calculus_kinematics\\pid_components.png', dpi=100)
    print("PID 各項分析圖已儲存: pid_components.png")
    plt.close()


# ============================================
# 第四部分：實際應用
# ============================================

def temperature_control_simulation():
    """溫度控制模擬"""
    print("\n" + "=" * 50)
    print("實際應用：溫度控制")
    print("=" * 50)

    # 模擬加熱器控制溫度到 150°C
    dt = 0.1  # 100ms 採樣
    t_end = 60  # 60 秒
    t = np.arange(0, t_end, dt)

    target_temp = 150  # 目標溫度
    room_temp = 25     # 室溫

    # PID 控制器
    pid = PIDController(Kp=5.0, Ki=0.2, Kd=2.0, setpoint=target_temp, output_limits=(0, 100))

    # 溫度系統（熱慣性）
    temp_system = FirstOrderSystem(tau=5.0, initial_value=room_temp)

    # 模擬
    temperatures = []
    heater_powers = []

    for ti in t:
        current_temp = temp_system.value
        heater_power = pid.update(current_temp, dt)

        # 加熱器功率影響溫度上升，同時有散熱
        heat_input = heater_power * 2  # 加熱效率
        heat_loss = (current_temp - room_temp) * 0.1  # 散熱
        net_heat = heat_input - heat_loss

        temp_system.update(current_temp + net_heat * dt / 10, dt)

        temperatures.append(current_temp)
        heater_powers.append(heater_power)

    # 視覺化
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    # 溫度
    axes[0].plot(t, temperatures, 'r-', linewidth=2, label='實際溫度')
    axes[0].axhline(y=target_temp, color='b', linestyle='--', label='目標溫度')
    axes[0].fill_between(t, target_temp-2, target_temp+2, alpha=0.2, color='g', label='允許範圍 ±2°C')
    axes[0].set_ylabel('溫度 (°C)')
    axes[0].set_title('PID 溫度控制模擬')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # 加熱器功率
    axes[1].plot(t, heater_powers, 'g-', linewidth=2, label='加熱器功率')
    axes[1].set_xlabel('時間 (s)')
    axes[1].set_ylabel('功率 (%)')
    axes[1].set_ylim(-5, 105)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\2_calculus_kinematics\\temperature_control.png', dpi=100)
    print("溫度控制圖已儲存: temperature_control.png")
    print(f"穩定時間: ~{t[np.argmax(np.array(temperatures) > target_temp-2)]:.1f} 秒")
    plt.close()


def motor_position_control():
    """馬達位置控制"""
    print("\n" + "=" * 50)
    print("實際應用：馬達位置控制")
    print("=" * 50)

    dt = 0.001  # 1ms 控制週期
    t_end = 2
    t = np.arange(0, t_end, dt)

    # 目標位置（階梯輸入）
    setpoints = np.zeros_like(t)
    setpoints[t >= 0.5] = 100
    setpoints[t >= 1.0] = 50
    setpoints[t >= 1.5] = 150

    # PID 控制器
    pid = PIDController(Kp=50, Ki=10, Kd=5, setpoint=0, output_limits=(-1000, 1000))

    # 馬達系統
    motor = MassSpringDamper(mass=0.1, damping=1.0, stiffness=0)

    # 模擬
    positions = []
    velocities = []
    forces = []

    for i, ti in enumerate(t):
        # 更新目標值
        pid.setpoint = setpoints[i]

        # PID 控制
        current_pos = motor.position
        force = pid.update(current_pos, dt)

        # 更新馬達
        motor.update(force, dt)

        positions.append(current_pos)
        velocities.append(motor.velocity)
        forces.append(force)

    # 視覺化
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))

    # 位置
    axes[0].plot(t, positions, 'b-', linewidth=2, label='實際位置')
    axes[0].plot(t, setpoints, 'r--', linewidth=2, label='目標位置')
    axes[0].set_ylabel('位置 (mm)')
    axes[0].set_title('PID 馬達位置控制')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # 速度
    axes[1].plot(t, velocities, 'g-', linewidth=2)
    axes[1].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    axes[1].set_ylabel('速度 (mm/s)')
    axes[1].grid(True, alpha=0.3)

    # 控制力
    axes[2].plot(t, forces, 'm-', linewidth=2)
    axes[2].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    axes[2].set_xlabel('時間 (s)')
    axes[2].set_ylabel('控制力 (N)')
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\2_calculus_kinematics\\motor_control.png', dpi=100)
    print("馬達控制圖已儲存: motor_control.png")
    plt.close()


# ============================================
# 第五部分：PID 調試技巧
# ============================================

def pid_tuning_guide():
    """PID 調試指南"""
    print("\n" + "=" * 50)
    print("PID 調試指南")
    print("=" * 50)

    print("""
    Ziegler-Nichols 調試法（經典方法）：

    步驟 1：設定 Ki=0, Kd=0，只調整 Kp
    - 逐漸增加 Kp 直到系統開始持續振盪
    - 記錄此時的 Kp 值（稱為 Ku）和振盪週期 Tu

    步驟 2：根據控制器類型設定參數

    P 控制：
        Kp = 0.5 * Ku

    PI 控制：
        Kp = 0.45 * Ku
        Ki = 0.54 * Ku / Tu

    PID 控制：
        Kp = 0.6 * Ku
        Ki = 1.2 * Ku / Tu
        Kd = 0.075 * Ku * Tu

    手動調試法（推薦用於實際系統）：

    1. 設定所有增益為 0
    2. 增加 Kp 直到響應快速但穩定（允許小幅振盪）
    3. 增加 Ki 來消除穩態誤差（慢慢增加，避免振盪）
    4. 增加 Kd 來減少超調和振盪（如果需要）

    調試技巧：
    - Kp 太大 -> 超調、振盪
    - Kp 太小 -> 響應慢、穩態誤差大
    - Ki 太大 -> 振盪、不穩定
    - Ki 太小 -> 穩態誤差無法消除
    - Kd 太大 -> 對噪聲敏感、振盪
    - Kd 太小 -> 超調大

    常見問題：
    - 積分飽和：使用 Anti-windup
    - 噪聲敏感：降低 Kd 或加濾波器
    - 控制死區：增加最小輸出
    """)


def compare_tuning_methods():
    """比較不同的 PID 參數"""
    print("\n" + "=" * 50)
    print("PID 參數調試比較")
    print("=" * 50)

    dt = 0.01
    t_end = 8
    t = np.arange(0, t_end, dt)
    setpoint = 100

    configs = [
        {'Kp': 0.5, 'Ki': 0, 'Kd': 0, 'label': '欠調整 (太慢)'},
        {'Kp': 2.0, 'Ki': 1.0, 'Kd': 0.5, 'label': '良好調整'},
        {'Kp': 10.0, 'Ki': 5.0, 'Kd': 0, 'label': '過調整 (振盪)'},
    ]

    plt.figure(figsize=(12, 6))

    for config in configs:
        pid = PIDController(Kp=config['Kp'], Ki=config['Ki'], Kd=config['Kd'], setpoint=setpoint)
        system = FirstOrderSystem(tau=1.0, initial_value=0)

        output = []
        for _ in t:
            current = system.value
            control = pid.update(current, dt)
            system.update(control, dt)
            output.append(current)

        plt.plot(t, output, label=config['label'], linewidth=2)

    plt.axhline(y=setpoint, color='r', linestyle='--', label='目標值')
    plt.xlabel('時間 (s)')
    plt.ylabel('輸出')
    plt.title('PID 調試比較')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\2_calculus_kinematics\\pid_tuning.png', dpi=100)
    print("PID 調試比較圖已儲存: pid_tuning.png")
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
    練習 1: 實現 PID 控制器
    - 模擬一個簡單的 RC 電路（一階系統，τ=2.0）
    - 設計 PID 控制器使溫度從 20°C 上升到 80°C
    - 要求：上升時間 < 5s，超調 < 10%，穩態誤差 < 1°C
    - 繪製響應曲線

    練習 2: 手動調試
    - 使用給定的系統（MassSpringDamper, m=1, c=0.5, k=1）
    - 從 Kp=0, Ki=0, Kd=0 開始
    - 按照手動調試法找到合適的參數
    - 記錄每次調整的結果

    練習 3: 抗干擾測試
    - 在練習 1 的基礎上，加入外部干擾
    - 在 t=5s 時，系統受到 -20 的階躍干擾
    - 觀察 PID 控制器的恢復能力
    - 嘗試調整參數以提高抗干擾性

    練習 4: 積分飽和問題
    - 設計一個有輸出限制的系統（如馬達電流限制）
    - 目標值變化很大（如 0 -> 1000）
    - 觀察有無 Anti-windup 的差異
    - 實現並測試 Anti-windup 算法

    練習 5: 實際應用
    - 模擬 AOI 平台的 XY 軸定位
    - 兩個軸都需要 PID 控制
    - 目標：從 (0, 0) 移動到 (100, 80)
    - 要求：定位精度 ±0.1mm，穩定時間 < 1s
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
    print("PID 控制器教學\n")

    # 執行所有示範
    pid_theory()
    demonstrate_p_control()
    demonstrate_pi_control()
    demonstrate_pid_control()
    visualize_pid_components()
    temperature_control_simulation()
    motor_position_control()
    pid_tuning_guide()
    compare_tuning_methods()
    exercises()

    print("\n" + "=" * 50)
    print("教學完成！")
    print("=" * 50)
    print("\n下一步：學習 03_mpc_intro.py（模型預測控制入門）")
