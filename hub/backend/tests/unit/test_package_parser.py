"""包解析器单元测试"""
import pytest
import io
import json
import zipfile

from infrastructure.external.package_parser import ZipPackageParser
from domain.exceptions import InvalidPackageException


class TestZipPackageParser:
    """ZIP包解析器测试"""
    
    @pytest.fixture
    def parser(self):
        return ZipPackageParser()
    
    @pytest.mark.asyncio
    async def test_parse_valid_package(self, parser, valid_zip_file):
        """测试解析有效的包"""
        result = await parser.parse(valid_zip_file)
        
        assert result.manifest_version == 1
        assert result.name == "DIP for ITOps"
        assert result.version == "1.0.0"
    
    @pytest.mark.asyncio
    async def test_parse_package_missing_manifest(self, parser, invalid_zip_file):
        """测试解析缺少manifest的包"""
        with pytest.raises(InvalidPackageException) as exc_info:
            await parser.parse(invalid_zip_file)
        
        assert "manifest.json" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_parse_invalid_zip(self, parser):
        """测试解析无效的ZIP文件"""
        invalid_file = io.BytesIO(b"not a zip file")
        
        with pytest.raises(InvalidPackageException) as exc_info:
            await parser.parse(invalid_file)
        
        assert "Invalid ZIP" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_parse_manifest_missing_name(self, parser):
        """测试解析缺少name字段的manifest"""
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            manifest = {"manifest_version": 1, "version": "1.0.0"}  # 缺少name
            zf.writestr("manifest.json", json.dumps(manifest))
        zip_buffer.seek(0)
        
        with pytest.raises(InvalidPackageException) as exc_info:
            await parser.parse(zip_buffer)
        
        assert "name" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_parse_invalid_json(self, parser):
        """测试解析无效的JSON"""
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            zf.writestr("manifest.json", "invalid json {")
        zip_buffer.seek(0)
        
        with pytest.raises(InvalidPackageException) as exc_info:
            await parser.parse(zip_buffer)
        
        assert "Invalid manifest.json" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_parse_nested_manifest(self, parser):
        """测试解析嵌套目录中的manifest"""
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            manifest = {
                "manifest_version": 1,
                "name": "Nested App",
                "version": "2.0.0",
            }
            zf.writestr("my-app/manifest.json", json.dumps(manifest))
        zip_buffer.seek(0)
        
        result = await parser.parse(zip_buffer)
        
        assert result.name == "Nested App"
    
    @pytest.mark.asyncio
    async def test_extract_chart(self, parser, valid_zip_file):
        """测试提取chart"""
        chart_data = await parser.extract_chart(valid_zip_file)
        
        assert chart_data == b"mock-chart-content"
    
    @pytest.mark.asyncio
    async def test_extract_chart_fallback(self, parser):
        """测试提取chart（无chart时返回整个ZIP）"""
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            zf.writestr("manifest.json", '{"name": "test"}')
        zip_buffer.seek(0)
        
        original_content = zip_buffer.getvalue()
        
        chart_data = await parser.extract_chart(zip_buffer)
        
        # 返回整个ZIP内容
        assert chart_data == original_content

