# Agent 分工说明

## Architecture Agent

输入：仓库扫描结果、README、目录结构、依赖文件。  
输出：项目架构摘要、核心模块职责、潜在技术债。

## Retrieval Agent

输入：Issue 描述、仓库摘要、文件列表。  
输出：与任务最相关的源码文件、测试文件和配置文件。

## Implementation Agent

输入：Issue、相关文件、架构说明。  
输出：初始代码补丁或测试补丁。

## Test Agent

输入：测试命令、工作目录。  
输出：测试日志、退出码、失败摘要。

## Review Agent

输入：失败日志、补丁、相关代码。  
输出：失败原因分析、修复建议、二次修复计划。

## Documentation Agent

输入：最终补丁、测试结果、修复说明。  
输出：PR 描述、测试结果摘要、风险评估、迁移说明。
