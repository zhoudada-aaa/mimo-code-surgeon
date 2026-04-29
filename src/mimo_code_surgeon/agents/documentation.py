from __future__ import annotations

from mimo_code_surgeon.models import TestResult


class DocumentationAgent:
    def build_pr_description(self, issue: str, final_result: TestResult) -> str:
        status = "通过" if final_result.passed else "未通过"
        return f'''# PR: Clarify divide-by-zero behavior and add regression test

## 背景

本次任务来自 Issue：

> {issue}

原始 `calculator.divide` 在除数为 0 时直接依赖 Python 默认异常，行为不够清晰，不利于调用方理解和测试回归。

## 修改内容

1. 在 `tests/test_calculator.py` 中新增除数为 0 的回归测试。
2. 在 `src/calculator.py` 中显式判断 `b == 0`。
3. 当除数为 0 时抛出 `ValueError("division by zero is not allowed")`。
4. 保留正常除法行为不变。

## 测试结果

```text
{final_result.command}
```

最终状态：**{status}**

## 风险评估

- 修改范围小，仅影响 `divide` 函数。
- 正常除法路径保持不变。
- 主要行为变化是将除零场景统一为更明确的 `ValueError`。

## 回滚方案

如需回滚，移除 `divide` 中的显式 `ValueError` 判断，并删除新增回归测试即可。
'''
