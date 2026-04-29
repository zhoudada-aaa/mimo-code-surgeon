# GitHub 上传步骤

## 方式一：网页上传

1. 登录 GitHub。
2. 新建仓库，例如 `mimo-code-surgeon`。
3. 解压本项目压缩包。
4. 将全部文件拖入 GitHub 网页上传。
5. 提交 commit。

## 方式二：命令行上传

```bash
unzip mimo-code-surgeon.zip
cd mimo-code-surgeon

git init
git add .
git commit -m "Initial commit: MiMo Code Surgeon"

git branch -M main
git remote add origin https://github.com/your-name/mimo-code-surgeon.git
git push -u origin main
```

上传后建议在 README 顶部补充：

```text
Demo 视频链接：
MiMo Token 申请说明：
示例运行日志：runs/local-demo/
```
