ui-shell:
  image:
    repository: 760618/ui-shell
    tag: "v1.0.0"

  ingress:
    enabled: true
    className: nginx
    hosts:
      - host: shell.local
        paths:
          - path: /
            pathType: Prefix

