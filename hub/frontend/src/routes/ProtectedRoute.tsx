import { Navigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../stores'
import { getAccessToken } from '@/utils/http/token-config'
import { getRouteByPath, isRouteVisibleForRoles } from './routes'
import { SYSTEM_FIXED_NORMAL_USER_ID } from '@/apis/types'

interface ProtectedRouteProps {
  children: React.ReactNode
}

/**
 * 路由守卫组件（组件包装器形式）
 * 保护需要登录才能访问的路由
 *
 * 使用方式：
 * <Route path="/protected" element={
 *   <ProtectedRoute>
 *     <YourComponent />
 *   </ProtectedRoute>
 * } />
 */
export const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
  const { isAuthenticated, userInfo } = useAuthStore()
  const location = useLocation()
  console.log('userInfo', userInfo)

  // // 1) token 校验：无 token 或未登录 -> 登录页
  // const token = getAccessToken()
  // if (!token || !isAuthenticated) {
  //   return <Navigate to="/login" state={{ from: location }} replace />
  // }

  // // 2) 角色校验：无角色 -> 登录失败页
  // const roleIds = new Set(userInfo?.role_ids ?? [])
  // if (roleIds.size === 0) {
  //   return <Navigate to="/login-failed" replace />
  // }

  // // 3) 权限校验：根据当前路由绑定的 requiredRoleIds 判断
  // const pathname = location.pathname
  // // 微应用容器：仅“普通用户”角色可访问
  // if (pathname.startsWith('/application/')) {
  //   if (!roleIds.has(SYSTEM_FIXED_NORMAL_USER_ID)) {
  //     return <Navigate to="/403" replace />
  //   }
  //   return <>{children}</>
  // }

  // const route = getRouteByPath(pathname)
  // if (route && !isRouteVisibleForRoles(route, roleIds)) {
  //   return <Navigate to="/403" replace />
  // }

  return <>{children}</>
}

/**
 * 路由守卫高阶组件（HOC 形式）
 *
 * 使用方式：
 * const ProtectedComponent = withProtectedRoute(YourComponent)
 *
 * 或者在路由配置中：
 * <Route path="/protected" element={<ProtectedComponent />} />
 */
export function withProtectedRoute<P extends object>(
  Component: React.ComponentType<P>
) {
  return function ProtectedComponent(props: P) {
    const { isAuthenticated } = useAuthStore()
    const location = useLocation()

    if (!isAuthenticated) {
      return <Navigate to="/login" state={{ from: location }} replace />
    }

    return <Component {...props} />
  }
}

export default ProtectedRoute
