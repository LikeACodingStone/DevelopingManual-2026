# git-crypt 使用笔记

[English](git-crypt-usage_EN.md) · 中文

- 别名与生态:git-crypt(AGWA/git-crypt),Git 的透明文件加密工具
- 适用平台:Linux / macOS(Windows 建议用 WSL)
- 标签:git、加密、仓库管理
- 验证状态:**已在临时仓库中实际运行验证**。环境:git-crypt 0.7.0(Ubuntu 24.04 软件包)、git 2.43.0。验证了加密、无密钥/错误口令/正确口令克隆后解锁、GPG 用户模式、`lock`、`status`,以及配套脚本;使用的是本地裸仓库作为远端,**没有在 GitHub 上实际推送测试**

## 是什么

git-crypt 让你在同一个 Git 仓库里,**只加密指定的文件或目录**,其余文件保持公开。加密算法为 AES-256。

- 本地工作区:解锁后是明文,可以正常编辑、`git add`、`git commit`。
- 远端(如 GitHub):存的是密文,浏览器里看到的是二进制内容。

## 工作原理

靠 Git 的 `filter` 机制和 `.gitattributes` 实现:

1. `.gitattributes` 声明哪些路径要加密。
2. `git add` 时,clean filter 自动加密后再写入仓库。
3. `git checkout` / 解锁时,smudge filter 自动解密到工作区。

加密文件的开头固定是 10 字节头 `\0GITCRYPT\0`,可以用它来验证文件确实加密了。

## 安装

```bash
sudo apt install git-crypt     # Debian / Ubuntu
brew install git-crypt         # macOS
git-crypt --version
```

## 快速上手(对称密钥模式)

### 1. 初始化

在仓库根目录执行,会生成一把随机的对称密钥,保存在 `.git/git-crypt/keys/default`:

```bash
git-crypt init
```

### 2. 声明要加密的路径,并**先提交**

```gitattributes
# .gitattributes
Projects/** filter=git-crypt diff=git-crypt
```

```bash
git add .gitattributes
git commit -m "configure git-crypt for Projects/"
```

> **一定要先提交 `.gitattributes`,再添加要加密的文件。** 否则文件会以明文进入仓库。
> 规则不要匹配到 `.gitattributes` 本身,否则它也会被加密。

### 3. 添加文件并检查

```bash
git add Projects
git commit -m "add encrypted projects"

git-crypt status -e                  # 列出按规则会加密的文件
git-crypt status -e | grep WARNING   # 必须没有输出
```

如果某个文件以明文进了暂存区或提交,会显示这样的警告:

```
    encrypted: Projects/x/oops.md *** WARNING: staged/committed version is NOT ENCRYPTED! ***
```

> 注意 `git-crypt status -u` 列出的是**所有没有被加密的文件**(README、`.gitattributes` 等),不是"该加密却没加密"的文件,不能用它做检查。

### 4. 验证提交的内容确实是密文

`cat-file` 读取的是仓库里存的原始内容,不会经过解密:

```bash
git cat-file blob HEAD:Projects/E009_diagram/README.md | head -c 10 | xxd
# 期望:00 47 49 54 43 52 59 50 54 00   即 \0GITCRYPT\0
```

(路径换成你仓库里真实存在的文件。要检查全部文件和全部历史,用下面的 `verify.sh`。)

### 5. 导出并备份密钥

```bash
git-crypt export-key ~/secret/devmanual.key
```

- **密钥文件千万不要放进仓库。**
- 丢了密钥又没有 GPG 授权,加密的内容就**无法恢复**。至少备份到两个不同位置。

### 6. 推送

```bash
git push
```

## 在别处解锁

```bash
git clone git@github.com:<user>/<repo>.git
cd <repo>
# 此时 Projects/ 里的文件都是二进制密文
git-crypt unlock ~/secret/devmanual.key
# 解锁后变回明文
```

没有安装 git-crypt 或没有密钥的人,clone 或下载 ZIP 后拿到的都是密文。传错密钥文件会报 `not a valid git-crypt key file`,文件保持密文。

## 用 GPG 授权多人(可选)

不共享密钥文件,而是用每个人自己的 GPG 公钥授权:

