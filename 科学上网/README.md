## 安装 X-ui 面板
### 申请 SSL 证书
### 下面环境的安装方式，大家根据自己的系统选择命令安装就好了。

### centos命令：
`firewall-cmd --state       			   # 查看防火墙状态`
`systemctl stop firewalld.service       # 停止防火墙`
`systemctl disable firewalld.service    # 禁止防火墙开机自启`


### 更新及安装组件

`apt update -y          # Debian/Ubuntu 命令`
`apt install -y curl    #Debian/Ubuntu 命令`
`apt install -y socat    #Debian/Ubuntu 命令`

`yum update -y          #CentOS 命令`
`yum install -y curl    #CentOS 命令`
`yum install -y socat    #CentOS 命令`


### 安装 Acme 脚本

`curl https://get.acme.sh | sh`

### 80 端口空闲的证书申请方式
### 自行更换代码中的域名、邮箱为你解析的域名及邮箱

`~/.acme.sh/acme.sh --register-account -m oxmosama@qq.com`
`~/.acme.sh/acme.sh  --issue -d ui.oxmo.cn   --standalone`


### 安装证书到指定文件夹
### 自行更换代码中的域名为你解析的域名

`~/.acme.sh/acme.sh --installcert -d ui.oxmo.cn --key-file /root/private.key --fullchain-file /root/cert.crt`


### 安装 & 升级 X-ui 面板
### 安装及升级的一键代码

`bash <(curl -Ls https://raw.githubusercontent.com/sprov065/x-ui/master/install.sh)`

