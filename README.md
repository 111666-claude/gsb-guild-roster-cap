# guild-roster-cap

公会名册容量与候补队列。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m guild --sample=cap
python3 -m guild --sample=vip
python3 -m guild --sample=promote
python3 -m guild --sample=idempotent
python3 -m guild --sample=work
```

不带 `--sample` 时从标准输入读 JSONL，字段为 `id`、`action`（`apply` / `leave`）、`player`、`vip`、`at`。

## 口径

- **容量**：在册成员不超过 `cap`，超出的申请进候补队列，状态为 `waiting`。
- **VIP 覆盖层**：`vip` 为真的申请不受容量限制，直接入会。
- **补位**：有空缺时按申请先后把候补队列里的第一名补进名册。
- **重复申请**：已经在册或已在候补的玩家重复申请时状态不变，不占新名额。
- **幂等**：同一个 `id` 只处理一次。

## 不变量

- 在册人数不超过 `cap`（VIP 除外）。
- 同一玩家不会同时出现在名册和候补队列里。
- `scanned` 不得随名册人数放大。

## 输出契约

每次操作打印一行：

```
{"id": <原样>, "status": <member|waiting|left|absent|bad-request>, "size": N, "waiting": N}
```

`--sample=work` 只打印 `{"members": N, "scanned": N}`。
