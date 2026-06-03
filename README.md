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

## 脚本

```sh
python3 scripts/update_direct_rules.py
```

用于更新 `rules/policy/direct.list` 中需要跟随跳转解析最终域名的直连规则。目前会自动解析 88 影视网的当前可用域名，并更新对应规则块。
