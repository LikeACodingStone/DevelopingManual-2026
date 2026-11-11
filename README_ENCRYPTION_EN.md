# Encrypted Projects: How to Decrypt and Update

English (this file) · [中文](README_ENCRYPTION_CH.md)

The `Projects/` folder of this repository is encrypted. This page explains how to **decrypt** it (read the files) and how to **encrypt** changes (update the files). It sits at the repository root on purpose: anything inside `Projects/` is itself encrypted, so it could not be read before you have the key.

## What is and is not protected

- Everything under `Projects/` is encrypted with [git-crypt](https://github.com/AGWA/git-crypt) (AES-256). In the repository and on GitHub those files are ciphertext: the browser shows unreadable binary, and "Download ZIP" gives the same ciphertext.
- **Still visible to everyone:** file and folder names, file sizes, and the commit history. Only the contents are protected.
- Everything outside `Projects/` (topics, examples, catalog, notes) is ordinary, public text.

## Decrypt: read the files

You need three things: `git`, `git-crypt`, and the **key**. The key is not in this repository; ask the repository owner for it. It comes in one of two forms:

- a key file (`*.key`), or
- a passphrase-protected key file (`*.key.gpg`) together with its passphrase.

```bash
# 1. install git-crypt (on Windows use WSL)
sudo apt install git-crypt          # Debian / Ubuntu
brew install git-crypt              # macOS

# 2. clone the repository. It must be a real git clone: a downloaded ZIP cannot be unlocked
git clone <repository-url>
cd <repository>

# 3. unlock, using whichever key form you were given
git-crypt unlock /path/to/KEYFILE                    # plain key file
tools/projects-crypt/unlock.sh /path/to/KEYFILE.gpg  # passphrase-protected key: you type the passphrase
```

Check that it worked: the files under `Projects/` are now readable text. To lock them again, run `git-crypt lock` (the working tree must be clean).

If the owner authorised your GPG key instead, run `git-crypt unlock` with no argument.

## Encrypt: update the files (for the owner)

There is **no separate encrypt command**. git-crypt encrypts automatically on `git add`, so you edit and commit as usual. Do this in the clone that has already been unlocked:

```bash
# edit files under Projects/ as you normally would, then:
git add -A Projects            # edits, new files and deletions
git commit -m "update projects"
tools/projects-crypt/verify.sh # optional but recommended: confirms everything stored is ciphertext
git push
```

- New files created under `Projects/` are encrypted automatically.
- To protect more files, add a rule to `.gitattributes`, commit **that file first**, then add the files (use `git add --renormalize <file>` for files Git already tracks):
  ```gitattributes
  private/** filter=git-crypt diff=git-crypt        # a whole directory
  notes/diary.md filter=git-crypt diff=git-crypt    # one file
  ```
  The same key unlocks every rule. Details are in [the usage notes](notes/git-crypt-usage_EN.md).
- Check at any time: `git-crypt status -e | grep WARNING` must print nothing.

## Rules to follow

1. **Work only inside this repository's clone.** Never copy the files into a different repository and commit them there: the encryption settings live in `.git`, not in the files, so a copy is stored as **plaintext**.
2. **Never edit files while the repository is locked.** They are unreadable ciphertext; unlock first.
3. **Back up the key** in at least two places outside the repository. If it is lost, the encrypted files cannot be recovered.
4. **Before making a repository public, or after anything unusual,** run `tools/projects-crypt/verify.sh --remote origin`. It audits every file, every commit, and every branch and tag on the remote.
5. Never write a rule that matches `.gitattributes` itself (for example `*` or `**`).

## Scripts (`tools/projects-crypt/`)

| Script | Purpose |
|---|---|
| `unlock.sh [KEY or KEY.gpg]` | Unlock after cloning. With a `.gpg` key it asks for the passphrase. |
| `verify.sh [--remote origin]` | Audit that every stored version under `Projects/` is ciphertext. |
| `setup.sh --key-out FILE` | One-time setup of encryption in a repository. |
| `purge-history.sh DEST` | One-time: build a clean clone with the plaintext removed from history. |

Every script has `--help`.

## FAQ

| Problem | Cause and fix |
|---|---|
| Files under `Projects/` are unreadable garbage | The repository is locked. Unlock it as described above. |
| `not a valid git-crypt key file` | Wrong file. Use the key file the owner gave you, not another file. |
| `git-crypt: command not found` | Install git-crypt (see above). |
| I downloaded a ZIP | A ZIP cannot be unlocked. Use `git clone`. |
| `git-crypt lock` says `Working directory not clean` | Commit or stash your changes first; `--force` may lose uncommitted edits. |
| I forgot the passphrase | It cannot be recovered. Only a backup of the plain key file can unlock the repository. |
| Is anything else hidden? | No. File names, sizes and history stay public; see "What is and is not protected". |

## More

- [git-crypt usage notes](notes/git-crypt-usage_EN.md) · [中文](notes/git-crypt-usage.md): the full explanation, including GPG authorisation, adding rules, and what to do if plaintext was ever committed.
- Official project: <https://github.com/AGWA/git-crypt>
