# Report Management Guide

如何管理 FinRobot-AF 项目中 AI 生成的开发报告。

## 🎯 问题说明

当使用 AI coding agent（如 Claude Code）生成报告时，这些文件**默认不会**自动放到 `docs/development-reports/` 目录，而是会放在当前工作目录（通常是项目根目录）。

## ✅ 解决方案

我们提供了多种方法来管理这个问题：

---

## 方法 1: 使用自动化脚本（推荐）

### 快速使用

```bash
# 运行整理脚本
./scripts/organize_reports.sh
```

脚本会自动：
- ✅ 扫描项目根目录
- ✅ 找到所有报告文件（`*_REPORT.md`, `*_SUMMARY.md` 等）
- ✅ 移动到 `docs/development-reports/`
- ✅ 跳过重要的根目录文件（README.md 等）
- ✅ 显示移动结果

### 定期运行

建议在以下情况运行脚本：
- 使用 AI agent 生成报告后
- 每周清理一次
- 提交代码前

---

## 方法 2: 明确指定文件路径

在请求 AI agent 生成报告时，**明确指定完整路径**：

### ❌ 不好的做法
```
"生成一个测试报告"
"创建项目总结"
```

### ✅ 好的做法
```
"生成一个测试报告，保存到 docs/development-reports/NEW_FEATURE_TEST_REPORT.md"
"创建项目总结，保存到 docs/development-reports/PROJECT_STATUS_20241109.md"
```

### 示例对话

```
用户: 请为新功能创建一个测试报告

AI: 我会创建测试报告。文件将保存到哪里？

用户: 保存到 docs/development-reports/RAG_FEATURE_TEST_REPORT.md
```

---

## 方法 3: 手动移动文件

如果报告已经在根目录生成，手动移动：

```bash
# 单个文件
mv MY_REPORT.md docs/development-reports/

# 批量移动所有报告
mv *_REPORT.md docs/development-reports/
mv *_SUMMARY.md docs/development-reports/
mv *_ANALYSIS.md docs/development-reports/
```

---

## 方法 4: Git Ignore 规则

项目的 `.gitignore` 已配置忽略根目录的报告文件：

```gitignore
# Reports generated in root directory
*_REPORT.md
*_SUMMARY.md
*_ANALYSIS.md
*_GUIDE.md

# Exceptions
!README.md
!ORGANIZATION_SUMMARY.md
```

**好处**：
- ❌ 不会意外提交根目录的报告文件到 Git
- ✅ 提醒你移动文件到正确位置

**注意**：这不会自动移动文件，只是防止提交

---

## 📋 标准工作流程

### 生成新报告的完整流程

#### 步骤 1: 生成报告（指定路径）

```
请生成 [功能] 的测试报告，保存到：
docs/development-reports/[FEATURE]_TEST_REPORT.md
```

#### 步骤 2: 如果在根目录生成了

```bash
# 运行整理脚本
./scripts/organize_reports.sh

# 或手动移动
mv *_REPORT.md docs/development-reports/
```

#### 步骤 3: 更新索引

编辑 `docs/development-reports/README.md`，添加新报告信息：

```markdown
### [NEW_FEATURE_TEST_REPORT.md](NEW_FEATURE_TEST_REPORT.md)
**Date**: 2024-11-09
**Size**: 15K
**Purpose**: Testing results for new feature

Description of what the report contains...
```

#### 步骤 4: 提交

```bash
git add docs/development-reports/NEW_FEATURE_TEST_REPORT.md
git add docs/development-reports/README.md
git commit -m "Add test report for new feature"
```

---

## 🔍 检查和验证

### 检查是否有遗漏的报告

```bash
# 列出根目录的所有 .md 文件
ls -1 *.md

# 应该只看到：
# - README.md
# - ORGANIZATION_SUMMARY.md
# - (其他重要的根文档)
```

### 如果看到其他 `*_REPORT.md` 或 `*_SUMMARY.md`

```bash
# 运行整理脚本
./scripts/organize_reports.sh
```

### 查看所有已整理的报告

```bash
# 列出所有报告
ls -1 docs/development-reports/*.md

# 查看报告数量
ls -1 docs/development-reports/*.md | wc -l
```

---

## 📊 命名规范

生成报告时使用以下命名模式：

### 测试报告
```
[FEATURE]_TEST_REPORT.md
例如: RAG_INTEGRATION_TEST_REPORT.md
```

### 项目总结
```
PROJECT_[TOPIC]_SUMMARY.md
例如: PROJECT_STATUS_SUMMARY.md
```

