import type { RouteConfig } from './types'
import { routeConfigs } from './routes'

/**
 * 根据路径获取路由配置
 * 支持动态路由匹配（如 /application/:appKey/*）
 */
export const getRouteByPath = (path: string): RouteConfig | undefined => {
  // 移除前导斜杠
  const normalizedPath = path.startsWith('/') ? path.slice(1) : path

  // 先尝试精确匹配
  const exactMatch = routeConfigs.find((route) => route.path === normalizedPath)
  if (exactMatch) return exactMatch

  // 匹配动态路由 /application/:appKey/*
  const appRouteMatch = normalizedPath.match(/^application\/([^/]+)/)
  if (appRouteMatch) {
    // 返回一个虚拟的路由配置，用于微应用
    return {
      path: normalizedPath,
      key: `micro-app-${appRouteMatch[1]}`,
      label: appRouteMatch[1], // 默认使用 appKey，后续可以从微应用列表获取
      showInSidebar: false,
    }
  }

  return undefined
}

/**
 * 根据 key 获取路由配置
 */
export const getRouteByKey = (key: string): RouteConfig | undefined => {
  return routeConfigs.find((route) => route.key === key)
}

/**
 * 判断路由是否对用户可见
 */
export const isRouteVisibleForRoles = (
  route: RouteConfig,
  roleIds: Set<string>
): boolean => {
  const required = route.requiredRoleIds
  if (!required || required.length === 0) return true
  // 用户未携带任何角色时：默认不放行；首页会重定向到 /login-failed
  if (roleIds.size === 0) return false
  return required.some((id) => roleIds.has(id))
}

export const getFirstVisibleSidebarRoute = (
  roleIds: Set<string>
): RouteConfig | undefined => {
  return routeConfigs.find(
    (r) => r.showInSidebar && r.key && isRouteVisibleForRoles(r, roleIds)
  )
}
