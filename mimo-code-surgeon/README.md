# MiMo Code Surgeon

MiMo Code Surgeon 是一个 **多 Agent 自动化代码重构与可验证 PR 生成系统**。它的目标不是简单生成代码，而是把真实仓库维护任务拆成一条可审计、可回归、可证明的工程链路：

```text
Issue 输入
  -> 仓库扫描
  -> 架构理解
  -> 相关文件定位
  -> 代码补丁生成
  -> 单元测试 / 静态检查
  -> 失败日志分析
  -> 二次修复
  -> PR 描述、迁移说明、风险评估生成
```

本项目适合作为 MiMo / OpenAI-Compatible API 的 Agent 工程示例，用于展示长上下文仓库理解、多 Agent 协作、自动测试回归和可验证 PR 产出。

## 项目亮点

- **多 Agent 协作**：Architecture / Retrieval / Implementation / Test / Review / Documentation Agent。
- **可验证闭环**：不是只输出代码，而是输出 patch、测试日志、失败分析、修复说明和 PR 描述。
- **长上下文友好**：支持读取 README、源码、测试、依赖文件、Issue 描述和 CI 日志。
- **无 API Key 可运行**：默认 mock 模式可本地跑通完整闭环。
- **可接入真实 MiMo API**：支持 OpenAI-Compatible 配置，后续可替换 mock Agent 为真实 LLM Agent。
- **适合申请 Token 额度**：项目天然需要大量 token 处理仓库扫描、多轮推理、补丁生成和回归验证。

## 快速开始

```bash
git clone https://github.com/your-name/mimo-code-surgeon.git
cd mimo-code-surgeon

python -m venv .venv
source .venv/bin/activate
pip install -e .

mimo-surgeon run \
  --repo examples/sample_repo \
  --issue "修复 calculator.divide 在除数为 0 时行为不清晰的问题，并补充测试" \
  --test "python -m unittest discover -s tests"
```

Windows PowerShell：

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -e .

mimo-surgeon run `
  --repo examples/sample_repo `
  --issue "修复 calculator.divide 在除数为 0 时行为不清晰的问题，并补充测试" `
  --test "python -m unittest discover -s tests"
```

运行完成后会生成类似目录：

```text
runs/20260429T120000Z/
├── input_issue.md
├── repo_summary.md
├── architecture.md
├── plan.md
├── test_before.log
├── first_patch.diff
├── test_first_attempt.log
├── repair_notes.md
├── repair_patch.diff
├── test_after.log
├── pr_description.md
├── token_estimate.json
└── working_repo/
```

## 接入 MiMo / OpenAI-Compatible API

复制环境变量模板：

```bash
cp .env.example .env
```

填写：

```bash
MIMO_API_KEY=your_api_key
MIMO_BASE_URL=https://your-openai-compatible-endpoint/v1/chat/completions
MIMO_MODEL=mimo-v2.5
```

然后执行：

```bash
mimo-surgeon run \
  --repo examples/sample_repo \
  --issue "修复 calculator.divide 在除数为 0 时行为不清晰的问题，并补充测试" \
  --test "python -m unittest discover -s tests" \
  --mode auto
```

当前版本默认优先保障可复现 demo，因此即使没有 API Key 也会自动进入 mock 模式。真实 API 接入逻辑在 `src/mimo_code_surgeon/llm.py` 中，后续可将各 Agent 的 mock 逻辑替换为真实 LLM 调用。

## 目录结构

```text
mimo-code-surgeon/
├── src/mimo_code_surgeon/
│   ├── cli.py
│   ├── workflow.py
│   ├── repo_scanner.py
│   ├── test_runner.py
│   ├── patch_utils.py
│   ├── token_estimator.py
│   ├── llm.py
│   └── agents/
├── examples/
│   ├── issues/
│   └── sample_repo/
├── prompts/
├── docs/
├── runs/local-demo/
├── tests/
├── TOKEN_APPLICATION_DRAFT.md
└── pyproject.toml
```

## Demo 说明

`runs/local-demo/` 中已经放置了一次完整示例运行结果，用于证明本项目不是纯文字构想，而是已经跑通了基础闭环：

```text
Issue -> 仓库分析 -> 增加回归测试 -> 测试失败 -> 分析失败原因 -> 修复源码 -> 测试通过 -> 生成 PR 说明
```

## 后续规划

- 接入 GitHub API，自动读取 Issue、PR、CI 日志。
- 支持真实仓库的多文件 patch 生成。
- 支持 pytest、unittest、npm test、go test 等多语言测试命令。
- 增加安全审查 Agent，检查敏感信息、危险依赖和高风险代码修改。
- 增加评测集，对每次 Agent 修改进行成功率、失败率、测试通过率和 token 消耗统计。
- 支持自动创建 GitHub PR。

## License

MIT