```bash
git-crypt init                                       # 仍然要先 init
git-crypt add-gpg-user --trusted alice@example.com   # 自动生成一个提交
git push
```

- `add-gpg-user` 会提交 `.git-crypt/keys/default/0/<指纹>.gpg`,即用 Alice 公钥加密后的仓库密钥。
- 如果这把公钥在你的 GPG 里还没有被信任,需要加 `--trusted`,否则会失败。

Alice 在自己的机器上 clone 后,不带参数解锁(用她的 GPG 私钥):

```bash
git-crypt unlock
```

## 想要"输入密码"的体验

git-crypt 本身没有密码,解锁靠密钥文件或 GPG 私钥。要接近"输入密码",可以把导出的密钥文件再用口令加密一层:

```bash
# 加密密钥文件
gpg --symmetric --cipher-algo AES256 --output devmanual.key.gpg ~/secret/devmanual.key

# 使用者:先输入口令解出密钥,再解锁仓库
gpg --decrypt --output /tmp/devmanual.key devmanual.key.gpg
git-crypt unlock /tmp/devmanual.key
rm /tmp/devmanual.key
```

注意:如果把 `devmanual.key.gpg` 也公开放进仓库,那么**整个保护就取决于这个口令的强度**。别人可以拿密文离线反复猜口令,所以必须用足够长的随机口令(5 个以上随机单词)。配套脚本的 `setup.sh --wrap-key` 和 `unlock.sh` 把这两步自动化了。

## 命令速查

| 命令 | 作用 |
|---|---|
| `git-crypt init` | 在仓库里生成密钥并配置 filter |
| `git-crypt status -e` | 列出按规则会加密的文件;已进入暂存区或提交的明文会带 `WARNING` |
| `git-crypt status -u` | 列出**不**加密的文件(其他所有文件) |
| `git-crypt status -f` | 把误以明文暂存的受保护文件重新以密文暂存(**不会**清除已提交的历史) |
| `git-crypt export-key <文件>` | 导出对称密钥 |
| `git-crypt unlock [密钥文件]` | 解锁;不带参数时使用 GPG 私钥 |
| `git-crypt lock` | 重新锁定,工作区文件变回密文。工作区不干净时报错,可用 `--force` 强制(可能丢失未提交的修改) |
| `git-crypt add-gpg-user <ID>` | 用 GPG 公钥授权一个用户 |

## 配套脚本(`tools/projects-crypt/`)

| 脚本 | 作用 |
|---|---|
| `purge-history.sh DEST` | 在**新的干净克隆** `DEST` 里把 `Projects/` 从所有历史中删除,并把你当前的明文 `Projects/` 放回去(未跟踪)。原仓库不会被修改 |
| `setup.sh --key-out FILE [--wrap-key]` | 一次性设置:`git-crypt init`、导出密钥、写 `.gitattributes` 并先单独提交、加密 `Projects/`、**提交前逐个文件验证是密文**,最后提交。不会推送 |
| `verify.sh [--remote origin]` | 审计暂存区和**所有提交**里 `Projects/` 的每个版本是否都是密文;加 `--remote` 会把远端的所有分支和标签也取回来一起审计 |
| `unlock.sh [KEY \| KEY.gpg]` | 解锁。传 `.gpg` 密钥时会提示输入口令,临时解出的密钥用完即删;不带参数则用 GPG 用户模式 |

`setup.sh` 在发现历史里已有明文 `Projects/` 时会拒绝运行,并提示先用 `purge-history.sh`。每个脚本都有 `--help`。

## 已经提交过明文怎么办

git-crypt **只保护之后提交的内容**。如果文件已经以明文提交过,它仍然留在历史里,公开仓库后任何人都能 `git log` 翻出来,`git-crypt status -f` 也清除不了。必须重写历史,把它从所有提交里删掉。

先确认历史里有没有:

```bash
git log --all --oneline -- Projects
```

### 用配套脚本(推荐)

