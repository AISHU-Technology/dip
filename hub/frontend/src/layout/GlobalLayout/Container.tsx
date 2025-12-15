import { useState } from 'react'
import type { ReactNode } from 'react'
import { useMatches } from 'react-router-dom'
import { Layout } from 'antd'
import Sidebar from '../../components/Sidebar'
import Header from '../../components/Header'

const { Content } = Layout

interface LayoutConfig {
  hasSider?: boolean
  hasHeader?: boolean
}

interface RouteHandle {
  layout?: LayoutConfig
}

interface ContainerProps {
  children: ReactNode
}

const Container = ({ children }: ContainerProps) => {
  const [collapsed, setCollapsed] = useState(false)
  const matches = useMatches()

  // 只使用最后一个匹配的路由（当前路由）的布局配置
  // 如果当前路由没有设置 handle.layout，则默认都是 false
  const currentMatch = matches[matches.length - 1]
  const layoutConfig = (currentMatch?.handle as RouteHandle | undefined)?.layout

  // 默认值：如果当前路由没有设置，则默认都是 false
  const { hasSider = false, hasHeader = false } = layoutConfig || {}

  const headerHeight = 52

  return (
    <Layout className="overflow-hidden">
      {hasHeader && <Header />}
      <Layout>
        {hasSider && (
          <Sidebar
            collapsed={collapsed}
            onCollapse={setCollapsed}
            topOffset={hasHeader ? headerHeight : 0}
          />
        )}
        <Layout
          className="transition-all duration-200 flex"
          style={{
            height: hasHeader ? `calc(100vh - ${headerHeight}px)` : '100vh',
          }}
        >
          <Content className="relative min-w-[1040px] m-0 flex-1">
            {children}
          </Content>
        </Layout>
      </Layout>
    </Layout>
  )
}

export default Container
