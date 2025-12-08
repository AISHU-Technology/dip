"""Proton 服务适配器"""
import uuid
from dataclasses import dataclass

from application.ports import IProtonService, ProtonUploadResult


@dataclass
class ProtonService(IProtonService):
    """Proton服务实现（Mock实现）"""
    
    base_url: str = "http://localhost:8080"
    
    async def upload_package(self, chart_data: bytes, image_data: bytes) -> ProtonUploadResult:
        """
        上传应用包到Proton
        
        Mock实现：返回模拟的chart_code和image_code
        实际实现需要调用Proton API
        """
        # Mock: 生成唯一的code
        chart_code = f"chart-{uuid.uuid4().hex[:12]}"
        image_code = f"image-{uuid.uuid4().hex[:12]}"
        
        return ProtonUploadResult(
            chart_code=chart_code,
            image_code=image_code,
        )

