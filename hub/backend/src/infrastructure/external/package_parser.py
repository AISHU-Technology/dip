"""应用包解析器"""
import json
import zipfile
import io
from typing import BinaryIO

from application.ports import IPackageParser, PackageManifest
from domain.exceptions import InvalidPackageException


class ZipPackageParser(IPackageParser):
    """ZIP包解析器实现"""
    
    MANIFEST_FILE = "manifest.json"
    
    async def parse(self, file: BinaryIO) -> PackageManifest:
        """
        解析ZIP包并验证，返回manifest信息
        
        验证规则：
        - 必须是有效的ZIP文件
        - 必须包含manifest.json
        - manifest.json必须包含必要字段
        """
        try:
            # 读取文件内容到内存
            file_content = file.read()
            file.seek(0)
            
            with zipfile.ZipFile(io.BytesIO(file_content)) as zf:
                # 检查是否包含manifest.json
                file_list = zf.namelist()
                manifest_path = None
                
                for name in file_list:
                    if name.endswith(self.MANIFEST_FILE):
                        manifest_path = name
                        break
                
                if manifest_path is None:
                    raise InvalidPackageException("Package must contain manifest.json")
                
                # 读取并解析manifest.json
                with zf.open(manifest_path) as mf:
                    manifest_content = mf.read().decode("utf-8")
                    manifest_data = json.loads(manifest_content)
                
                # 验证必要字段
                if "name" not in manifest_data:
                    raise InvalidPackageException("manifest.json must contain 'name' field")
                
                return PackageManifest(
                    manifest_version=manifest_data.get("manifest_version", 1),
                    name=manifest_data["name"],
                    version=manifest_data.get("version", "1.0.0"),
                )
                
        except zipfile.BadZipFile:
            raise InvalidPackageException("Invalid ZIP file")
        except json.JSONDecodeError:
            raise InvalidPackageException("Invalid manifest.json format")
        except InvalidPackageException:
            raise
        except Exception as e:
            raise InvalidPackageException(f"Failed to parse package: {str(e)}")
    
    async def extract_chart(self, file: BinaryIO) -> bytes:
        """从ZIP包中提取chart"""
        try:
            file_content = file.read()
            file.seek(0)
            
            with zipfile.ZipFile(io.BytesIO(file_content)) as zf:
                # 查找client/package.tgz或service/package.tgz
                chart_paths = [
                    "client/package.tgz",
                    "service/package.tgz",
                ]
                
                for name in zf.namelist():
                    for chart_path in chart_paths:
                        if name.endswith(chart_path):
                            with zf.open(name) as cf:
                                return cf.read()
                
                # 如果没有找到chart，返回整个ZIP内容
                return file_content
                
        except Exception as e:
            raise InvalidPackageException(f"Failed to extract chart: {str(e)}")

