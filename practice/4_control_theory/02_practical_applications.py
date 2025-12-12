"""
控制理論實際應用
適用於 AOI/上位機開發

學習目標：
1. 馬達速度控制
2. 位置伺服控制
3. 溫度控制
4. 多軸同步控制
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

# ============================================
# 第一部分：DC 馬達速度控制
# ============================================

class DCMotor:
    """DC 馬達模型"""

    def __init__(self, J=0.01, b=0.1, Kt=0.01, Ke=0.01, R=1.0, L=0.5):
        """
        參數:
            J: 轉動慣量 (kg·m²)
            b: 阻尼係數 (N·m·s)
            Kt: 轉矩常數 (N·m/A)
            Ke: 反電動勢常數 (V·s/rad)
            R: 電樞電阻 (Ω)
            L: 電樞電感 (H)
        """
        self.J = J
        self.b = b
        self.Kt = Kt
        self.Ke = Ke
        self.R = R
        self.L = L

        # 狀態變數
        self.omega = 0.0  # 角速度 (rad/s)
        self.i = 0.0      # 電流 (A)

    def update(self, voltage, dt):
        """
        更新馬達狀態

        運動方程：
        J * dω/dt = Kt * i - b * ω
        L * di/dt = V - R * i - Ke * ω
        """
        # 計算導數
        domega_dt = (self.Kt * self.i - self.b * self.omega) / self.J
        di_dt = (voltage - self.R * self.i - self.Ke * self.omega) / self.L

        # 更新狀態
        self.omega += domega_dt * dt
        self.i += di_dt * dt

        return self.omega


class PIDController:
    """簡化的 PID 控制器"""

    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.integral = 0
        self.prev_error = 0

    def compute(self, setpoint, measured, dt):
        error = setpoint - measured
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        self.prev_error = error

        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        return output


def motor_speed_control():
    """馬達速度控制範例"""
    print("=" * 50)
    print("DC 馬達速度控制")
    print("=" * 50)

    print("""
    系統組成：
    - DC 馬達（受控對象）
    - PID 控制器
    - 速度感測器

    目標：
    - 快速響應目標轉速
    - 抵抗負載擾動
    - 無穩態誤差
    """)

    # 模擬參數
    dt = 0.001  # 1ms 控制週期
    t_end = 5.0
    t = np.arange(0, t_end, dt)

    # 創建馬達和控制器
    motor = DCMotor()
    pid = PIDController(Kp=2.0, Ki=5.0, Kd=0.1)

    # 目標轉速 (rad/s)
    setpoint = np.zeros_like(t)
    setpoint[t >= 0.5] = 100  # 0.5s 時設定目標轉速 100 rad/s
    setpoint[t >= 2.5] = 150  # 2.5s 時改變目標

    # 負載擾動
    load_torque = np.zeros_like(t)
    load_torque[t >= 1.5] = 0.05  # 1.5s 時加入負載
    load_torque[t >= 3.5] = 0     # 3.5s 時移除負載

    # 模擬
    omega_history = []
    voltage_history = []

    for i in range(len(t)):
        # PID 控制
        voltage = pid.compute(setpoint[i], motor.omega, dt)
        voltage = np.clip(voltage, -24, 24)  # 限制電壓 ±24V

        # 馬達更新（加入負載）
        original_b = motor.b
        motor.b = original_b + load_torque[i]  # 模擬負載
        omega = motor.update(voltage, dt)
        motor.b = original_b

        omega_history.append(omega)
        voltage_history.append(voltage)

    omega_history = np.array(omega_history)
    voltage_history = np.array(voltage_history)

    # 轉換為 RPM
    rpm_history = omega_history * 60 / (2 * np.pi)
    rpm_setpoint = setpoint * 60 / (2 * np.pi)

    # 視覺化
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))

    # 轉速
    axes[0].plot(t, rpm_setpoint, 'r--', linewidth=2, label='目標轉速')
    axes[0].plot(t, rpm_history, 'b-', linewidth=2, label='實際轉速')
    axes[0].set_ylabel('轉速 (RPM)')
    axes[0].set_title('DC 馬達速度控制')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # 控制電壓
    axes[1].plot(t, voltage_history, 'g-', linewidth=2)
    axes[1].set_ylabel('控制電壓 (V)')
    axes[1].axhline(y=24, color='r', linestyle=':', alpha=0.5)
    axes[1].axhline(y=-24, color='r', linestyle=':', alpha=0.5)
    axes[1].grid(True, alpha=0.3)

    # 負載擾動
    axes[2].plot(t, load_torque, 'm-', linewidth=2)
    axes[2].set_xlabel('時間 (s)')
    axes[2].set_ylabel('負載 (N·m)')
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\4_control_theory\\motor_speed_control.png', dpi=100)
    print("馬達速度控制圖已儲存: motor_speed_control.png")
    plt.close()


# ============================================
# 第二部分：XY 平台位置控制
# ============================================

def xy_platform_control():
    """XY 平台位置控制"""
    print("\n" + "=" * 50)
    print("XY 平台位置控制")
    print("=" * 50)

    print("""
    應用場景：
    - AOI 檢測平台
    - PCB 組裝設備
    - 雷射切割機

    控制目標：
    - 精確定位（±0.01mm）
    - 平滑運動
    - 快速響應
    """)

    # 模擬參數
    dt = 0.001
    t_end = 3.0
    t = np.arange(0, t_end, dt)

    # 目標軌跡：矩形路徑
    target_x = np.zeros_like(t)
    target_y = np.zeros_like(t)

    # 四個角點
    corner_times = [0.5, 1.0, 1.5, 2.0, 2.5]
    corners = [(0, 0), (100, 0), (100, 80), (0, 80), (0, 0)]

    for i in range(len(corner_times)-1):
        mask = (t >= corner_times[i]) & (t < corner_times[i+1])
        target_x[mask] = corners[i+1][0]
        target_y[mask] = corners[i+1][1]

    # X 軸控制器
    pid_x = PIDController(Kp=50, Ki=20, Kd=5)
    # Y 軸控制器
    pid_y = PIDController(Kp=50, Ki=20, Kd=5)

    # 平台狀態
    x, y = 0.0, 0.0
    vx, vy = 0.0, 0.0

    # 平台參數
    mass = 1.0  # kg
    damping = 10.0  # N·s/m

    # 模擬
    x_history = []
    y_history = []

    for i in range(len(t)):
        # PID 控制力
        fx = pid_x.compute(target_x[i], x, dt)
        fy = pid_y.compute(target_y[i], y, dt)

        # 限制力
        fx = np.clip(fx, -500, 500)
        fy = np.clip(fy, -500, 500)

        # 運動方程：F = ma + bv
        ax = (fx - damping * vx) / mass
        ay = (fy - damping * vy) / mass

        # 更新速度和位置
        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt

        x_history.append(x)
        y_history.append(y)

    x_history = np.array(x_history)
    y_history = np.array(y_history)

    # 視覺化
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # XY 軌跡
    axes[0, 0].plot(target_x, target_y, 'r--', linewidth=2, label='目標軌跡')
    axes[0, 0].plot(x_history, y_history, 'b-', linewidth=2, label='實際軌跡')
    axes[0, 0].plot(corners[0][0], corners[0][1], 'go', markersize=10, label='起點')
    axes[0, 0].set_xlabel('X (mm)')
    axes[0, 0].set_ylabel('Y (mm)')
    axes[0, 0].set_title('XY 平台軌跡追蹤')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].axis('equal')

    # X 位置
    axes[0, 1].plot(t, target_x, 'r--', linewidth=2, label='目標')
    axes[0, 1].plot(t, x_history, 'b-', linewidth=2, label='實際')
    axes[0, 1].set_xlabel('時間 (s)')
    axes[0, 1].set_ylabel('X 位置 (mm)')
    axes[0, 1].set_title('X 軸位置追蹤')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Y 位置
    axes[1, 0].plot(t, target_y, 'r--', linewidth=2, label='目標')
    axes[1, 0].plot(t, y_history, 'b-', linewidth=2, label='實際')
    axes[1, 0].set_xlabel('時間 (s)')
    axes[1, 0].set_ylabel('Y 位置 (mm)')
    axes[1, 0].set_title('Y 軸位置追蹤')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # 追蹤誤差
    error = np.sqrt((target_x - x_history)**2 + (target_y - y_history)**2)
    axes[1, 1].plot(t, error, 'b-', linewidth=2)
    axes[1, 1].set_xlabel('時間 (s)')
    axes[1, 1].set_ylabel('位置誤差 (mm)')
    axes[1, 1].set_title('追蹤誤差')
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\4_control_theory\\xy_platform_control.png', dpi=100)
    print("XY 平台控制圖已儲存: xy_platform_control.png")
    print(f"最大追蹤誤差: {np.max(error):.3f} mm")
    print(f"平均追蹤誤差: {np.mean(error[t > 1.0]):.3f} mm")
    plt.close()


# ============================================
# 第三部分：溫度控制（非線性系統）
# ============================================

def furnace_temperature_control():
    """加熱爐溫度控制"""
    print("\n" + "=" * 50)
    print("加熱爐溫度控制")
    print("=" * 50)

    print("""
    挑戰：
    - 非線性系統（輻射散熱）
    - 大時間常數
    - 測量延遲

    解決方案：
    - PID 控制 + 前饋補償
    - 抗積分飽和
    - 分段控制策略
    """)

    # 模擬參數
    dt = 1.0  # 1 秒控制週期
    t_end = 600  # 10 分鐘
    t = np.arange(0, t_end, dt)

    # 目標溫度階段
    target_temp = np.ones_like(t) * 25  # 室溫
    target_temp[t >= 60] = 200   # 1分鐘後升溫到 200°C
    target_temp[t >= 300] = 300  # 5分鐘後升溫到 300°C
    target_temp[t >= 480] = 150  # 8分鐘後降溫到 150°C

    # PID 控制器
    pid = PIDController(Kp=5.0, Ki=0.2, Kd=10.0)

    # 溫度系統
    T = 25.0  # 當前溫度
    T_ambient = 25.0  # 環境溫度

    # 系統參數
    mass = 10.0  # kg
    specific_heat = 500  # J/(kg·K)
    heat_transfer_coeff = 50  # W/K
    max_heater_power = 5000  # W

    # 模擬
    temp_history = []
    power_history = []

    for i in range(len(t)):
        # PID 控制
        power = pid.compute(target_temp[i], T, dt)

        # 限制功率並防止積分飽和
        power_limited = np.clip(power, 0, max_heater_power)
        if power != power_limited:
            # 積分項回退
            error = target_temp[i] - T
            pid.integral -= error * dt

        # 熱量計算
        # 輸入：加熱器
        Q_in = power_limited * dt

        # 輸出：對流散熱（線性）+ 輻射散熱（非線性）
        Q_out_conv = heat_transfer_coeff * (T - T_ambient) * dt
        Q_out_rad = 5.67e-8 * 0.8 * 0.1 * (T**4 - T_ambient**4) * dt

        # 溫度變化
        dT = (Q_in - Q_out_conv - Q_out_rad) / (mass * specific_heat)
        T += dT

        temp_history.append(T)
        power_history.append(power_limited)

    temp_history = np.array(temp_history)
    power_history = np.array(power_history)

    # 視覺化
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    # 溫度
    axes[0].plot(t/60, target_temp, 'r--', linewidth=2, label='目標溫度')
    axes[0].plot(t/60, temp_history, 'b-', linewidth=2, label='實際溫度')
    axes[0].set_ylabel('溫度 (°C)')
    axes[0].set_title('加熱爐溫度控制')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # 加熱功率
    axes[1].plot(t/60, power_history/1000, 'g-', linewidth=2)
    axes[1].set_xlabel('時間 (分鐘)')
    axes[1].set_ylabel('加熱功率 (kW)')
    axes[1].axhline(y=max_heater_power/1000, color='r', linestyle=':', alpha=0.5)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\4_control_theory\\temperature_control.png', dpi=100)
    print("溫度控制圖已儲存: temperature_control.png")
    plt.close()


# ============================================
# 練習題
# ============================================

def exercises():
    """綜合練習"""
    print("\n" + "=" * 50)
    print("綜合練習")
    print("=" * 50)

    print("""
    練習 1: 伺服馬達調試
    - 使用提供的 DCMotor 類別
    - 調整 PID 參數以達到：
      - 上升時間 < 0.2s
      - 超調 < 5%
      - 穩態誤差 < 1%

    練習 2: 圓形軌跡追蹤
    - 修改 XY 平台程式
    - 追蹤半徑 50mm 的圓形軌跡
    - 計算追蹤精度

    練習 3: 串級控制
    - 實現溫度串級控制
    - 外環：溫度控制
    - 內環：加熱功率控制
    - 比較單環和串級的性能

    練習 4: 抗干擾設計
    - 在馬達控制中加入測量雜訊
    - 測試不同濾波器的效果
    - 調整控制器以抵抗雜訊

    練習 5: AOI 系統整合
    - 整合影像處理和運動控制
    - 實現：檢測瑕疵 -> 移動到瑕疵位置
    - 測量整個流程的週期時間
    """)


# ============================================
# 主程式
# ============================================

if __name__ == "__main__":
    print("控制理論實際應用教學\n")
    motor_speed_control()
    xy_platform_control()
    furnace_temperature_control()
    exercises()

    print("\n" + "=" * 50)
    print("全部教學完成！")
    print("=" * 50)
    print("\n恭喜完成所有課程！")
    print("你已經掌握 AOI/上位機開發的核心數學和程式技能！")
    print("\n📚 學習資源已準備完成，開始你的學習之旅吧！")
