#!/bin/sh
set -e

# Генерація env.js з актуальних ENV
cat <<EOF > /usr/share/nginx/html/env.js
window._env_ = {
  REACT_APP_KEYCLOAK_URL: "${REACT_APP_KEYCLOAK_URL}",
  REACT_APP_KEYCLOAK_REALM: "${REACT_APP_KEYCLOAK_REALM}",
  REACT_APP_PORTAL_URL: "${REACT_APP_PORTAL_URL}"
};
EOF

# Виклик CMD (nginx)
exec "$@"
