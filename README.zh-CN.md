# 适用于 ChatGPT 的 ACE Music 任务查看器

此安装包仅包含 ACE Music 的只读工具与结果组件。用户通过自己的 OAuth 授权查询已有任务、查看已完成音轨的标题和时长，并用原任务 ID 刷新状态。部分失败时保留成功的音轨。

先安装 Python 3.12+、Git 和 Node.js 22+，检出固定源码并构建：

```sh
git clone --recurse-submodules https://github.com/AceDataCloud/ACEMusicChatGPT.git
cd ACEMusicChatGPT
python3 scripts/package.py --output dist/acemusic-chatgpt.tar.gz
```

构建命令会输出归档的 SHA-256，安装步骤与 OAuth、可信任务查询服务所需环境变量见 [INSTALL.md](INSTALL.md)。此仓库使用固定提交的共享 Apps SDK 实现。ChatGPT 应用目录收录和生产授权服务需要另外部署与审核。
