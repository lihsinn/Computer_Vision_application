"""
AOI 系統整合範例
Integration Example with AOI System

展示如何將旋轉角度檢測整合到現有的 AOI 系統
"""

import numpy as np
import cv2
from typing import Dict, Tuple, Optional


class RotationDetector:
    """旋轉角度檢測器類別"""

    def __init__(self, method='minAreaRect'):
        """
        初始化檢測器

        Args:
            method: 檢測方法 ('minAreaRect', 'pca', 'markers')
        """
        self.method = method

    def detect(self, image: np.ndarray, bbox: Optional[Dict] = None) -> Dict:
        """
        檢測物件旋轉角度

        Args:
            image: 輸入影像
            bbox: 物件邊界框 {'x1', 'y1', 'x2', 'y2'}（可選）

        Returns:
            結果字典：{
                'angle': 旋轉角度,
                'center': 中心座標,
                'success': 是否成功
            }
        """
        # 如果有 bbox，裁切影像
        if bbox:
            x1, y1 = bbox['x1'], bbox['y1']
            x2, y2 = bbox['x2'], bbox['y2']
            roi = image[y1:y2, x1:x2]
            offset = (x1, y1)
        else:
            roi = image
            offset = (0, 0)

        # 轉為灰階
        if len(roi.shape) == 3:
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        else:
            gray = roi

        # 二值化
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # 尋找輪廓
        contours, _ = cv2.findContours(
            binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if len(contours) == 0:
            return {'success': False, 'angle': 0, 'center': (0, 0)}

        # 取最大輪廓
        largest_contour = max(contours, key=cv2.contourArea)

        # 根據方法檢測角度
        if self.method == 'minAreaRect':
            angle, center = self._detect_with_min_area_rect(largest_contour)
        elif self.method == 'pca':
            angle, center = self._detect_with_pca(largest_contour)
        else:
            return {'success': False, 'angle': 0, 'center': (0, 0)}

        # 加上偏移
        center = (center[0] + offset[0], center[1] + offset[1])

        return {
            'success': True,
            'angle': angle,
            'center': center,
            'method': self.method
        }

    def _detect_with_min_area_rect(self, contour) -> Tuple[float, Tuple[int, int]]:
        """使用最小面積矩形檢測"""
        rect = cv2.minAreaRect(contour)
        center, size, angle = rect

        # 角度正規化
        if size[0] < size[1]:
            angle = angle + 90

        return angle, (int(center[0]), int(center[1]))

    def _detect_with_pca(self, contour) -> Tuple[float, Tuple[int, int]]:
        """使用 PCA 檢測"""
        # 計算質心
        M = cv2.moments(contour)
        if M["m00"] == 0:
            return 0, (0, 0)

        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        # PCA
        pts = contour.reshape(-1, 2).astype(np.float32)
        mean, eigenvectors = cv2.PCACompute(pts, mean=None)
        main_direction = eigenvectors[0]

        # 計算角度
        angle = np.degrees(np.arctan2(main_direction[1], main_direction[0]))
        if angle < 0:
            angle += 360

        return angle, (cx, cy)


class AOIWithRotation:
    """
    整合旋轉檢測的 AOI 系統
    模擬與後端 API 的整合
    """

    def __init__(self):
        self.rotation_detector = RotationDetector(method='minAreaRect')

    def inspect_and_pick(self, image: np.ndarray, defect_threshold: float = 0.5):
        """
        檢測瑕疵並計算抓取資訊

        Args:
            image: 輸入影像
            defect_threshold: 瑕疵閾值

        Returns:
            檢測結果和抓取指令
        """
        results = {
            'inspection': None,
            'pick_command': None
        }

        # 1. AOI 檢測（模擬）
        inspection_result = self._simulate_aoi_inspection(image)
        results['inspection'] = inspection_result

        # 2. 如果需要抓取，計算旋轉角度
        if inspection_result['needs_removal']:
            rotation_info = self.rotation_detector.detect(
                image,
                bbox=inspection_result['bbox']
            )

            if rotation_info['success']:
                # 3. 生成機器人指令
                pick_command = self._generate_pick_command(
                    rotation_info,
                    inspection_result
                )
                results['pick_command'] = pick_command

        return results

    def _simulate_aoi_inspection(self, image: np.ndarray) -> Dict:
        """模擬 AOI 檢測"""
        # 這裡模擬檢測結果
        # 實際應用中會呼叫真實的 AOI 檢測模組

        # 尋找物件
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(
            binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if len(contours) == 0:
            return {'needs_removal': False}

        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)

        # 模擬瑕疵檢測
        defect_score = np.random.random()

        return {
            'needs_removal': defect_score > 0.3,  # 70% 需要移除
            'defect_score': defect_score,
            'defect_type': 'NG' if defect_score > 0.5 else 'PASS',
            'bbox': {'x1': x, 'y1': y, 'x2': x+w, 'y2': y+h}
        }

    def _generate_pick_command(
        self,
        rotation_info: Dict,
        inspection_result: Dict
    ) -> Dict:
        """
        生成機器人抓取指令

        Args:
            rotation_info: 旋轉資訊
            inspection_result: 檢測結果

        Returns:
            機器人指令
        """
        center = rotation_info['center']
        angle = rotation_info['angle']

        # 座標轉換（像素 -> 機器人座標）
        # 假設：相機視野中心 = 機器人原點
        # 實際需要相機標定
        PIXEL_TO_MM = 0.1
        IMAGE_CENTER_X = 250  # 假設影像中心
        IMAGE_CENTER_Y = 250

        robot_x = (center[0] - IMAGE_CENTER_X) * PIXEL_TO_MM
        robot_y = (IMAGE_CENTER_Y - center[1]) * PIXEL_TO_MM

        # 決定放置位置（根據檢測結果）
        if inspection_result['defect_type'] == 'NG':
            place_x, place_y = 100.0, 100.0  # NG 區
            bin_type = 'NG'
        else:
            place_x, place_y = -100.0, 100.0  # PASS 區
            bin_type = 'PASS'

        command = {
            'action': 'pick_and_place',
            'pick_position': {
                'x': robot_x,
                'y': robot_y,
                'z': 0.0,
                'rotation': angle
            },
            'place_position': {
                'x': place_x,
                'y': place_y,
                'z': 0.0,
                'rotation': 0.0
            },
            'gripper_rotation': angle,
            'bin_type': bin_type,
            'defect_score': inspection_result['defect_score']
        }

        return command


# ============================================
# 使用範例
# ============================================

def demo_integration():
    """示範整合使用"""
    print("=" * 60)
    print("AOI 系統整合範例")
    print("=" * 60)

    # 創建測試影像（旋轉的矩形）
    img = np.zeros((500, 500, 3), dtype=np.uint8)
    img[:] = (200, 200, 200)  # 灰色背景

    # 創建旋轉物件
    angle = 42.0
    center = (250, 250)
    size = (120, 80)
    rect = (center, size, angle)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img, [box], 0, (100, 150, 200), -1)

    # 初始化系統
    aoi_system = AOIWithRotation()

    # 執行檢測和生成指令
    print("\n執行檢測...")
    results = aoi_system.inspect_and_pick(img)

    # 顯示結果
    print("\n檢測結果：")
    print(f"  瑕疵分數：{results['inspection']['defect_score']:.3f}")
    print(f"  判定：{results['inspection']['defect_type']}")
    print(f"  需要移除：{results['inspection']['needs_removal']}")

    if results['pick_command']:
        print("\n🤖 機器人指令：")
        cmd = results['pick_command']
        print(f"  動作：{cmd['action']}")
        print(f"  抓取位置：")
        print(f"    X = {cmd['pick_position']['x']:7.2f} mm")
        print(f"    Y = {cmd['pick_position']['y']:7.2f} mm")
        print(f"    旋轉 = {cmd['pick_position']['rotation']:6.2f}°")
        print(f"  放置位置：{cmd['bin_type']} 區")
        print(f"    X = {cmd['place_position']['x']:7.2f} mm")
        print(f"    Y = {cmd['place_position']['y']:7.2f} mm")

    # 視覺化
    result_img = img.copy()

    # 繪製檢測框
    bbox = results['inspection']['bbox']
    cv2.rectangle(result_img,
                 (bbox['x1'], bbox['y1']),
                 (bbox['x2'], bbox['y2']),
                 (0, 255, 0), 2)

    if results['pick_command']:
        # 繪製抓取點和角度
        pick_pos = results['pick_command']['pick_position']
        cx, cy = center

        # 繪製角度指示
        angle_rad = np.radians(pick_pos['rotation'])
        arrow_len = 60
        end_x = int(cx + arrow_len * np.cos(angle_rad))
        end_y = int(cy + arrow_len * np.sin(angle_rad))

        cv2.circle(result_img, (cx, cy), 5, (0, 0, 255), -1)
        cv2.arrowedLine(result_img, (cx, cy), (end_x, end_y),
                       (255, 0, 0), 2, tipLength=0.3)

        # 顯示資訊
        cv2.putText(result_img, f"{pick_pos['rotation']:.1f} deg",
                   (cx + 10, cy - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.putText(result_img, results['inspection']['defect_type'],
                   (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('AOI + Rotation Detection', result_img)
    print("\n按任意鍵關閉視窗...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("\n✅ 示範完成！")


# ============================================
# Flask API 端點範例
# ============================================

def flask_api_example():
    """
    Flask API 整合範例代碼
    可以加到 aoi-system/backend/app/routes/ 中
    """
    example_code = """
# aoi-system/backend/app/routes/rotation_detection.py

from flask import Blueprint, request, jsonify
import cv2
import numpy as np
from app.services.rotation_detector import RotationDetector

rotation_bp = Blueprint('rotation', __name__)
detector = RotationDetector(method='minAreaRect')

@rotation_bp.route('/api/detect_rotation', methods=['POST'])
def detect_rotation():
    '''檢測物件旋轉角度'''

    # 接收影像
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image provided'}), 400

    # 讀取影像
    image_bytes = file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 檢測旋轉角度
    result = detector.detect(image)

    if result['success']:
        return jsonify({
            'success': True,
            'angle': result['angle'],
            'center': result['center'],
            'method': result['method']
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Detection failed'
        }), 400

@rotation_bp.route('/api/inspect_with_rotation', methods=['POST'])
def inspect_with_rotation():
    '''AOI 檢測 + 旋轉角度'''

    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image provided'}), 400

    # 讀取影像
    image_bytes = file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 執行完整檢測
    aoi_system = AOIWithRotation()
    results = aoi_system.inspect_and_pick(image)

    return jsonify(results)
"""
    print("\n" + "=" * 60)
    print("Flask API 整合範例")
    print("=" * 60)
    print(example_code)


if __name__ == "__main__":
    print("🎯 AOI 系統整合範例\n")

    # 執行示範
    demo_integration()

    # 顯示 API 範例
    flask_api_example()

    print("\n" + "=" * 60)
    print("整合說明")
    print("=" * 60)
    print("""
    如何整合到現有系統：

    1. 將 RotationDetector 類別加入到後端服務
       檔案：aoi-system/backend/app/services/rotation_detector.py

    2. 建立 API 端點
       檔案：aoi-system/backend/app/routes/rotation_detection.py

    3. 前端呼叫 API
       在 aoi-system/frontend/src/services/api.ts 中加入：

       export const detectRotation = async (imageFile: File) => {
         const formData = new FormData();
         formData.append('image', imageFile);

         const response = await fetch('/api/detect_rotation', {
           method: 'POST',
           body: formData
         });

         return response.json();
       };

    4. 更新機械手臂模擬器
       在 RoboticArmSimulator.tsx 中使用旋轉角度資訊
    """)