```bash
# 0. 先提交 notes/ 和脚本。purge-history.sh 要求源仓库工作区完全干净
git add notes tools/projects-crypt && git commit -m "add git-crypt notes and scripts"

# 1. 生成不含 Projects 历史的干净克隆(原仓库不动)
tools/projects-crypt/purge-history.sh ../DevelopingManual-clean

# 2. 在干净克隆里加密并审计
cd ../DevelopingManual-clean
tools/projects-crypt/setup.sh --key-out ~/secret/devmanual.key --wrap-key
tools/projects-crypt/verify.sh

# 3. 你自己推送(会改写远端历史)
git fetch origin && git push --force-with-lease origin main
git ls-remote origin                              # 远端的其他分支、标签也含旧明文,必须强推或删除
tools/projects-crypt/verify.sh --remote origin    # 审计远端实际保存的内容

# 4. 全部通过后,才把仓库改为公开
```

### 手动做法

```bash
cp -r Projects ../Projects.backup            # 1. 先备份!filter-repo 会把 Projects/ 从工作区删掉
git clone --no-local <本地仓库路径> ../repo-clean && cd ../repo-clean   # 2. 在新克隆上操作
git filter-repo --path Projects --invert-paths   # 3. 需要先安装 git-filter-repo;会移除 origin
git remote add origin <仓库地址>
# 4. 配置 git-crypt、把备份的 Projects 放回来、提交、推送
```

### 重写历史也清不掉的东西

- 远端的**其他分支和标签**:不强推或删除,旧明文仍然可达。`verify.sh --remote` 会发现它们。
- **已被别人 clone、fork 或缓存的内容**无法收回。
- GitHub 上的 `refs/pull/*`(只要开过 Pull Request)和旧提交的 SHA 链接。按 GitHub 官方的敏感数据清理文档所述,强推之后旧提交仍可能通过 SHA 访问,直到垃圾回收,要彻底清除需要联系 GitHub 支持。
- 因此,**如果这个仓库曾经以明文推送过、现在要公开,最稳妥的做法是新建一个空仓库,把干净克隆推送过去,再把新仓库设为公开**,旧仓库删除。

## 限制与注意事项

- **文件名、目录结构、文件大小、提交信息、修改历史都是公开的**,别人能看出有哪些项目、改了哪些文件。
- 加密是确定性的:相同内容得到相同密文,别人能判断两个文件是否相同、某个文件是否被修改过。实测 313 个文件只产生 306 个不同的内容对象,正是因为有内容完全相同的文件。
- 不支持更换密钥。密钥泄露后,所有历史版本都能被解开;已授权的人也无法撤销对旧内容的访问。
- GitHub 网页上看不到加密文件的预览,`.md` / `.svg` 也不会渲染。
- 密文无法压缩,仓库会变大。实测约 29 MB 的 Projects(大多是 md、svg、png)让 `.git` 从约 15 MB 增长到约 28 MB。文件内容只要改动一点,整个密文都会变,Git 无法做增量压缩,所以经常修改的大文件会让仓库持续变大。
- git-crypt 也会加密空文件(得到 22 字节的密文),不是跳过。

## 常见问题

**`git-crypt status -e` 里出现 `WARNING: staged/committed version is NOT ENCRYPTED!`。**
说明这个文件按规则应加密,但已经以明文进入了暂存区或提交。先确认 `.gitattributes` 已经提交,再用 `git-crypt status -f` 重新以密文暂存并提交。如果明文已经提交或推送过,还需要按上一节处理历史。

**clone 后文件是乱码。**
还没解锁,执行 `git-crypt unlock <密钥文件>` 或 `tools/projects-crypt/unlock.sh <密钥文件>`。

**`git-crypt lock` 报 `Working directory not clean`。**
先提交或暂存改动;确认不需要时才加 `--force`。

**别人需要密码才能下载后查看,git-crypt 够不够?**
不够直接。要用上面的"想要输入密码的体验",或者改用带密码的加密压缩包(如 `7z -mhe=on`),后者还能隐藏文件名。

**`setup.sh` 报 `already appears in earlier commits`。**
历史里已有明文。按"已经提交过明文怎么办"先用 `purge-history.sh`。只有在这个仓库从未推送、从未共享的情况下,才可以用 `--allow-plaintext-history` 跳过。

## 参考资料

- 官方仓库与 README:<https://github.com/AGWA/git-crypt>
- git-filter-repo:<https://github.com/newren/git-filter-repo>
- GitHub 文档 "Removing sensitive data from a repository"
- Git 属性与 filter:`man gitattributes`
