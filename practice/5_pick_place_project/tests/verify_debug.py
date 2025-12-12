"""驗證 debug_angle.py 的輸出是否正確"""
import subprocess
import re

print("運行 debug_angle.py 並檢查輸出...")
print("=" * 70)

# 運行腳本但不顯示圖形
result = subprocess.run(
    ['python', 'debug_angle.py'],
    capture_output=True,
    text=True,
    timeout=60,
    env={'MPLBACKEND': 'Agg'}  # 使用非交互式後端
)

output = result.stdout

# 檢查 -30° 的輸出
if "測試角度: -30°" in output:
    # 找到 -30° 測試後的檢測結果
    pattern = r"測試角度: -30°.*?檢測結果比較:(.*?)(?=視覺化|測試角度|檢測摘要|$)"
    match = re.search(pattern, output, re.DOTALL)

    if match:
        result_section = match.group(1)
        print("\n-30° 測試結果:")
        print(result_section)

        # 檢查誤差是否小於 1°
        errors = re.findall(r'誤差: (\d+\.\d+)°', result_section)
        print(f"\n找到的誤差值: {errors}")

        all_small = all(float(e) < 1.0 for e in errors)
        if all_small:
            print("\n✓ 所有誤差都 < 1°！")
        else:
            print("\n✗ 仍有誤差 > 1°")

# 檢查摘要
if "檢測摘要" in output:
    lines = output.split('\n')
    summary_started = False
    print("\n" + "=" * 70)
    print("檢測摘要:")
    print("=" * 70)
    for line in lines:
        if "檢測摘要" in line:
            summary_started = True
        if summary_started and ("OK" in line or "FAIL" in line):
            print(line)
