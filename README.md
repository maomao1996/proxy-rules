# proxy-rules

通用代理分流规则列表，适用于 Surge / Quantumult X / Clash

## 目录结构

```sh
proxy-rules/
└─ rules/
   ├─ ai/
   │  └─ cursor.list
   ├─ sites/
   │  └─ linuxdo.list
   └─ policy/
      ├─ proxy.list
      └─ direct.list
```

- `rules/ai/`：AI 服务相关规则
- `rules/sites/`：普通站点相关规则
- `rules/policy/`：按策略归类的通用规则，如 `proxy.list`、`direct.list`
