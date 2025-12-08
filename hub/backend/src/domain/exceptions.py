"""领域异常定义"""


class DomainException(Exception):
    """领域异常基类"""
    def __init__(self, message: str, code: str = "DOMAIN_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class AppNotFoundException(DomainException):
    """应用未找到异常"""
    def __init__(self, app_id: int):
        super().__init__(f"App not found: {app_id}", "APP_NOT_FOUND")


class AppAlreadyPublishedException(DomainException):
    """应用已发布异常"""
    def __init__(self, app_id: int):
        super().__init__(f"App already published: {app_id}", "APP_ALREADY_PUBLISHED")


class AppNotPublishedException(DomainException):
    """应用未发布异常"""
    def __init__(self, app_id: int):
        super().__init__(f"App not published: {app_id}", "APP_NOT_PUBLISHED")


class AppCannotBePublishedException(DomainException):
    """应用无法发布异常"""
    def __init__(self, app_id: int, reason: str = ""):
        message = f"App cannot be published: {app_id}"
        if reason:
            message += f", reason: {reason}"
        super().__init__(message, "APP_CANNOT_BE_PUBLISHED")


class InvalidPackageException(DomainException):
    """无效应用包异常"""
    def __init__(self, reason: str):
        super().__init__(f"Invalid package: {reason}", "INVALID_PACKAGE")


class PackageNotFoundException(DomainException):
    """应用包未找到异常"""
    def __init__(self, package_id: int):
        super().__init__(f"Package not found: {package_id}", "PACKAGE_NOT_FOUND")