### 分析报告
```
[TOPIC]_ANALYSIS.md
例如: PERFORMANCE_ANALYSIS.md
```

### 实现报告
```
[FEATURE]_IMPLEMENTATION.md
例如: MULTI_AGENT_IMPLEMENTATION.md
```

### 调试报告
```
[ISSUE]_DEBUG_REPORT.md
例如: MEMORY_LEAK_DEBUG_REPORT.md
```

### 示例输出
```
[SYMBOL]_Analysis_[TIMESTAMP].md
例如: AAPL_Analysis_20241109_143022.md
```

---

## 🤖 与 AI Agent 协作的最佳实践

### 1. 明确说明文件位置

```
✅ "创建测试报告到 docs/development-reports/TEST_REPORT.md"
❌ "创建测试报告"
```

### 2. 使用完整路径

```
✅ docs/development-reports/FEATURE_ANALYSIS.md
❌ development-reports/FEATURE_ANALYSIS.md
❌ FEATURE_ANALYSIS.md
```

### 3. 包含日期和描述性名称

```
✅ INTEGRATION_TEST_REPORT_20241109.md
✅ RAG_PERFORMANCE_ANALYSIS.md
❌ report.md
❌ test.md
```

### 4. 完成后运行整理脚本

```bash
./scripts/organize_reports.sh
```

---

## 🛠️ 维护任务

### 每周清理（推荐）

```bash
# 1. 运行整理脚本
./scripts/organize_reports.sh

# 2. 检查根目录
ls -1 *.md

# 3. 更新报告索引
vim docs/development-reports/README.md

# 4. 提交变更
git add docs/development-reports/
git commit -m "Weekly report organization"
```

### 每月审查

1. 审查所有报告
2. 归档过时报告
3. 更新统计信息
4. 清理不需要的报告

---

## 📁 目录结构参考

```
FinRobot-AF/
├── README.md                         ✅ 保留在根目录
├── ORGANIZATION_SUMMARY.md           ✅ 保留在根目录
│
├── docs/
│   ├── development-reports/          ← 所有开发报告放这里
│   │   ├── README.md                 ← 报告索引
│   │   ├── *_REPORT.md              ← 测试报告
│   │   ├── *_SUMMARY.md             ← 项目总结
│   │   ├── *_ANALYSIS.md            ← 分析报告
│   │   └── ...
│   │
│   ├── user-guide/                   ← 用户指南
│   ├── tutorials/                    ← 教程
│   └── ...
│
└── scripts/
    └── organize_reports.sh           ← 自动整理脚本
```

---

## ❓ 常见问题

### Q: AI 生成的报告总是在根目录，怎么办？

**A**: 使用以下任一方法：
1. 在请求时明确指定路径
2. 生成后运行 `./scripts/organize_reports.sh`
3. 手动移动文件

### Q: 如何防止意外提交根目录的报告？

**A**: `.gitignore` 已配置，会自动忽略根目录的报告文件

### Q: 整理脚本会移动哪些文件？

**A**: 匹配以下模式的文件：
- `*_REPORT.md`
- `*_SUMMARY.md`
- `*_ANALYSIS.md`
- `*_GUIDE.md`
- `*_TEST*.md`
- `*_DEBUG*.md`

**但会保留**：
- `README.md`
- `ORGANIZATION_SUMMARY.md`
- 其他重要根文档

### Q: 可以自动运行整理脚本吗？

**A**: 可以设置 Git hooks：

```bash
# 在 .git/hooks/pre-commit 添加：
#!/bin/bash
./scripts/organize_reports.sh
```

### Q: 如果不小心删除了报告怎么办？

**A**: 使用 Git 恢复：
```bash
git checkout docs/development-reports/REPORT_NAME.md
```

---

## 📚 相关文档

- [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) - 开发指南
- [ORGANIZATION_SUMMARY.md](../ORGANIZATION_SUMMARY.md) - 项目组织总结
- [development-reports/README.md](development-reports/README.md) - 报告索引

---

## 🎯 快速参考

```bash
# 生成报告后立即运行
./scripts/organize_reports.sh

# 检查根目录
ls -1 *.md

# 查看所有报告
ls -1 docs/development-reports/*.md

# 手动移动
mv *_REPORT.md docs/development-reports/

# 更新索引
vim docs/development-reports/README.md
```

---

**Last Updated**: November 9, 2024
**Version**: 1.0
**Status**: Active
