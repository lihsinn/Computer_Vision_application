# AOI System Database Design

## Database: PostgreSQL

### 📊 Entity Relationship Overview

```
Lots (批次)
  ↓ 1:N
Inspections (檢測記錄)
  ↓ 1:N
Cells (Cell資料)
  ↓ 1:N
Defects (瑕疵記錄)
  ↓ 1:N
ManualReviews (人工覆判)
```

---

## 表格結構設計

### 1. lots (批次表)

| 欄位名 | 類型 | 約束 | 說明 |
|--------|------|------|------|
| id | UUID | PK | 主鍵 |
| lot_number | VARCHAR(100) | UNIQUE, NOT NULL | 批號（LotNum） |
| description | TEXT | NULL | 批次描述 |
| status | VARCHAR(20) | NOT NULL | 狀態：CREATED, IN_PROGRESS, COMPLETED |
| created_at | TIMESTAMP | NOT NULL | 建立時間 |
| updated_at | TIMESTAMP | NOT NULL | 更新時間 |

**索引**：
- `idx_lot_number` ON `lot_number`
- `idx_status` ON `status`

---

### 2. inspections (檢測記錄表)

| 欄位名 | 類型 | 約束 | 說明 |
|--------|------|------|------|
| id | UUID | PK | 主鍵 |
| lot_id | UUID | FK → lots.id | 所屬批次 |
| serial_number | VARCHAR(100) | NOT NULL | 序號 |
| side | VARCHAR(1) | NOT NULL | A面/B面 |
| inspection_mode | VARCHAR(20) | NOT NULL | Run/OfflineTest |
| inspection_type | VARCHAR(20) | NOT NULL | SingleInsp/BatchInsp |
| image_path | VARCHAR(500) | NOT NULL | 原始影像路徑 |
| annotated_image_path | VARCHAR(500) | NULL | 標註後影像路徑 |
| running_result | VARCHAR(50) | NOT NULL | 運行結果：SUCCESS, FAILED |
| judgment_result | VARCHAR(10) | NOT NULL | 判定結果：PASS, NG |
| yield_rate | DECIMAL(5,2) | NOT NULL | 良率(%) |
| ng_count | INTEGER | NOT NULL | NG顆數 |
| total_cells | INTEGER | NOT NULL | 總Cell數 |
| positioning_abnormal | BOOLEAN | DEFAULT FALSE | 定位異常 |
| threshold | INTEGER | NULL | 檢測閾值參數 |
| created_at | TIMESTAMP | NOT NULL | 檢測時間 |
| updated_at | TIMESTAMP | NOT NULL | 更新時間 |

**索引**：
- `idx_lot_id` ON `lot_id`
- `idx_serial_number` ON `serial_number`
- `idx_judgment_result` ON `judgment_result`

**外鍵**：
- `lot_id` REFERENCES `lots(id)` ON DELETE CASCADE

---

### 3. cells (Cell資料表)

| 欄位名 | 類型 | 約束 | 說明 |
|--------|------|------|------|
| id | UUID | PK | 主鍵 |
| inspection_id | UUID | FK → inspections.id | 所屬檢測記錄 |
| cell_number | INTEGER | NOT NULL | Cell編號（1, 2, 3...） |
| position_x | INTEGER | NOT NULL | X座標（像素） |
| position_y | INTEGER | NOT NULL | Y座標（像素） |
| width | INTEGER | NOT NULL | 寬度（像素） |
| height | INTEGER | NOT NULL | 高度（像素） |
| status | VARCHAR(10) | NOT NULL | PASS/NG |
| defect_count | INTEGER | DEFAULT 0 | 瑕疵數量 |
| created_at | TIMESTAMP | NOT NULL | 建立時間 |

**索引**：
- `idx_inspection_id` ON `inspection_id`
- `idx_status` ON `status`

**外鍵**：
- `inspection_id` REFERENCES `inspections(id)` ON DELETE CASCADE

---

### 4. defects (瑕疵記錄表)

