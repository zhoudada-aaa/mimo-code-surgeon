# 系统架构说明

MiMo Code Surgeon 采用多 Agent 流水线架构，将一次代码维护任务拆分为多个可审查环节。

## 核心流程

```text
用户输入 Issue
  |
  v
Repository Scanner
  - 扫描 README / 源码 / 测试 / 依赖 / 配置
  - 生成 repo_summary.md
  |
  v
Architecture Agent
  - 理解项目结构
  - 生成模块职责说明
  - 输出 architecture.md
  |
  v
Retrieval Agent
  - 定位与 Issue 相关的源码和测试文件
  - 给 Implementation Agent 提供最小上下文
  |
  v
Implementation Agent
  - 生成初始补丁
  - 本地 demo 中先补充回归测试
  |
  v
Test Agent
  - 执行测试命令
  - 保存 test log
  |
  v
Review Agent
  - 分析失败日志
  - 生成修复策略
  |
  v
Repair Patch
  - 修复源码
  - 再次运行测试
  |
  v
Documentation Agent
  - 生成 PR 描述
  - 生成风险评估和迁移说明
```

## 设计原则

1. 代码修改必须可验证，不能只输出自然语言建议。
2. 每次运行都要保留 patch、测试日志和修复说明。
3. Agent 之间传递结构化上下文，减少无效 token 消耗。
4. mock 模式用于证明工程链路，真实模型模式用于处理更复杂仓库。
5. 输出内容要适合 GitHub PR、技术评审和 Token 申请证明材料。
