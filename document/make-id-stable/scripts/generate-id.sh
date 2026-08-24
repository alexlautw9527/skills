#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "用法: $0 <TYPE> [LENGTH]" >&2
  echo "  TYPE   類型前綴，例如 REQ、ADR、TEST（不會做任何處理，原樣輸出）" >&2
  echo "  LENGTH 隨機段長度，8~12，預設 8" >&2
  exit 1
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage
fi

TYPE="$1"
LENGTH="${2:-8}"

if [[ -z "$TYPE" ]]; then
  usage
fi

if (( LENGTH < 8 || LENGTH > 12 )); then
  echo "LENGTH 必須在 8~12 之間" >&2
  exit 1
fi

# 字元集：RFC 4648 的 A-Z 加 2-7，再排除字形容易混淆的 I、L、O，
# 剩下 23 個字母加 2-7，共 29 字元。0、1、8、9 本來就不在標準字元集內。
ALPHABET="ABCDEFGHJKMNPQRSTUVWXYZ234567"

ID=""
while (( ${#ID} < LENGTH )); do
  read -ra BYTES < <(od -An -N16 -tu1 /dev/urandom)
  for b in "${BYTES[@]}"; do
    if (( ${#ID} >= LENGTH )); then
      break
    fi
    # 29 不是 2 的冪，byte % 29 有偏差：0~23 每個出現 9 次，24~28 每個 8 次。
    # 只接受 < 232（29 的 8 倍）的 byte，使每個字元出現機率完全相等。
    if (( b < 232 )); then
      ID+="${ALPHABET:$((b % 29)):1}"
    fi
  done
done

echo "${TYPE}-${ID}"
