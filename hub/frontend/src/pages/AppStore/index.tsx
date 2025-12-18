import { useState, useCallback, memo, useEffect } from 'react'
import { Spin, Button, message } from 'antd'
import GradientContainer from '@/components/GradientContainer'
import AppList from '@/components/AppList'
import Empty from '@/components/Empty'
import { ModeEnum } from '@/components/AppList/types'
import { AppStoreActionEnum } from './types'
import { type ApplicationInfo } from '@/apis/dip-hub'
import SearchInput from '@/components/SearchInput'
import { ReloadOutlined } from '@ant-design/icons'
import IconFont from '@/components/IconFont'
import { useApplicationsService } from '@/hooks/useApplicationsService'
import AppConfigDrawer from '@/components/AppConfigDrawer'

const AppStore = () => {
  const { apps, loading, error, searchValue, handleSearch, handleRefresh } =
    useApplicationsService()
  const [installModalVisible, setInstallModalVisible] = useState(false)
  const [configModalVisible, setConfigModalVisible] = useState(false)
  const [selectedApp, setSelectedApp] = useState<ApplicationInfo | null>(null)
  const [hasLoadedData, setHasLoadedData] = useState(false) // 记录是否已经成功加载过数据（有数据的情况）

  // 当数据加载完成且有数据时，标记为已加载过数据
  useEffect(() => {
    if (!loading && apps.length > 0) {
      setHasLoadedData(true)
    }
  }, [loading, apps.length])

  /** 处理卡片菜单操作 */
  const handleMenuClick = useCallback(
    async (action: string, _app: ApplicationInfo) => {
      try {
        switch (action) {
          case AppStoreActionEnum.Install:
            // TODO: 调用安装接口
            message.success('安装成功')
            handleRefresh()
            break
          case AppStoreActionEnum.Uninstall:
            // TODO: 调用卸载接口
            message.success('卸载成功')
            handleRefresh()
            break
          case AppStoreActionEnum.Config:
            setSelectedApp(_app)
            setConfigModalVisible(true)
            break
          case AppStoreActionEnum.Run:
            // TODO: 运行应用
            break
          case AppStoreActionEnum.Auth:
            // TODO: 跳转授权管理
            break
          default:
            break
        }
      } catch (err) {
        console.error('Failed to handle app action:', err)
        message.error('操作失败')
      }
    },
    [handleRefresh]
  )

  /** 渲染状态内容（loading/error/empty） */
  const renderStateContent = () => {
    if (loading) {
      return <Spin size="large" />
    }

    if (error) {
      return (
        <Empty type="failed" desc="加载失败">
          <Button type="primary" onClick={handleRefresh}>
            重试
          </Button>
        </Empty>
      )
    }

    if (apps.length === 0) {
      if (searchValue) {
        return <Empty type="search" desc="抱歉，没有找到相关内容" />
      }
      return (
        <Empty
          desc="暂无可用应用"
          subDesc="您当前没有任何应用的访问权限。这可能是因为管理员尚未为您分配权限，或者应用尚未部署。"
        >
          <Button
            type="primary"
            icon={<IconFont type="icon-dip-upload" />}
            onClick={() => {
              setInstallModalVisible(true)
            }}
          >
            安装应用
          </Button>
        </Empty>
      )
    }

    return null
  }

  /** 渲染内容区域 */
  const renderContent = () => {
    const stateContent = renderStateContent()

    if (stateContent) {
      return (
        <div className="absolute inset-0 flex items-center justify-center">
          {stateContent}
        </div>
      )
    }

    return (
      <AppList
        mode={ModeEnum.AppStore}
        apps={apps}
        onMenuClick={handleMenuClick}
      />
    )
  }

  return (
    <GradientContainer className="h-full p-6 flex flex-col">
      <div className="flex justify-between mb-6 flex-shrink-0 z-20">
        <div className="flex flex-col gap-y-3">
          <span className="text-base font-bold">应用商店</span>
          <span className="text-sm">管理企业应用市场，安装或卸载应用</span>
        </div>
        {hasLoadedData && (
          <div className="flex items-center gap-x-2">
            <SearchInput onSearch={handleSearch} placeholder="搜索应用" />
            <Button
              type="text"
              icon={<ReloadOutlined />}
              onClick={handleRefresh}
            />
            <Button
              type="primary"
              icon={<IconFont type="icon-dip-upload" />}
              onClick={() => setInstallModalVisible(true)}
            >
              安装应用
            </Button>
          </div>
        )}
      </div>
      {renderContent()}
      <AppConfigDrawer
        appData={selectedApp ?? undefined}
        open={configModalVisible}
        onClose={() => setConfigModalVisible(false)}
      />
    </GradientContainer>
  )
}

export default memo(AppStore)
