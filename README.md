# ACE Music tasks for ChatGPT

Build an independently installable ChatGPT Apps SDK package for checking your existing ACE Music tasks. It exposes one read-only tool, `acemusic_get_existing_task`, and a component that displays task state and completed track metadata. It preserves partial results and supports same-ID refresh.

The [shared adapter](https://github.com/AceDataCloud/SunoChatGPT) is pinned as a submodule. The release archive contains only the ACE Music profile, its built widget and a launcher that fixes the service at startup. The required OAuth scope is `acemusic.tasks:read`.

## Build

With Python 3.12+, Git and Node.js 22+:

```sh
git clone --recurse-submodules https://github.com/AceDataCloud/ACEMusicChatGPT.git
cd ACEMusicChatGPT
python3 scripts/package.py --output dist/acemusic-chatgpt.tar.gz
```

The builder prints the archive SHA-256. Follow [installation and runtime configuration](INSTALL.md) to run the archive behind a TLS reverse proxy. Production authorization and the trusted ownership reader must be provided by the operator. The [listing draft in the shared source](upstream/profiles/acemusic/listing.json) tracks directory submission separately.

[简体中文](README.zh-CN.md)
