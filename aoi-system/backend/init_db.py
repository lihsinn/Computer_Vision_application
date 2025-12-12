"""
Database Initialization Script
運行此腳本以建立資料庫表格

使用方法:
    python init_db.py --create   # 建立表格
    python init_db.py --drop     # 刪除表格（危險！）
    python init_db.py --reset    # 重置表格（刪除後重建）
"""

import sys
import argparse
from app.database import init_db, drop_db, engine
from app.models import Base


def create_tables():
    """建立所有資料庫表格"""
    print("🚀 正在建立資料庫表格...")
    Base.metadata.create_all(bind=engine)
    print("✅ 資料庫表格建立成功！")
    print("\n已建立的表格:")
    for table in Base.metadata.sorted_tables:
        print(f"  - {table.name}")


def drop_tables():
    """刪除所有資料庫表格"""
    confirm = input("⚠️  警告：這將刪除所有資料！是否繼續？ (yes/no): ")
    if confirm.lower() == 'yes':
        print("🗑️  正在刪除資料庫表格...")
        Base.metadata.drop_all(bind=engine)
        print("✅ 資料庫表格已刪除！")
    else:
        print("❌ 操作已取消")


def reset_tables():
    """重置所有資料庫表格"""
    confirm = input("⚠️  警告：這將刪除並重建所有表格！是否繼續？ (yes/no): ")
    if confirm.lower() == 'yes':
        print("🔄 正在重置資料庫...")
        Base.metadata.drop_all(bind=engine)
        print("✅ 舊表格已刪除")
        Base.metadata.create_all(bind=engine)
        print("✅ 新表格已建立")
        print("\n已建立的表格:")
        for table in Base.metadata.sorted_tables:
            print(f"  - {table.name}")
    else:
        print("❌ 操作已取消")


def main():
    parser = argparse.ArgumentParser(description='AOI System Database Initialization')
    parser.add_argument('--create', action='store_true', help='建立資料庫表格')
    parser.add_argument('--drop', action='store_true', help='刪除資料庫表格')
    parser.add_argument('--reset', action='store_true', help='重置資料庫表格')

    args = parser.parse_args()

    if args.create:
        create_tables()
    elif args.drop:
        drop_tables()
    elif args.reset:
        reset_tables()
    else:
        print("請指定操作: --create, --drop, 或 --reset")
        parser.print_help()


if __name__ == '__main__':
    main()
