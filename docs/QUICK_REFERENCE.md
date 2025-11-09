# FinRobot-AF Quick Reference

快速参考指南，用于日常开发和维护。

## 🚀 常用命令

### 报告管理

```bash
# 整理所有报告文件到正确位置
./scripts/organize_reports.sh

# 检查根目录是否有遗漏的报告
ls -1 *.md

# 查看所有开发报告
ls -1 docs/development-reports/*.md
```

### 文档查看

```bash
# 查看文档结构
tree docs/ -L 2

# 计算文档数量
find docs/ -name "*.md" | wc -l

# 查看报告索引
cat docs/development-reports/README.md
```

### 开发工作流

```bash
# 运行测试
pytest tests/

# 安装依赖
pip install -r requirements.txt

# 安装开发模式
pip install -e .
```

## 📝 生成报告的标准流程

### 步骤 1: 明确指定路径

向 AI agent 请求时：

```
请创建 [功能] 测试报告，保存到：
docs/development-reports/[FEATURE]_TEST_REPORT_20241109.md
```

### 步骤 2: 运行整理脚本

```bash
./scripts/organize_reports.sh
```

### 步骤 3: 更新索引

```bash
vim docs/development-reports/README.md
# 添加新报告的条目
```

### 步骤 4: 提交

```bash
git add docs/development-reports/
git commit -m "Add [feature] test report"
```

## 📁 文件放置规则

| 文件类型 | 位置 | 示例 |
|---------|------|------|
| 项目主 README | 根目录 | `README.md` |
| 开发报告 | `docs/development-reports/` | `TEST_REPORT.md` |
| 用户指南 | `docs/user-guide/` | `agents.md` |
| 教程 | `docs/tutorials/` | `01-market-analysis.md` |
| API 文档 | `docs/api/` | `agents.md` |
| 示例代码 | `examples/` | `basic_market_analysis.py` |
| 测试代码 | `tests/` | `test_workflows.py` |
| 源代码 | `finrobot/` | `agents/workflows.py` |

## 📋 报告命名规范

```bash
# 测试报告
[FEATURE]_TEST_REPORT.md
例: RAG_INTEGRATION_TEST_REPORT.md

# 项目总结
PROJECT_[TOPIC]_SUMMARY.md
例: PROJECT_STATUS_SUMMARY.md

# 分析报告
[TOPIC]_ANALYSIS.md
例: PERFORMANCE_ANALYSIS.md

# 实现报告
[FEATURE]_IMPLEMENTATION.md
例: MULTI_AGENT_IMPLEMENTATION.md

# 示例输出
[SYMBOL]_Analysis_[TIMESTAMP].md
例: AAPL_Analysis_20241109_143022.md
```

## 🔍 检查清单

### 提交前检查

- [ ] 运行 `./scripts/organize_reports.sh`
- [ ] 检查 `ls -1 *.md` 只显示必要文件
- [ ] 更新了 `docs/development-reports/README.md`
- [ ] 代码通过测试
- [ ] 文档链接正确

### 每周维护

- [ ] 运行整理脚本
- [ ] 审查新增报告
- [ ] 更新文档索引
- [ ] 清理临时文件

### 每月审查

- [ ] 归档旧报告
- [ ] 更新统计信息
- [ ] 审查文档完整性
- [ ] 更新 CHANGELOG

## 🎯 快速链接

### 文档
- [主文档](README.md)
- [快速开始](quick-start.md)
- [安装指南](installation.md)
- [配置指南](configuration.md)
- [开发指南](DEVELOPMENT_GUIDE.md)
- [报告管理](REPORT_MANAGEMENT.md)

### 用户指南
- [Agents 指南](user-guide/agents.md)
- [Workflows 指南](user-guide/workflows.md)

### 教程
- [市场分析教程](tutorials/01-market-analysis.md)

### API 参考
- [Agents API](api/agents.md)

### 开发报告
- [报告索引](development-reports/README.md)

## 💡 常见任务

### 创建新的测试报告

```bash
# 1. 生成报告（通过 AI 或手动）
touch docs/development-reports/NEW_FEATURE_TEST_REPORT.md

# 2. 编写报告内容
vim docs/development-reports/NEW_FEATURE_TEST_REPORT.md

# 3. 更新索引
vim docs/development-reports/README.md

# 4. 提交
git add docs/development-reports/
git commit -m "Add test report for new feature"
```

### 移动错放的报告

```bash
# 方法 1: 使用脚本（推荐）
./scripts/organize_reports.sh

# 方法 2: 手动移动
mv MY_REPORT.md docs/development-reports/

# 更新索引
vim docs/development-reports/README.md
```

### 查看项目统计

```bash
# 文档数量
find docs/ -name "*.md" | wc -l

# 报告数量
ls -1 docs/development-reports/*.md | wc -l

# 代码文件数量
find finrobot/ -name "*.py" | wc -l

# 项目总大小
du -sh .
```

## 🛠️ 故障排除

### 问题: 脚本没有权限

```bash
chmod +x scripts/organize_reports.sh
```

### 问题: 找不到报告

```bash
# 搜索所有 .md 文件
find . -name "*.md" -type f

# 只搜索报告类文件
find . -name "*REPORT*.md" -o -name "*SUMMARY*.md"
```

### 问题: Git 提示有未跟踪的文件

```bash
# 查看未跟踪的文件
git status

# 如果是报告文件，移动到正确位置
./scripts/organize_reports.sh

# 或添加到 .gitignore
echo "MY_FILE.md" >> .gitignore
```

## 📞 获取帮助

### 文档问题
- 查看 [FAQ](reference/faq.md)
- 查看 [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)

### 报告管理问题
- 查看 [REPORT_MANAGEMENT.md](REPORT_MANAGEMENT.md)
- 查看 [development-reports/README.md](development-reports/README.md)

### 技术问题
- 查看项目 README
- 查看 API 文档
- 提交 GitHub Issue

## 🎓 最佳实践

1. **总是指定完整路径** - 生成文件时使用完整路径
2. **定期运行整理脚本** - 每周至少一次
3. **更新文档索引** - 添加新文件后立即更新
4. **使用描述性命名** - 清晰的文件名和日期
5. **提交前检查** - 确保没有遗漏的文件

---

**Last Updated**: November 9, 2024
**Version**: 1.0
