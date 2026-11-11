# 加密的 Projects:如何解密与更新

[English](README_ENCRYPTION_EN.md) · 中文（本文件）

本仓库的 `Projects/` 目录是加密的。本页说明如何**解密**(读取文件)和如何**加密**(更新文件)。它放在仓库根目录是有意的:`Projects/` 里的任何文件本身都是加密的,在拿到密钥之前根本读不了。

## 哪些受保护,哪些不受保护

- `Projects/` 下的所有内容用 [git-crypt](https://github.com/AGWA/git-crypt)(AES-256)加密。在仓库和 GitHub 上,这些文件都是密文:浏览器里看到的是无法阅读的二进制,"Download ZIP"下载到的也是同样的密文。
- **所有人仍然能看到:**文件名、文件夹名、文件大小和提交历史。受保护的只有文件**内容**。
- `Projects/` 以外的内容(topics、examples、catalog、notes)是普通的公开文本。

## 解密:读取文件

需要三样东西:`git`、`git-crypt` 和**密钥**。密钥不在本仓库里,请向仓库所有者索取。它有两种形式:

- 密钥文件(`*.key`),或者
- 带口令保护的密钥文件(`*.key.gpg`)以及对应的口令。

```bash
# 1. 安装 git-crypt(Windows 请使用 WSL)
sudo apt install git-crypt          # Debian / Ubuntu
brew install git-crypt              # macOS

# 2. 克隆仓库。必须是真正的 git clone,下载的 ZIP 无法解锁
git clone <仓库地址>
cd <仓库目录>

# 3. 解锁,按你拿到的密钥形式选择其一
git-crypt unlock /path/to/KEYFILE                    # 普通密钥文件
tools/projects-crypt/unlock.sh /path/to/KEYFILE.gpg  # 带口令的密钥:按提示输入口令
```

确认成功:`Projects/` 下的文件已经是可读的文本。想重新锁定,执行 `git-crypt lock`(工作区必须干净)。

如果所有者用 GPG 公钥授权了你,则不带参数执行 `git-crypt unlock` 即可。

## 加密:更新文件(所有者)

**没有单独的加密命令。** git-crypt 在 `git add` 时自动加密,所以你照常编辑、提交即可。请在已经解锁的克隆里操作:

```bash
# 照常编辑 Projects/ 下的文件,然后:
git add -A Projects            # 修改、新增、删除都会处理
git commit -m "update projects"
tools/projects-crypt/verify.sh # 可选但建议:确认仓库里存的全是密文
git push
```

- 在 `Projects/` 下新建的文件会自动加密。
- 要保护更多文件,在 `.gitattributes` 里加一条规则,**先单独提交这个文件**,再添加要加密的文件(Git 已经在跟踪的文件要用 `git add --renormalize <文件>`):
  ```gitattributes
  private/** filter=git-crypt diff=git-crypt        # 整个目录
  notes/diary.md filter=git-crypt diff=git-crypt    # 单个文件
  ```
  同一把密钥可以解锁所有规则。详见[使用笔记](notes/git-crypt-usage.md)。
- 随时检查:`git-crypt status -e | grep WARNING` 必须没有输出。

## 必须遵守的规则

1. **只在本仓库的克隆里工作。** 不要把文件复制到另一个仓库再提交:加密设置保存在 `.git` 里,不在文件里,复制过去的文件会以**明文**存储。
2. **仓库处于锁定状态时不要编辑文件。** 那时它们是读不了的密文,先解锁。
3. **备份密钥**到仓库之外的至少两个位置。丢了就无法恢复加密的文件。
4. **公开仓库之前,或做过任何特殊操作之后,**运行 `tools/projects-crypt/verify.sh --remote origin`。它会审计每个文件、每个提交,以及远端的每个分支和标签。
5. 不要写会匹配到 `.gitattributes` 本身的规则(例如 `*` 或 `**`)。

## 脚本(`tools/projects-crypt/`)

| 脚本 | 用途 |
|---|---|
| `unlock.sh [KEY 或 KEY.gpg]` | 克隆后解锁。使用 `.gpg` 密钥时会提示输入口令。 |
| `verify.sh [--remote origin]` | 审计 `Projects/` 下每个存储的版本是否都是密文。 |
| `setup.sh --key-out FILE` | 一次性设置:在仓库中启用加密。 |
| `purge-history.sh DEST` | 一次性:生成一个历史中不含明文的干净克隆。 |

每个脚本都有 `--help`。

## 常见问题

| 问题 | 原因与处理 |
|---|---|
| `Projects/` 下的文件是无法阅读的乱码 | 仓库处于锁定状态。按上文解锁。 |
| `not a valid git-crypt key file` | 文件不对。请使用所有者给你的密钥文件,不要用其他文件。 |
| `git-crypt: command not found` | 还没安装 git-crypt(见上文)。 |
| 我下载的是 ZIP | ZIP 无法解锁,请使用 `git clone`。 |
| `git-crypt lock` 提示 `Working directory not clean` | 先提交或暂存改动;`--force` 可能丢失未提交的修改。 |
| 我忘记了口令 | 无法找回。只有备份的普通密钥文件才能解锁仓库。 |
| 还有别的内容被隐藏吗? | 没有。文件名、大小和历史仍然公开,见"哪些受保护,哪些不受保护"。 |

## 更多资料

- [git-crypt 使用笔记](notes/git-crypt-usage.md) · [English](notes/git-crypt-usage_EN.md):完整说明,包括 GPG 授权、添加规则,以及曾经提交过明文时怎么办。
- 官方项目:<https://github.com/AGWA/git-crypt>
