import React, { useMemo, useState } from 'react'
import { Card, Dropdown, Avatar } from 'antd'
import type { MenuProps } from 'antd'
import { formatTimeMinute } from '@/utils/handle-function/FormatTime'
import type { AppInfo } from '@/apis/app-development'
import { ModeEnum } from './types'
import { cardHeight, getAppCardMenuItems } from './utils'
import IconFont from '../IconFont'
import classNames from 'classnames'

interface AppCardProps {
  app: AppInfo
  mode: ModeEnum.MyApp | ModeEnum.AppStore
  onMenuClick?: (key: string, app: AppInfo) => void
}

const AppCard: React.FC<AppCardProps> = ({ app, mode, onMenuClick }) => {
  const [menuOpen, setMenuOpen] = useState(false)

  const menuItems = useMemo(() => {
    return getAppCardMenuItems(mode, app) as MenuProps['items']
  }, [mode, app])

  const handleMenuClick: MenuProps['onClick'] = ({ key }) => {
    onMenuClick?.(key as string, app)
  }

  const updateTime = app.updateTime ? formatTimeMinute(app.updateTime) : ''
  const userName = app.createdByName || app.createdBy || ''

  return (
    <Card
      className="group rounded-xl border border-[var(--dip-border-color)] transition-all w-full"
      style={{ height: cardHeight }}
      styles={{
        body: {
          height: '100%',
          padding: '16px 16px 12px 16px',
          display: 'flex',
          flexDirection: 'column',
        },
      }}
    >
      <div className="flex gap-4 mb-2 flex-shrink-0">
        {/* 应用图标 */}
        <div className="w-16 h-16 flex-shrink-0 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
          {app.appIcon ? (
            <img
              src={app.appIcon}
              alt={app.appName}
              className="w-full h-full rounded-full object-cover"
            />
          ) : (
            <span className="text-white text-base font-medium">
              {app.appName?.charAt(0)}
            </span>
          )}
        </div>
        {/* 名称 + 版本号 + 描述 */}
        <div className="flex-1 min-w-0">
          <div className="flex flex-col gap-2">
            <h3 className="text-sm font-medium mr-px truncate text-black">
              {app.appName}
            </h3>
            <div className="w-fit rounded text-xs px-2 py-0.5 border border-[var(--dip-border-color-base)]">
              {app.version}
            </div>
            <p className="text-xs line-clamp-2">
              {app.appDescription || '[暂无描述]'}
            </p>
          </div>
        </div>
      </div>

      <div className="flex flex-col justify-end flex-1 h-0">
        <div className="mb-2 h-px bg-[var(--dip-line-color)]" />
        <div className="flex items-center justify-between">
          {/* 更新信息 */}
          <div className="flex items-center text-xs text-[var(--dip-text-color-45)]">
            <Avatar size={24} className="flex-shrink-0 mr-2">
              {userName.charAt(0)}
            </Avatar>
            <span className="truncate max-w-20 mr-4">{userName}</span>
            <span>更新：{updateTime}</span>
          </div>
          {/* 更多操作 */}
          {menuItems && menuItems.length > 0 && (
            <Dropdown
              menu={{ items: menuItems, onClick: handleMenuClick }}
              trigger={['click']}
              placement="bottomRight"
              onOpenChange={(open) => {
                setMenuOpen(open)
              }}
            >
              <span
                onClick={(e) => {
                  e.stopPropagation()
                }}
                className={classNames(
                  'w-6 h-6 flex items-center justify-center cursor-pointer text-[var(--dip-text-color-45)] hover:text-[var(--dip-text-color-85)] transition-opacity',
                  menuOpen
                    ? 'opacity-100 visible'
                    : 'opacity-0 invisible group-hover:opacity-100 group-hover:visible'
                )}
              >
                <IconFont type="icon-dip-gengduo" />
              </span>
            </Dropdown>
          )}
        </div>
      </div>
    </Card>
  )
}

export default AppCard
