"""API 路由定义"""
from typing import Optional

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Query

from application.dto import (
    CreateAppDto,
    UpdateAppDto,
    AppResponseDto,
    AppDetailResponseDto,
    CreateAppResponseDto,
    SuccessResponseDto,
)
from domain.exceptions import (
    AppNotFoundException,
    AppCannotBePublishedException,
    AppNotPublishedException,
    InvalidPackageException,
)
from infrastructure.api.dependencies import AppServiceDep, CurrentUserDep

router = APIRouter(prefix="/apps", tags=["apps"])


@router.post(
    "/",
    response_model=CreateAppResponseDto,
    status_code=status.HTTP_201_CREATED,
    summary="创建应用",
)
async def create_app(
    dto: CreateAppDto,
    app_service: AppServiceDep,
    user_id: CurrentUserDep,
):
    """
    创建应用
    
    - 创建后 editor = creator
    - publish_status = 0 (未发布)
    - 开发模式不可修改，目前只支持上传模式
    """
    return await app_service.create_app(dto, user_id)


@router.post(
    "/{app_id}/packages/upload",
    response_model=CreateAppResponseDto,
    status_code=status.HTTP_201_CREATED,
    summary="上传应用包",
)
async def upload_package(
    app_id: int,
    app_service: AppServiceDep,
    user_id: CurrentUserDep,
    package: UploadFile = File(..., description="ZIP应用安装包"),
):
    """
    上传应用包
    
    - ZIP必须包含manifest.json
    - 更新publish_status = 2 (未发布更新)
    """
    try:
        return await app_service.upload_package(app_id, package.file, user_id)
    except AppNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="App not found")
    except InvalidPackageException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.message))


@router.put(
    "/{app_id}",
    response_model=SuccessResponseDto,
    summary="编辑应用",
)
async def update_app(
    app_id: int,
    dto: UpdateAppDto,
    app_service: AppServiceDep,
    user_id: CurrentUserDep,
):
    """
    编辑应用（名称/描述/封面）
    
    - 只能修改名称/描述/封面
    - 修改后更新editorId和editTime
    """
    try:
        return await app_service.update_app(app_id, dto, user_id)
    except AppNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="App not found")


@router.get(
    "/",
    response_model=list[AppResponseDto],
    summary="浏览应用列表",
)
async def list_apps(
    app_service: AppServiceDep,
    publish_status: Optional[int] = Query(None, description="发布状态过滤"),
):
    """
    浏览应用列表
    
    - 后端默认按edit_time DESC排序
    - 可根据publish_status过滤
    """
    return await app_service.list_apps(publish_status)


@router.get(
    "/{app_id}",
    response_model=AppDetailResponseDto,
    summary="查看应用详情",
)
async def get_app_detail(
    app_id: int,
    app_service: AppServiceDep,
):
    """
    查看应用详情
    
    包括：
    - 应用元数据
    - 最近10个版本的应用安装包
    """
    try:
        return await app_service.get_app_detail(app_id)
    except AppNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="App not found")


@router.post(
    "/{app_id}/publish",
    response_model=SuccessResponseDto,
    summary="发布应用",
)
async def publish_app(
    app_id: int,
    app_service: AppServiceDep,
    user_id: CurrentUserDep,
):
    """
    发布应用
    
    - 只有状态为未发布或未发布更新可发布
    - 发布成功后publish_status = 1
    """
    try:
        return await app_service.publish_app(app_id, user_id)
    except AppNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="App not found")
    except AppCannotBePublishedException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.post(
    "/{app_id}/unpublish",
    response_model=SuccessResponseDto,
    summary="撤销发布",
)
async def unpublish_app(
    app_id: int,
    app_service: AppServiceDep,
    user_id: CurrentUserDep,
):
    """
    撤销发布
    
    - 只能撤销已发布状态应用
    - 不影响已安装的应用
    """
    try:
        return await app_service.unpublish_app(app_id, user_id)
    except AppNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="App not found")
    except AppNotPublishedException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="App is not published")


@router.delete(
    "/{app_id}",
    response_model=SuccessResponseDto,
    summary="删除应用",
)
async def delete_app(
    app_id: int,
    app_service: AppServiceDep,
    user_id: CurrentUserDep,
):
    """
    删除应用
    
    - 删除后标记is_deleted = 1
    - 不影响已安装应用
    """
    try:
        return await app_service.delete_app(app_id, user_id)
    except AppNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="App not found")

