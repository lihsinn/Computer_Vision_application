"""
控制理論基礎
適用於 AOI/上位機開發

學習目標：
1. 控制系統基本概念
2. 系統建模
3. 穩定性分析
4. 頻率響應
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def control_theory_basics():
    """控制理論基本概念"""
    print("=" * 50)
    print("控制理論基礎")
    print("=" * 50)

    print("""
    控制系統基本組成：
    1. 受控對象（Plant）：需要控制的系統
    2. 控制器（Controller）：產生控制信號
    3. 感測器（Sensor）：測量系統輸出
    4. 執行器（Actuator）：執行控制動作

    控制系統類型：
    - 開迴路控制：無回饋
    - 閉迴路控制：有回饋（常用）

    性能指標：
    - 穩定性（Stability）
    - 準確性（Accuracy）
    - 快速性（Speed）
    - 抗干擾性（Robustness）

    常用控制方法：
    - PID 控制：簡單、實用
    - MPC：處理約束、預測
    - 狀態回饋：現代控制理論
    - 模糊控制：處理非線性
    """)


def system_modeling():
    """系統建模"""
    print("\n" + "=" * 50)
    print("系統建模")
    print("=" * 50)

    print("""
    傳遞函數（Transfer Function）：
    - 描述系統輸入輸出關係
    - G(s) = Y(s) / U(s)
    - s 是拉普拉斯變數

    一階系統：
    G(s) = K / (τs + 1)
    - K：增益
    - τ：時間常數

    二階系統：
    G(s) = ωn² / (s² + 2ζωns + ωn²)
    - ωn：自然頻率
    - ζ：阻尼比

    狀態空間模型：
    dx/dt = Ax + Bu
    y = Cx + Du
    """)

    # 示範一階系統階躍響應
    K = 1.0
    tau = 1.0
    num = [K]
    den = [tau, 1]
    sys = signal.TransferFunction(num, den)

    t, y = signal.step(sys)

    plt.figure(figsize=(10, 6))
    plt.plot(t, y, 'b-', linewidth=2, label=f'K={K}, τ={tau}')
    plt.axhline(y=K, color='r', linestyle='--', alpha=0.5, label='最終值')
    plt.axhline(y=K*0.63, color='g', linestyle=':', alpha=0.5, label='63% (1τ)')
    plt.xlabel('時間 (s)')
    plt.ylabel('輸出')
    plt.title('一階系統階躍響應')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\4_control_theory\\first_order_system.png', dpi=100)
    print("一階系統響應圖已儲存")
    plt.close()


def second_order_systems():
    """二階系統特性"""
    print("\n" + "=" * 50)
    print("二階系統特性")
    print("=" * 50)

    print("""
    二階系統是控制系統的基本模型
    G(s) = ωn² / (s² + 2ζωns + ωn²)

    阻尼比 ζ 的影響：
    - ζ < 1：欠阻尼（有超調）
    - ζ = 1：臨界阻尼
    - ζ > 1：過阻尼（無超調但慢）
    """)

    # 不同阻尼比的響應
    wn = 2 * np.pi  # 自然頻率
    damping_ratios = [0.1, 0.5, 0.707, 1.0, 2.0]

    plt.figure(figsize=(12, 6))

    for zeta in damping_ratios:
        num = [wn**2]
        den = [1, 2*zeta*wn, wn**2]
        sys = signal.TransferFunction(num, den)
        t, y = signal.step(sys)

        label = f'ζ={zeta}'
        if zeta < 1:
            label += ' (欠阻尼)'
        elif zeta == 1:
            label += ' (臨界)'
        else:
            label += ' (過阻尼)'

        plt.plot(t, y, linewidth=2, label=label)

    plt.axhline(y=1, color='k', linestyle='--', alpha=0.3)
    plt.xlabel('時間 (s)')
    plt.ylabel('輸出')
    plt.title('二階系統：不同阻尼比的階躍響應')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\4_control_theory\\second_order_system.png', dpi=100)
    print("二階系統響應圖已儲存")
    plt.close()


def stability_analysis():
    """穩定性分析"""
    print("\n" + "=" * 50)
    print("穩定性分析")
    print("=" * 50)

    print("""
    穩定性判斷：
    1. 極點位置：
       - 所有極點在左半平面 → 穩定
       - 有極點在右半平面 → 不穩定

    2. Routh-Hurwitz 準則：
       - 代數判據

    3. Nyquist 準則：
       - 頻域判據

    4. 波德圖：
       - 增益裕度（Gain Margin）
       - 相位裕度（Phase Margin）

    常見問題：
    - 增益過大 → 振盪、不穩定
    - 延遲過大 → 相位滯後、不穩定
    """)

    # 示範穩定和不穩定系統
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 穩定系統
    num = [1]
    den = [1, 3, 2]  # 極點在 -1, -2
    sys_stable = signal.TransferFunction(num, den)
    t, y = signal.step(sys_stable)

    axes[0].plot(t, y, 'b-', linewidth=2)
    axes[0].set_title('穩定系統\n極點: -1, -2 (左半平面)')
    axes[0].set_xlabel('時間 (s)')
    axes[0].set_ylabel('輸出')
    axes[0].grid(True, alpha=0.3)

    # 不穩定系統模擬
    t2 = np.linspace(0, 5, 500)
    y2 = np.exp(0.5 * t2)  # 指數增長

    axes[1].plot(t2, y2, 'r-', linewidth=2)
    axes[1].set_title('不穩定系統\n極點: +0.5 (右半平面)')
    axes[1].set_xlabel('時間 (s)')
    axes[1].set_ylabel('輸出')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\4_control_theory\\stability.png', dpi=100)
    print("穩定性分析圖已儲存")
    plt.close()


def frequency_response():
    """頻率響應"""
    print("\n" + "=" * 50)
    print("頻率響應（波德圖）")
    print("=" * 50)

    print("""
    波德圖（Bode Plot）：
    - 增益圖：顯示系統放大倍率
    - 相位圖：顯示輸出相對輸入的相位差

    重要參數：
    - 頻寬（Bandwidth）：系統響應頻率範圍
    - 截止頻率：增益下降 3dB 處
    - 相位裕度：穩定性指標

    應用：
    - 濾波器設計
    - 控制器調整
    - 系統診斷
    """)

    # 創建一個二階系統
    wn = 10  # rad/s
    zeta = 0.5
    num = [wn**2]
    den = [1, 2*zeta*wn, wn**2]
    sys = signal.TransferFunction(num, den)

    # 計算頻率響應
    w, mag, phase = signal.bode(sys)

    # 繪製波德圖
    fig, axes = plt.subplots(2, 1, figsize=(10, 10))

    # 增益圖
    axes[0].semilogx(w, mag, 'b-', linewidth=2)
    axes[0].axhline(y=-3, color='r', linestyle='--', alpha=0.5, label='-3dB')
    axes[0].set_ylabel('增益 (dB)')
    axes[0].set_title(f'波德圖 (ωn={wn} rad/s, ζ={zeta})')
    axes[0].grid(True, alpha=0.3, which='both')
    axes[0].legend()

    # 相位圖
    axes[1].semilogx(w, phase, 'g-', linewidth=2)
    axes[1].set_xlabel('頻率 (rad/s)')
    axes[1].set_ylabel('相位 (度)')
    axes[1].grid(True, alpha=0.3, which='both')

    plt.tight_layout()
    plt.savefig('C:\\Users\\Liily.Chen\\Desktop\\computer-vision-application\\practice\\4_control_theory\\bode_plot.png', dpi=100)
    print("波德圖已儲存")
    plt.close()


def exercises():
    """練習題"""
    print("\n" + "=" * 50)
    print("練習題")
    print("=" * 50)

    print("""
    練習 1: 一階系統分析
    - 給定傳遞函數 G(s) = 5 / (2s + 1)
    - 計算系統增益 K 和時間常數 τ
    - 繪製階躍響應
    - 計算 63% 上升時間

    練習 2: 二階系統特性
    - 給定 ωn = 5 rad/s, ζ = 0.3
    - 計算超調量（Overshoot）
    - 計算峰值時間（Peak Time）
    - 計算穩定時間（Settling Time）

    練習 3: 穩定性判斷
    - 給定特徵方程 s³ + 6s² + 11s + 6 = 0
    - 求極點位置
    - 判斷系統穩定性
    - 繪製極點分布圖

    練習 4: 頻率響應
    - 設計一個低通濾波器 fc = 10 Hz
    - 繪製波德圖
    - 計算 -3dB 頻率
    - 驗證濾波效果

    練習 5: 綜合應用
    - 模擬一個 RC 電路
    - 推導傳遞函數
    - 分析頻率響應
    - 計算時間常數
    """)



def main():
    print("控制理論基礎教學\n")
    control_theory_basics()
    system_modeling()
    second_order_systems()
    stability_analysis()
    frequency_response()
    exercises()

    print("\n" + "=" * 50)
    print("教學完成！")
    print("=" * 50)
    print("\n下一步：學習 02_practical_applications.py（實際應用）")


if __name__ == "__main__":
    main()
