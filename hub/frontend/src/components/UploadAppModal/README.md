# 布局

- 整个弹窗从上到下布局，figma 链接 `https://www.figma.com/design/awdYlPYcJPhGxTgSGCiUwm/%E5%95%86%E5%BA%97?node-id=215-11818&t=AqJW2RaHlbF3kEdn-4`

1. 弹窗头部
2. 上传/拖拽区域
3. 文件展示区域
4. 错误展示区域
5. 操作按钮区域（开始安装应用 + 重新上传）
6. 弹窗底部按钮（确定 + 取消）

# 交互

## 过程

- 初始空白时，只有布局的 1 + 2
- 点击或拖住文件添加后，布局为 1 + 2 + 3 + 5 + 6
- 点击`开始安装应用`按钮，调用接口`postApplications`
- 成功后 3 中文件状态变更为成功
- 成功关闭弹窗，弹窗所在页面顶部出现提示，figma 链接`https://www.figma.com/design/awdYlPYcJPhGxTgSGCiUwm/%E5%95%86%E5%BA%97?node-id=215-10761&t=AqJW2RaHlbF3kEdn-4`
- 失败后 3 中文件状态变更为失败，同时出现布局 4，显示具体错误原因

## 细节

- 文件添加成功后，`开始安装应用`+`重新上传`可用
- 失败后，`开始安装应用`不可用
- 底部`确定`按钮，只有在上传
