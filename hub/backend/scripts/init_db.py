"""
数据库初始化脚本

创建 DIP Hub 所需的数据库表。
"""
import pymysql
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库连接配置
DB_HOST = os.getenv('DIP_HUB_DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DIP_HUB_DB_PORT', '3306'))
DB_USER = os.getenv('DIP_HUB_DB_USER', 'root')
DB_PASSWORD = os.getenv('DIP_HUB_DB_PASSWORD', '123456')
DB_NAME = os.getenv('DIP_HUB_DB_NAME', 'dip')

def init_database():
    """初始化数据库和表。"""
    # 首先连接到 MySQL（不指定数据库）
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            # 创建数据库（如果不存在）
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✓ 数据库 '{DB_NAME}' 已创建或已存在")

            # 使用该数据库
            cursor.execute(f"USE `{DB_NAME}`")

            # 创建用户表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `t_user` (
                    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
                    `user_id` CHAR(36) NOT NULL COMMENT '用户ID',
                    `display_name` VARCHAR(255) NOT NULL COMMENT '用户显示名',
                    PRIMARY KEY (`id`),
                    INDEX `idx_user_id` (`user_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表'
            """)
            print("✓ 表 't_user' 已创建")

            # 创建角色表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `t_role` (
                    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
                    `role_id` CHAR(36) NOT NULL COMMENT '角色ID',
                    `role_name` VARCHAR(255) NOT NULL COMMENT '角色名称',
                    PRIMARY KEY (`id`),
                    INDEX `idx_role_id` (`role_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色表'
            """)
            print("✓ 表 't_role' 已创建")

            # 创建用户-角色关系表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `t_user_role` (
                    `user_id` CHAR(36) NOT NULL COMMENT '用户ID',
                    `role_id` CHAR(36) NOT NULL COMMENT '角色ID',
                    PRIMARY KEY (`user_id`, `role_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户-角色关系表'
            """)
            print("✓ 表 't_user_role' 已创建")

            # 创建应用表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `t_application` (
                    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
                    `key` CHAR(32) NOT NULL COMMENT '应用包唯一标识',
                    `name` VARCHAR(128) NOT NULL COMMENT '应用名称',
                    `description` VARCHAR(800) NULL COMMENT '应用描述',
                    `icon` BLOB NULL COMMENT '应用图标',
                    `version` VARCHAR(128) NULL COMMENT '当前上传的版本号',
                    `config` TEXT NULL COMMENT '应用配置',
                    `updated_by` CHAR(36) NOT NULL COMMENT '更新者ID',
                    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                    PRIMARY KEY (`id`),
                    UNIQUE INDEX `idx_key` (`key`),
                    INDEX `idx_updated_by` (`updated_by`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='应用表'
            """)
            print("✓ 表 't_application' 已创建")

        connection.commit()
        print("\n✓ 数据库初始化完成！")

    except Exception as e:
        print(f"\n✗ 数据库初始化失败: {e}")
        connection.rollback()
        raise
    finally:
        connection.close()

if __name__ == '__main__':
    print("开始初始化数据库...")
    print(f"数据库主机: {DB_HOST}:{DB_PORT}")
    print(f"数据库名称: {DB_NAME}")
    print(f"数据库用户: {DB_USER}")
    print("-" * 50)
    init_database()