| 欄位名 | 類型 | 約束 | 說明 |
|--------|------|------|------|
| id | UUID | PK | 主鍵 |
| cell_id | UUID | FK → cells.id | 所屬Cell |
| defect_type | VARCHAR(50) | NOT NULL | 瑕疵類型 |
| position_x | INTEGER | NOT NULL | X座標（像素） |
| position_y | INTEGER | NOT NULL | Y座標（像素） |
| area | DECIMAL(10,2) | NOT NULL | 面積（像素²） |
| width | DECIMAL(10,2) | NULL | 寬度（像素） |
| height | DECIMAL(10,2) | NULL | 高度（像素） |
| bbox_x1 | INTEGER | NULL | 邊界框左上X |
| bbox_y1 | INTEGER | NULL | 邊界框左上Y |
| bbox_x2 | INTEGER | NULL | 邊界框右下X |
| bbox_y2 | INTEGER | NULL | 邊界框右下Y |
| confidence | DECIMAL(5,2) | NULL | 置信度(%) |
| created_at | TIMESTAMP | NOT NULL | 檢測時間 |

**索引**：
- `idx_cell_id` ON `cell_id`
- `idx_defect_type` ON `defect_type`

**外鍵**：
- `cell_id` REFERENCES `cells(id)` ON DELETE CASCADE

---

### 5. manual_reviews (人工覆判表)

| 欄位名 | 類型 | 約束 | 說明 |
|--------|------|------|------|
| id | UUID | PK | 主鍵 |
| cell_id | UUID | FK → cells.id | 所屬Cell |
| original_status | VARCHAR(10) | NOT NULL | 原始狀態 |
| reviewed_status | VARCHAR(10) | NOT NULL | 覆判後狀態 |
| reviewer | VARCHAR(100) | NULL | 覆判人員 |
| review_mode | VARCHAR(20) | NOT NULL | 覆判模式：MULTI/SINGLE |
| notes | TEXT | NULL | 備註 |
| reviewed_at | TIMESTAMP | NOT NULL | 覆判時間 |

**索引**：
- `idx_cell_id` ON `cell_id`
- `idx_reviewed_status` ON `reviewed_status`

**外鍵**：
- `cell_id` REFERENCES `cells(id)` ON DELETE CASCADE

---

### 6. merged_inspections (AB面合併記錄表)

| 欄位名 | 類型 | 約束 | 說明 |
|--------|------|------|------|
| id | UUID | PK | 主鍵 |
| lot_id | UUID | FK → lots.id | 所屬批次 |
| serial_number | VARCHAR(100) | NOT NULL | 序號 |
| side_a_inspection_id | UUID | FK → inspections.id | A面檢測ID |
| side_b_inspection_id | UUID | FK → inspections.id | B面檢測ID |
| merged_judgment | VARCHAR(10) | NOT NULL | 合併判定：PASS/NG |
| merged_yield_rate | DECIMAL(5,2) | NOT NULL | 合併良率(%) |
| merged_ng_count | INTEGER | NOT NULL | 合併NG顆數 |
| created_at | TIMESTAMP | NOT NULL | 合併時間 |

**索引**：
- `idx_lot_id` ON `lot_id`
- `idx_serial_number` ON `serial_number`

**外鍵**：
- `lot_id` REFERENCES `lots(id)` ON DELETE CASCADE
- `side_a_inspection_id` REFERENCES `inspections(id)` ON DELETE CASCADE
- `side_b_inspection_id` REFERENCES `inspections(id)` ON DELETE CASCADE

---

### 7. marking_card_params (瑕疵標註卡參數表)

