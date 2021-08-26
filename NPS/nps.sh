#!/usr/bin/env bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

set -o errexit
set -o pipefail
set -o nounset
# set -o xtrace

# 变量区开始 #
nps_dir=
host=
port=
nps_path=
password=

github=0
nps_version="0.25.2"
user="$(id -un 2>/dev/null || true)"
default_nps_dir="$(eval echo ~$user)/nps"
default_port="80"

qiniu_url_prefix="http://static.xinshangshangxin.com/github"
github_url_prefix="https://github.com"
# 变量区结束 #

# 预定义开始 #
red='\033[0;31m'
green='\033[0;32m'
yellow='\033[0;33m'
plain='\033[0m'

user="$(id -un 2>/dev/null || true)"
sh_c='sh -c'
sed=
# 预定义结束 #

command_exists() {
  command -v "$@" >/dev/null 2>&1
}

set_sh() {
  if [ "$user" != 'root' ]; then
    if command_exists sudo; then
      sh_c='sudo -E sh -c'
    elif command_exists su; then
      sh_c='su -c'
    else
      cat >&2 <<-'EOF'
			Error: this installer needs the ability to run commands as root.
			We are unable to find either "sudo" or "su" available to make this happen.
EOF
      exit 1
    fi
  fi
}

set_sed_command() {
  if command_exists gsed; then
    sed="gsed"
  elif command_exists sed; then
    sed="sed"
  else
    echo "no sed or gsed found"
    exit 1
  fi
}

help() {
  echo "Usage:"
  echo "  bash nps.sh --host nps.demo.com --port 23456 --password XXXXX"
  echo ""
  echo "Options:"
  echo "  --host=             web管理界面域名"
  echo "  --port=             web管理界面端口"
  echo "  --password=         web管理界面密码"
  echo "  -d, --dir=          nps安装路径(默认为 ~/nps/)"
  echo "  -v, --version=      nps版本(默认为 ${nps_version})"
  echo "  -g, --github        从github下载(默认为七牛下载)"
  exit 0
}

parse_args() {
  # parse the arguments.
  COUNTER=0
  ARGS=("$@")
  SKIP_NEXT=0
  while [ $COUNTER -lt $# ]; do
    arg=${ARGS[$COUNTER]}
    let COUNTER=COUNTER+1
    nextArg=${ARGS[$COUNTER]:-}

    if [[ $SKIP_NEXT -eq 1 ]]; then
      SKIP_NEXT=0
      continue
    fi

    argKey=""
    argVal=""
    if [[ "$arg" =~ ^\- ]]; then
      # if the format is: -key=value
      if [[ "$arg" =~ \= ]]; then
        argVal=$(echo "$arg" | cut -d'=' -f2)
        argKey=$(echo "$arg" | cut -d'=' -f1)
        SKIP_NEXT=0

      # if the format is: -key value
      elif [[ ! "$nextArg" =~ ^\- ]]; then
        argKey="$arg"
        argVal="$nextArg"
        SKIP_NEXT=1

      # if the format is: -key (a boolean flag)
      elif [[ "$nextArg" =~ ^\- ]] || [[ -z "$nextArg" ]]; then
        argKey="$arg"
        argVal=""
        SKIP_NEXT=0
      fi
    # if the format has not flag, just a value.
    else
      argKey=""
      argVal="$arg"
      SKIP_NEXT=0
    fi

    case "${argKey}" in
    -d | --dir)
      nps_dir="${argVal}"
      ;;
    -v | --version)
      nps_version="${argVal}"
      ;;
    --host)
      host="${argVal}"
      ;;
    --password)
      password="${argVal}"
      ;;
    --port)
      port="${argVal}"
      ;;
    -g | --github)
      github=1
      ;;
    -h | --help)
      help
      exit 0
      ;;
    *)
      echo "${argKey} not support"
      ;;
    esac
  done
}

parse_host() {
  [ -n "${host}" ] && return

  read -e -p "web管理界面host: " host

  parse_host
}

parse_port() {
  [ -n "${port}" ] && return

  read -e -p "绑定端口(默认: ${default_port}): " port

  [ -z "${port}" ] && port=${default_port}

  parse_port
}

parse_password() {
  [ -n "${password}" ] && return

  read -e -p "web管理界面password: " password

  parse_password
}

