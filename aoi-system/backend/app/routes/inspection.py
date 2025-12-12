"""
Inspection Routes - 檢測記錄API
"""

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.database import Session
from app.models import Lot, Inspection, Cell, Defect
import uuid
from decimal import Decimal

bp = Blueprint('inspection', __name__)


@bp.route('/lots', methods=['POST'])
def create_lot():
    """
    建立新批次
    Request Body: { "lot_number": "LOT001", "description": "..." }
    """
    try:
        data = request.get_json()
        lot_number = data.get('lot_number')

        if not lot_number:
            return jsonify({'error': '批號不可為空'}), 400

        db = Session()

        # Check if lot_number already exists
        existing_lot = db.query(Lot).filter_by(lot_number=lot_number).first()
        if existing_lot:
            return jsonify({'error': '批號已存在'}), 409

        # Create new lot
        new_lot = Lot(
            lot_number=lot_number,
            description=data.get('description', ''),
            status='CREATED'
        )

        db.add(new_lot)
        db.commit()
        db.refresh(new_lot)

        return jsonify({
            'message': '批次建立成功',
            'lot': new_lot.to_dict()
        }), 201

    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({'error': f'資料庫錯誤: {str(e)}'}), 500
    finally:
        db.close()


@bp.route('/lots', methods=['GET'])
def get_lots():
    """
    取得所有批次列表
    Query Params: ?status=CREATED (optional)
    """
    try:
        db = Session()
        status = request.args.get('status')

        query = db.query(Lot)
        if status:
            query = query.filter_by(status=status)

        lots = query.order_by(Lot.created_at.desc()).all()

        return jsonify({
            'lots': [lot.to_dict() for lot in lots],
            'total': len(lots)
        }), 200

    except SQLAlchemyError as e:
        return jsonify({'error': f'資料庫錯誤: {str(e)}'}), 500
    finally:
        db.close()


@bp.route('/lots/<lot_id>', methods=['GET'])
def get_lot(lot_id):
    """取得單一批次詳細資訊"""
    try:
        db = Session()
        lot = db.query(Lot).filter_by(id=uuid.UUID(lot_id)).first()

        if not lot:
            return jsonify({'error': '批次不存在'}), 404

        # Get all inspections for this lot
        inspections = db.query(Inspection).filter_by(lot_id=lot.id).all()

        return jsonify({
            'lot': lot.to_dict(),
            'inspections': [insp.to_dict() for insp in inspections],
            'total_inspections': len(inspections)
        }), 200

    except ValueError:
        return jsonify({'error': '無效的批次ID'}), 400
    except SQLAlchemyError as e:
        return jsonify({'error': f'資料庫錯誤: {str(e)}'}), 500
    finally:
        db.close()


@bp.route('/inspections', methods=['POST'])
def create_inspection():
    """
    建立單片檢測記錄
    Request Body: {
        "lot_id": "uuid",
        "serial_number": "001",
        "side": "A",
        "inspection_mode": "OfflineTest",
        "inspection_type": "SingleInsp",
        "image_path": "/path/to/image.jpg",
        "cells": [...],
        "defects": [...]
    }
    """
    try:
        data = request.get_json()
        db = Session()

        # Validate required fields
        required_fields = ['lot_id', 'serial_number', 'side', 'inspection_mode', 'image_path']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必要欄位: {field}'}), 400

        # Check if lot exists
        lot = db.query(Lot).filter_by(id=uuid.UUID(data['lot_id'])).first()
        if not lot:
            return jsonify({'error': '批次不存在'}), 404

        # Extract cells and defects data
        cells_data = data.pop('cells', [])
        defects_data = data.pop('defects', {})  # { cell_number: [defects...] }

        # Calculate statistics
        total_cells = len(cells_data)
        ng_count = sum(1 for cell in cells_data if cell.get('status') == 'NG')
        yield_rate = ((total_cells - ng_count) / total_cells * 100) if total_cells > 0 else 0

        # Create inspection record
        inspection = Inspection(
            lot_id=uuid.UUID(data['lot_id']),
            serial_number=data['serial_number'],
            side=data['side'],
            inspection_mode=data.get('inspection_mode', 'OfflineTest'),
            inspection_type=data.get('inspection_type', 'SingleInsp'),
            image_path=data['image_path'],
            annotated_image_path=data.get('annotated_image_path'),
            running_result=data.get('running_result', 'SUCCESS'),
            judgment_result='NG' if ng_count > 0 else 'PASS',
            yield_rate=Decimal(str(round(yield_rate, 2))),
            ng_count=ng_count,
            total_cells=total_cells,
            positioning_abnormal=data.get('positioning_abnormal', False),
            threshold=data.get('threshold')
        )

        db.add(inspection)
        db.flush()  # Get inspection ID

        # Create cell records
        cell_objects = {}
        for cell_data in cells_data:
            cell = Cell(
                inspection_id=inspection.id,
                cell_number=cell_data['cell_number'],
                position_x=cell_data['position_x'],
                position_y=cell_data['position_y'],
                width=cell_data['width'],
                height=cell_data['height'],
                status=cell_data['status'],
                defect_count=0
            )
            db.add(cell)
            db.flush()
            cell_objects[cell_data['cell_number']] = cell

        # Create defect records
        for cell_number, defects in defects_data.items():
            cell = cell_objects.get(int(cell_number))
            if cell:
                for defect_data in defects:
                    defect = Defect(
                        cell_id=cell.id,
                        defect_type=defect_data.get('defect_type', 'UNKNOWN'),
                        position_x=defect_data['position_x'],
                        position_y=defect_data['position_y'],
                        area=Decimal(str(defect_data['area'])),
                        width=Decimal(str(defect_data.get('width', 0))) if defect_data.get('width') else None,
                        height=Decimal(str(defect_data.get('height', 0))) if defect_data.get('height') else None,
                        bbox_x1=defect_data.get('bbox_x1'),
                        bbox_y1=defect_data.get('bbox_y1'),
                        bbox_x2=defect_data.get('bbox_x2'),
                        bbox_y2=defect_data.get('bbox_y2'),
                        confidence=Decimal(str(defect_data.get('confidence', 0))) if defect_data.get('confidence') else None
                    )
                    db.add(defect)

                # Update cell defect count
                cell.defect_count = len(defects)

        # Update lot status
        lot.status = 'IN_PROGRESS'

        db.commit()
        db.refresh(inspection)

        return jsonify({
            'message': '檢測記錄建立成功',
            'inspection': inspection.to_dict()
        }), 201

    except ValueError as e:
        db.rollback()
        return jsonify({'error': f'資料格式錯誤: {str(e)}'}), 400
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({'error': f'資料庫錯誤: {str(e)}'}), 500
    finally:
        db.close()


