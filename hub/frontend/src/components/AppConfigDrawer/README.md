# 组件介绍

这个一个应用配置抽屉 AppConfigDrawer 组件，整体分 3 个部分，基本信息 + 业务知识网络 + 智能体配置，每个部分是一个单独的小组件

## 组件结构

- types.ts 类型声明、定义，枚举定义
- index.tsx 主组件
- BasicConfig.tsx 基本信息配置组件
- OntologyConfig.tsx 业务知识网络配置组件
- AgentConfig.tsx 智能体配置组件
- utils.tsx 工具方法（如果有的话）

# 交互设计

figma 链接，里面对应 3 个部分的细节，基本信息: `https://www.figma.com/design/awdYlPYcJPhGxTgSGCiUwm/%E5%95%86%E5%BA%97?node-id=153-4359&t=AqJW2RaHlbF3kEdn-4`,业务知识网络:`https://www.figma.com/design/awdYlPYcJPhGxTgSGCiUwm/%E5%95%86%E5%BA%97?node-id=128-655&t=AqJW2RaHlbF3kEdn-4`,智能体配置: `https://www.figma.com/design/awdYlPYcJPhGxTgSGCiUwm/%E5%95%86%E5%BA%97?node-id=132-1143&t=AqJW2RaHlbF3kEdn-4`

- 布局为上下布局，抽屉头 + 底部区，底部区为左右布局，菜单栏 + 各菜单配置区域
- 点击菜单项切换右侧显示内容
- 抽屉头显示：应用配置/`应用名称`
- 智能体配置部分， UI 里涉及到 `前往ADP平台查看详细配置` 相关，是一个链接地址，地址为`https://dip.aishu.cn/studio/dataagent/agent-web-space/agent-web-myagents/config?agentId=${agentId}`
- 业务知识网络部分，UI 里涉及到 `前往ADP平台配置数据视图映射` 相关，是一个链接地址，地址为`https://dip.aishu.cn/studio/ontology/ontology-manage/main/overview?id=${ontologyId}`

# 代码实现

- 抽屉收到 props ：appData，open，onClose, ...
- 菜单项默认选中 基本信息，初始加载就获取 基本信息 配置
- 切换时调用接口获取相关配置信息，接口在`/src/apis/dip-hub` 里
- 用 tailwind 完成样式，无法完成的用样式文件
