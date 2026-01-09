import type { ReactNode } from 'react'
import type { RouteObject } from 'react-router-dom'

/** 路由配置 */
export interface RouteConfig {
  path?: string
  element?: ReactNode | null
  key?: string
  label?: string
  /** 侧边栏图标资源路径（用于在 Sider 中做填充/渐变等处理） */
  iconUrl?: string
  /** 允许访问该菜单/路由的角色ID（命中任意一个即可）；为空则默认允许 */
  requiredRoleIds?: string[]
  disabled?: boolean
  /** 是否在侧边栏展示 */
  showInSidebar?: boolean
  handle?: RouteObject['handle']
  children?: RouteConfig[]
}