parse_dir() {
  [ -n "${nps_dir}" ] && return

  read -e -p "确定安装到 ${default_nps_dir}? [Y/n]" nps_dir_ensure

  [ -z "${nps_dir_ensure}" ] && nps_dir_ensure=y

  case "${nps_dir_ensure}" in
  y | Y)
    nps_dir=${default_nps_dir}
    ;;
  n | N)
    read -e -p "输入安装目录(会覆盖! 默认为 \"${default_nps_dir})\": " nps_dir

    [ -z "${nps_dir}" ] && nps_dir=${default_nps_dir}

    parse_dir
    ;;
  *)
    echo -e "[${red}Error${plain}] 请输入 [y/n]"
    parse_dir
    ;;
  esac
}

get_architecture() {
  local arch=""
  case $(uname -m) in
  i386) arch="386" ;;
  i686) arch="386" ;;
  x86_64) arch="amd64" ;;
  arm) dpkg --print-architecture | grep -q "arm64" && arch="arm64" || arch="arm" ;;
  esac

  echo ${arch}
}

get_os() {
  if [ "$(uname)" == "Darwin" ]; then
    echo "darwin"
  elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    echo "linux"
  else
    echo "仅支持 Mac 和 Linux"
    exit 1
  fi
}

download() {
  local filename=$(basename $1)

  url=${2:-}
  if [ -z "${url}" ]; then
    url=${1}
  fi

  if [ -f ${1} ]; then
    echo -e "${yellow}${filename} [found]${plain}"
  else
    echo "${filename} not found, download now..."
    echo -e "${green}wget --no-check-certificate -c -t3 -T60 -O ${filename} ${url}${plain}"
    wget --no-check-certificate -c -t3 -T60 -O ${filename} ${url}
    if [ $? -ne 0 ]; then
      echo -e "[${red}Error${plain}] Download ${filename} failed."
      exit 1
    fi
  fi
}