| 欄位名 | 類型 | 約束 | 說明 |
|--------|------|------|------|
| id | UUID | PK | 主鍵 |
| lot_id | UUID | FK → lots.id | 所屬批次 |
| name | VARCHAR(100) | NOT NULL | 參數名稱 |
| grid_rows | INTEGER | NOT NULL | 網格行數 |
| grid_cols | INTEGER | NOT NULL | 網格列數 |
| cell_width | INTEGER | NOT NULL | Cell寬度（像素） |
| cell_height | INTEGER | NOT NULL | Cell高度（像素） |
| offset_x | INTEGER | DEFAULT 0 | X偏移量 |
| offset_y | INTEGER | DEFAULT 0 | Y偏移量 |
| output_format | VARCHAR(20) | NOT NULL | 輸出格式：IMAGE/WORD/PDF |
| is_active | BOOLEAN | DEFAULT TRUE | 是否啟用 |
| created_at | TIMESTAMP | NOT NULL | 建立時間 |
| updated_at | TIMESTAMP | NOT NULL | 更新時間 |

**索引**：
- `idx_lot_id` ON `lot_id`

**外鍵**：
- `lot_id` REFERENCES `lots(id)` ON DELETE CASCADE

---

## 資料流程範例

### 單片檢測流程：
```
1. 建立批次 → INSERT INTO lots
2. 上傳影像 → 儲存到檔案系統
3. 執行檢測 → INSERT INTO inspections
4. 識別Cells → INSERT INTO cells (批量)
5. 檢測瑕疵 → INSERT INTO defects (批量)
6. 計算良率 → UPDATE inspections SET yield_rate, ng_count
```

### AB面合併流程：
```
1. A面檢測完成 → inspection (side='A')
2. B面檢測完成 → inspection (side='B')
3. 自動觸發合併 → INSERT INTO merged_inspections
4. 更新批次狀態 → UPDATE lots SET status='COMPLETED'
```

---

## 查詢範例

### 查詢某批次的所有檢測結果：
```sql
SELECT
    i.serial_number,
    i.side,
    i.judgment_result,
    i.yield_rate,
    i.ng_count,
    i.positioning_abnormal
FROM inspections i
WHERE i.lot_id = 'xxx-xxx-xxx'
ORDER BY i.serial_number, i.side;
```

### 統計多片瑕疵分類：
```sql
SELECT
    d.defect_type,
    COUNT(*) as defect_count,
    COUNT(DISTINCT c.inspection_id) as affected_chips
FROM defects d
JOIN cells c ON d.cell_id = c.id
JOIN inspections i ON c.inspection_id = i.id
WHERE i.lot_id = 'xxx-xxx-xxx'
GROUP BY d.defect_type
ORDER BY defect_count DESC;
```

### 計算批次整體良率：
```sql
SELECT
    l.lot_number,
    ROUND(AVG(i.yield_rate), 2) as avg_yield_rate,
    SUM(i.ng_count) as total_ng_count,
    COUNT(*) as total_inspections
FROM lots l
JOIN inspections i ON l.id = i.lot_id
WHERE l.id = 'xxx-xxx-xxx'
GROUP BY l.lot_number;
```

---

## 效能優化建議

1. **索引優化**：在高頻查詢欄位上建立索引
2. **分區表**：按時間分區 `inspections` 表（按月/季度）
3. **快取策略**：使用 Redis 快取批次狀態和統計資料
4. **批量插入**：使用 `COPY` 或批量 `INSERT` 提高效能
5. **歸檔策略**：定期歸檔舊資料到歷史表

---

## 資料完整性約束

1. **級聯刪除**：刪除批次時自動刪除所有相關檢測記錄
2. **檢查約束**：
   - `side IN ('A', 'B')`
   - `judgment_result IN ('PASS', 'NG')`
   - `status IN ('PASS', 'NG')`
   - `yield_rate BETWEEN 0 AND 100`
3. **唯一性約束**：
   - 同一批次下，同一序號的同一面只能有一條檢測記錄
   - `UNIQUE (lot_id, serial_number, side)`

---

## 擴展性設計

- **JSON欄位**：可在 `inspections` 表新增 `metadata JSONB` 欄位儲存額外參數
- **稽核日誌**：可新增 `audit_logs` 表記錄所有資料變更
- **使用者系統**：可新增 `users` 表支援多使用者權限管理
