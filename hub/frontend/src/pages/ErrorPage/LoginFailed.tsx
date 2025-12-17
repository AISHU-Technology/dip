import { Button, Result } from 'antd'

const LoginFailed = () => {
  const handleReturnLoginPage = () => {
    window.location.replace('/login')
  }

  return (
    <div className="w-full h-full flex items-center justify-center">
      <Result
        status="warning"
        subTitle="您当前使用的账号未绑定任何角色，无法登录"
        extra={
          <Button type="primary" onClick={handleReturnLoginPage}>
            返回登录页面
          </Button>
        }
      />
    </div>
  )
}

export default LoginFailed