quoteRe() { sed -e 's/[^^]/[&]/g; s/\^/\\^/g; $!a\'$'\n''\\n' <<<"$1" | tr -d '\n'; }

quoteSubst() {
  IFS= read -d '' -r < <(sed -e ':a' -e '$!{N;ba' -e '}' -e 's/[&/\]/\\&/g; s/\n/\\&/g' <<<"$1")
  printf %s "${REPLY%$'\n'}"
}

append_cmd_copy() {
  [ ! -f "${nps_dir}/web/views/client/list.html.bak" ] && cp ${nps_dir}/web/views/client/list.html ${nps_dir}/web/views/client/list.html.bak

  rm ${nps_dir}/web/views/client/list.html
  cp ${nps_dir}/web/views/client/list.html.bak ${nps_dir}/web/views/client/list.html

  copy_btn=$(
    cat <<-EOF
\`<br><br>
<button class="btn-info copy-btn" 
data-clipboard-text='bash -c "\$(wget -O - http://static.xinshangshangxin.com/shell-tools/nps/npc.sh)" - -server={{.ip}}:{{.p}} -vkey=\${row.VerifyKey} -type={{.bridgeType}}'>
复制第一次运行命令
</button>
&nbsp&nbsp&nbsp&nbsp
<button class="btn-info copy-btn" 
data-clipboard-text='~/nps/npc -server="{{.ip}}:{{.p}}" -vkey=\${row.VerifyKey} -type={{.bridgeType}}'>
复制运行命令</button>\`
EOF
  )

  local data=$(cat ${nps_dir}/web/views/client/list.html)
  local from='<div class="wrapper wrapper-content animated fadeInRight">'
  local to=$(
    cat <<EOF
  <script src="//cdn.bootcss.com/clipboard.js/2.0.4/clipboard.min.js"></script><div class="wrapper wrapper-content animated fadeInRight">
  
  <script>
      setTimeout(() => {
      new ClipboardJS('.copy-btn');
      document.querySelector('.detail-icon').click()
    }, 500);
</script>
EOF
  )

  data=$(sed -e ':a' -e '$!{N;ba' -e '}' -e "s/$(quoteRe "$from")/$(quoteSubst "$to")/" <<<"$data")

  from="</code>\""
  to="</code>\"+${copy_btn}"

  data=$(sed -e ':a' -e '$!{N;ba' -e '}' -e "s/$(quoteRe "$from")/$(quoteSubst "$to")/" <<<"$data")

  echo -e "${data}" >${nps_dir}/web/views/client/list.html
}

change_conf() {
  [ ! -f "${nps_dir}/conf/nps.conf.bak" ] && cp "${nps_dir}/conf/nps.conf" "${nps_dir}/conf/nps.conf.bak"

  ${sed} -i "s/^http_proxy_port.*/http_proxy_port=${port}/g" "${nps_dir}/conf/nps.conf"
  ${sed} -i "s/^https_proxy_port.*/https_proxy_port=/g" "${nps_dir}/conf/nps.conf"
  ${sed} -i "s/^bridge_port.*/bridge_port=${port}/g" "${nps_dir}/conf/nps.conf"
  ${sed} -i "s/^public_vkey.*/public_vkey=/g" "${nps_dir}/conf/nps.conf"
  ${sed} -i "s/^web_host.*/web_host=${host}/g" "${nps_dir}/conf/nps.conf"
  ${sed} -i "s/^web_password.*/web_password=${password}/g" "${nps_dir}/conf/nps.conf"
  ${sed} -i "s/^web_port.*/web_port=${port}/g" "${nps_dir}/conf/nps.conf"
  ${sed} -i "s/^auth_key.*/auth_key=/g" "${nps_dir}/conf/nps.conf"
  ${sed} -i "s/^auth_crypt_key.*/auth_crypt_key=/g" "${nps_dir}/conf/nps.conf"
  ${sed} -i "s/^allow_user_login.*/allow_user_login=true/g" "${nps_dir}/conf/nps.conf"
  ${sed} -i "s/^#log_path/log_path/g" "${nps_dir}/conf/nps.conf"
}

install_service() {
  # 因为可能需要绑定 80 端口, 所以 User 和 Group 均为 root
  ${sh_c} "tee /lib/systemd/system/nps.service <<-'EOF'
[Unit]
Description=nps server
After=network.target
Documentation=https://github.com/cnlh/nps
[Service]
User=root
Group=root
ExecStart=${nps_dir}/nps
Restart=always
RestartSec=30s
[Install]
WantedBy=multi-user.target
EOF"

  ${sh_c} "systemctl enable nps"
  ${sh_c} "systemctl daemon-reload"
  ${sh_c} "systemctl restart nps"

  echo -e "${green}systemctl status nps\njournalctl -f -u nps${plain}"
}

get_download_url() {
  os=${1}
  arch=${2}

  if [ "1" == "${github}" ]; then
    url_prefix=${github_url_prefix}
  else
    url_prefix=${qiniu_url_prefix}
  fi

  echo "${url_prefix}/cnlh/nps/releases/download/v${nps_version}/${os}_${arch}_server.tar.gz"
}

check_is_install() {
  local is_install='y'
  if [ ! -d ${nps_dir} ]; then
    is_install='y'
  else
    cd ${nps_dir}
    ls -la
    if [ -f "nps" ]; then
      read -e -p "nps已安装, 是否覆盖? [Y/n] " is_install
      [ -z "${is_install}" ] && is_install=y
    fi
  fi

  case "${is_install}" in
  n | N)
    echo "取消安装"
    exit 1
    ;;
  esac
}

backup_conf() {
  cd ${nps_dir}

  local date_bak_dir="bak/$(date +%s)"
  if [ -d conf ]; then
    mkdir -p ${date_bak_dir}
    cp -r conf ${date_bak_dir}

    rm -rf bak/conf
    mv conf bak/conf
  fi
}

restore_conf() {
  cd ${nps_dir}

  rm conf/clients.json
  cp bak/conf/clients.json conf/clients.json

  rm conf/hosts.json
  cp bak/conf/hosts.json conf/hosts.json

  rm conf/tasks.json
  cp bak/conf/tasks.json conf/tasks.json
}

install() {
  mkdir -p ${nps_dir}
  cd ${nps_dir}

  backup_conf

  os=$(get_os)

  arch=$(get_architecture)
  url=$(get_download_url ${os} ${arch})
  filename=$(basename ${url})
  echo "${filename}"

  rm -rf ${filename}
  download ${filename} ${url}

  echo "tar -zxvf ${filename}"
  tar -zxvf ${filename}
  rm -rf ${filename}

  append_cmd_copy
  change_conf
  restore_conf

  if [ "linux" == "${os}" ]; then
    install_service
  elif [ "darwin" == "${os}" ]; then
    echo -e "${yellow}启动命令: ${green}${nps_dir}/nps${plain}"
    echo -e "${yellow}http://${host}:${port}${plain}"
    echo ""
    ${nps_dir}/nps
  fi
}

set_sed_command
parse_args $*
set_sh
parse_dir
check_is_install
parse_host
parse_password
parse_port
install
