#!/usr/bin/env python3
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import re
import sys

RULE_FILE = Path("rules/policy/direct.list")
TARGETS = [
    {
        "name": "88影视网",
        "homepages": ["https://www.88ys.cn", "https://www.88ys.app"],
        "references": ["https://www.88ys.cn", "https://www.88ys.app"],
        "block_pattern": re.compile(
            r"^# \[88影视网\][^\n]*\n(?:DOMAIN-SUFFIX,[^\n]+\n?)*",
            re.MULTILINE,
        ),
    }
]


def normalize_hostname(url: str) -> str:
    hostname = urlparse(url).hostname
    if not hostname:
        raise ValueError(f"无法从 URL 中解析域名: {url}")

    return hostname[4:] if hostname.startswith("www.") else hostname


def resolve_final_domain(homepage: str) -> str:
    request = Request(
        homepage,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0 Safari/537.36"
            )
        },
    )

    with urlopen(request, timeout=10) as response:
        return normalize_hostname(response.geturl())


def resolve_target_domain(target: dict[str, object]) -> str:
    errors = []

    for homepage in target["homepages"]:
        try:
            return resolve_final_domain(homepage)
        except (OSError, URLError, ValueError) as error:
            errors.append(f"{homepage}: {error}")

    raise RuntimeError("; ".join(errors))


def build_rule_block(target: dict[str, object], domain: str) -> str:
    references = " ".join(target["references"])
    return f"# [{target['name']}]({references})\nDOMAIN-SUFFIX,{domain}\n"


def upsert_rule_block(content: str, target: dict[str, object], domain: str) -> str:
    block = build_rule_block(target, domain)
    pattern = target["block_pattern"]

    if pattern.search(content):
        return pattern.sub(block, content, count=1)

    return f"{content.rstrip()}\n\n{block}"


def main() -> int:
    content = RULE_FILE.read_text(encoding="utf-8")
    updates = []

    for target in TARGETS:
        domain = resolve_target_domain(target)
        content = upsert_rule_block(content, target, domain)
        updates.append(f"{target['name']}: {domain}")

    RULE_FILE.write_text(content, encoding="utf-8")
    print(f"已更新 {RULE_FILE}")
    for update in updates:
        print(f"- {update}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, URLError, RuntimeError, ValueError) as error:
        print(f"更新 direct 规则失败: {error}", file=sys.stderr)
        raise SystemExit(1)
