#!/usr/bin/env bash
set -euo pipefail

# Приймемо список імен/доменів з ENV або дефолтів
# Можеш передати сервісні DNS K8s: "admin-core config-svc"
DOMAINS="${DOMAINS:-"admin-core config-svc"}"
INTERVAL_SEC="${INTERVAL_SEC:-5}"
OUT_DIR="${OUT_DIR:-/tmp/nginx-dns}"
LOG_PREFIX="[nginx-reloader]"

mkdir -p "${OUT_DIR}"

echo "$LOG_PREFIX starting nginx..."
# стартуємо nginx у daemon-режимі (офіційний entrypoint це дозволяє)
nginx

echo "$LOG_PREFIX watching domains: ${DOMAINS}"
echo "$LOG_PREFIX check interval: ${INTERVAL_SEC}s"

resolve_ips() {
  local name="$1"
  # 1) Спроба через dig (A/AAAA), короткий вивід
  local a
  a="$(dig +time=1 +tries=1 +search +short "$name" 2>/dev/null || true)"
  if [[ -z "$a" ]]; then
    # 2) Фолбек на getent/hosts (корисно у k8s alpine)
    a="$(getent hosts "$name" 2>/dev/null | awk '{print $1}' | sort -u || true)"
  fi
  # нормалізуємо сортування
  echo "$a" | sed '/^$/d' | sort -u
}

while true; do
  for d in $DOMAINS; do
    prev_file="${OUT_DIR}/${d}.txt"
    current="$(resolve_ips "$d" | tr '\n' ' ' | sed 's/[[:space:]]\+$//')"

    if [[ -z "$current" ]]; then
      echo "$LOG_PREFIX WARN: $d has no resolved IPs (skipping)"
      continue
    fi

    if [[ -f "$prev_file" ]]; then
      prev="$(cat "$prev_file" | tr '\n' ' ' | sed 's/[[:space:]]\+$//')"
      if [[ "$current" != "$prev" ]]; then
        echo "$LOG_PREFIX DNS change for $d: '$prev' -> '$current' . Reloading nginx..."
        # невелика пауза, щоб уникати бурстів
        sleep 2
        nginx -s reload || {
          echo "$LOG_PREFIX ERROR: nginx reload failed, retrying in 2s..."
          sleep 2
          nginx -s reload || echo "$LOG_PREFIX ERROR: second reload failed"
        }
      fi
    else
      echo "$LOG_PREFIX no previous record for $d. current='$current'"
    fi

    echo "$current" > "$prev_file"
  done

  sleep "$INTERVAL_SEC"
done
