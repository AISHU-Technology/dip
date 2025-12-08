"""对象映射器"""
from domain.entities import App, AppPackage
from application.dto import AppResponseDto, AppDetailResponseDto, AppPackageResponseDto


class AppMapper:
    """应用映射器"""
    
    @staticmethod
    def to_response_dto(app: App) -> AppResponseDto:
        """将应用实体转换为列表响应DTO"""
        return AppResponseDto(
            id=app.id,
            name=app.name,
            description=app.description,
            cover_base64=app.cover_base64,
            editor=app.editor_id,
            edit_time=app.edit_time,
            publish_status=app.publish_status.value,
            release_app_package_id=app.release_app_package_id,
        )
    
    @staticmethod
    def to_detail_dto(app: App, packages: list[AppPackage]) -> AppDetailResponseDto:
        """将应用实体转换为详情响应DTO"""
        return AppDetailResponseDto(
            id=app.id,
            name=app.name,
            description=app.description,
            cover_base64=app.cover_base64,
            creator=app.creator_id,
            create_time=app.create_time,
            editor=app.editor_id,
            edit_time=app.edit_time,
            publish_status=app.publish_status.value,
            release_app_package_id=app.release_app_package_id,
            app_packages=[AppMapper.package_to_dto(p) for p in packages],
        )
    
    @staticmethod
    def package_to_dto(package: AppPackage) -> AppPackageResponseDto:
        """将应用包实体转换为响应DTO"""
        return AppPackageResponseDto(
            package_id=package.id,
            name=package.name,
            upload_user_id=package.upload_user_id,
            upload_time=package.upload_time,
        )

