#!/usr/bin/env bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

set -o errexit
set -o pipefail
set -o nounset
# set -o xtrace

# 变量区开始 #
nps_dir=
server=
vkey=
nps_path=

type=tcp
service=0
github=0
nps_version="0.25.2"
user="$(id -un 2>/dev/null || true)"
default_nps_dir="$(eval echo ~$user)/nps"

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

help() {
  echo "Usage:"
  echo "  bash npc.sh -s demo.com:80 -v somekey"
  echo ""
  echo "Options:"
  echo "  -s, --server=       服务器地址           (ip:端口)"
  echo "  -k, --vkey=         vkey                 (从web端获取)"
  echo "  -d, --dir=          npc安装路径          (默认为 ~/nps/)"
  echo "  -v, --version=      nps版本              (默认为 ${nps_version})"
  echo "  -g, --github        从github下载         (默认为七牛下载)"
  echo "  --service           linux下安装开机启动"
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
    -k | --vkey | -vkey)
      vkey="${argVal}"
      ;;
    -s | --server | -server)
      server="${argVal}"
      ;;
    -g | --github)
      github=1
      ;;
    -t | --type | -type)
      type="${argVal}"
      ;;
    --service)
      service=1
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

parse_vkey() {
  [ -n "${vkey}" ] && return

  read -e -p "vkey(从web端获取): " vkey
  parse_vkey
}

parse_server() {
  [ -n "${server}" ] && return

  read -e -p "服务器地址(ip:端口): " server
  parse_server
}

parse_dir() {
  [ -n "${nps_dir}" ] && return

  [ -z "${nps_dir}" ] && nps_dir=${default_nps_dir}

  while true; do
    read -e -p "确定安装到 ${nps_dir}? [Y/n] " nps_dir_ensure

    [ -z "${nps_dir_ensure}" ] && nps_dir_ensure=y

    case "${nps_dir_ensure}" in
    y | Y)
      break
      ;;
    n | N)
      read -e -p "输入安装目录(会覆盖! 默认为 \"${default_nps_dir})\": " nps_dir
      parse_dir
      break
      ;;
    *)
      echo -e "[${red}Error${plain}] 请输入 [y/n]"
      ;;
    esac
  done
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

get_download_url() {
  os=${1}
  arch=${2}

  if [ "1" == "${github}" ]; then
    url_prefix=${github_url_prefix}
  else
    url_prefix=${qiniu_url_prefix}
  fi

  echo "${url_prefix}/cnlh/nps/releases/download/v${nps_version}/${os}_${arch}_client.tar.gz"

}

install() {
  mkdir -p ${nps_dir}
  cd ${nps_dir}

  rm -f npc
  arch=$(get_architecture)
  os=$(get_os)
  url=$(get_download_url ${os} ${arch})
  filename=$(basename ${url})

  rm -f ${filename}
  download ${filename} ${url}
  echo "tar -zxvf ${filename}"
  tar -zxvf ${filename}
  rm -f ${filename}
}

get_run_cmd() {
  echo ${nps_dir}/npc -server=${server} -vkey=${vkey} -type=${type}
}

install_service() {
  os=$(get_os)

  [ "linux" != "${os}" ] && return

  ${sh_c} "tee /lib/systemd/system/npc.service <<-'EOF'
[Unit]
Description=npc
After=network.target
Documentation=https://github.com/cnlh/nps
[Service]
User=${user}
Group=${user}
ExecStart=$(get_run_cmd)
Restart=always
RestartSec=30s
[Install]
WantedBy=multi-user.target
EOF"

  ${sh_c} "systemctl enable npc"
  ${sh_c} "systemctl daemon-reload"
  ${sh_c} "systemctl restart npc"
}

run() {
  cmd=$(get_run_cmd)

  echo -e "${yellow}bash npc.sh -s ${server} -d ${nps_dir} -k ${vkey}${plain}"
  echo -e "${green}${cmd}${plain}"
  ${cmd}
}

parse_args $*
set_sh
parse_dir
parse_server
parse_vkey
install

if [ "0" == ${service} ]; then
  run
elif [ "1" == "${service}" ]; then
  install_service
fi