@bp.route('/inspections/<inspection_id>', methods=['GET'])
def get_inspection(inspection_id):
    """取得單一檢測記錄詳細資訊"""
    try:
        db = Session()
        inspection = db.query(Inspection).filter_by(id=uuid.UUID(inspection_id)).first()

        if not inspection:
            return jsonify({'error': '檢測記錄不存在'}), 404

        # Get cells
        cells = db.query(Cell).filter_by(inspection_id=inspection.id).all()

        # Get defects for each cell
        cells_with_defects = []
        for cell in cells:
            defects = db.query(Defect).filter_by(cell_id=cell.id).all()
            cell_dict = cell.to_dict()
            cell_dict['defects'] = [defect.to_dict() for defect in defects]
            cells_with_defects.append(cell_dict)

        result = inspection.to_dict()
        result['cells'] = cells_with_defects

        return jsonify(result), 200

    except ValueError:
        return jsonify({'error': '無效的檢測記錄ID'}), 400
    except SQLAlchemyError as e:
        return jsonify({'error': f'資料庫錯誤: {str(e)}'}), 500
    finally:
        db.close()


@bp.route('/inspections', methods=['GET'])
def get_inspections():
    """
    取得檢測記錄列表
    Query Params: ?lot_id=xxx&serial_number=xxx&side=A
    """
    try:
        db = Session()

        query = db.query(Inspection)

        # Apply filters
        if request.args.get('lot_id'):
            query = query.filter_by(lot_id=uuid.UUID(request.args.get('lot_id')))
        if request.args.get('serial_number'):
            query = query.filter_by(serial_number=request.args.get('serial_number'))
        if request.args.get('side'):
            query = query.filter_by(side=request.args.get('side'))

        inspections = query.order_by(Inspection.created_at.desc()).all()

        return jsonify({
            'inspections': [insp.to_dict() for insp in inspections],
            'total': len(inspections)
        }), 200

    except ValueError:
        return jsonify({'error': '無效的參數'}), 400
    except SQLAlchemyError as e:
        return jsonify({'error': f'資料庫錯誤: {str(e)}'}), 500
    finally:
        db.close()


@bp.route('/inspections/<inspection_id>/cells', methods=['GET'])
def get_inspection_cells(inspection_id):
    """取得檢測記錄的所有Cells"""
    try:
        db = Session()

        cells = db.query(Cell).filter_by(inspection_id=uuid.UUID(inspection_id)).all()

        return jsonify({
            'cells': [cell.to_dict() for cell in cells],
            'total': len(cells)
        }), 200

    except ValueError:
        return jsonify({'error': '無效的檢測記錄ID'}), 400
    except SQLAlchemyError as e:
        return jsonify({'error': f'資料庫錯誤: {str(e)}'}), 500
    finally:
        db.close()
