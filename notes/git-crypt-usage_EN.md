# git-crypt Usage Notes

English (this file) · [中文](git-crypt-usage.md)

- Aliases and ecosystem: git-crypt (AGWA/git-crypt), transparent file encryption for Git
- Platforms: Linux / macOS (use WSL on Windows)
- Tags: git, encryption, repository management
- Verification status: **run and verified in throwaway repositories.** Environment: git-crypt 0.7.0 (Ubuntu 24.04 package), git 2.43.0. Verified: encryption; unlocking a fresh clone with no key, a wrong passphrase and the right passphrase; GPG-user mode; `lock`; `status`; and the companion scripts. A local bare repository served as the remote, so **nothing was tested by actually pushing to GitHub**

## What it is

git-crypt lets you **encrypt only the files or directories you choose** inside an ordinary Git repository; everything else stays public. The cipher is AES-256.

- Local working tree: plaintext once unlocked; you edit, `git add` and `git commit` as usual.
- Remote (e.g. GitHub): stores ciphertext; the browser shows binary content.

## How it works

It uses Git's `filter` mechanism together with `.gitattributes`:

1. `.gitattributes` declares which paths are encrypted.
2. On `git add`, the clean filter encrypts the file before it is written to the repository.
3. On `git checkout` / unlock, the smudge filter decrypts it into the working tree.

Every encrypted file begins with a fixed 10-byte header, `\0GITCRYPT\0`, which you can use to check that a file really is encrypted.

## Install

```bash
sudo apt install git-crypt     # Debian / Ubuntu
brew install git-crypt         # macOS
git-crypt --version
```

## Quick start (symmetric key mode)

### 1. Initialise

Run it in the repository root. It generates a random symmetric key, stored in `.git/git-crypt/keys/default`:

```bash
git-crypt init
```

### 2. Declare the paths to encrypt, and commit that **first**

```gitattributes
# .gitattributes
Projects/** filter=git-crypt diff=git-crypt
```

```bash
git add .gitattributes
git commit -m "configure git-crypt for Projects/"
```

> **Commit `.gitattributes` before adding the files to encrypt.** Otherwise the files enter the repository as plaintext.
> Make sure no rule matches `.gitattributes` itself, or it would be encrypted too.

### 3. Add the files and check

```bash
git add Projects
git commit -m "add encrypted projects"

git-crypt status -e                  # files that the rules encrypt
git-crypt status -e | grep WARNING   # must print nothing
```

If a file reached the index or a commit as plaintext, you get a warning like this:

```
    encrypted: Projects/x/oops.md *** WARNING: staged/committed version is NOT ENCRYPTED! ***
```

> Note that `git-crypt status -u` lists **every file that is not encrypted** (README, `.gitattributes`, and so on), not "files that should be encrypted but are not". It cannot be used as a check.

### 4. Check that what was committed is ciphertext

`cat-file` reads the raw stored content and does not decrypt:

```bash
git cat-file blob HEAD:Projects/E009_diagram/README.md | head -c 10 | xxd
# expected: 00 47 49 54 43 52 59 50 54 00   i.e. \0GITCRYPT\0
```

(Replace the path with a file that exists in your repository. To check every file and all of history, use `verify.sh` below.)

### 5. Export and back up the key

```bash
git-crypt export-key ~/secret/devmanual.key
```

- **Never put the key file inside the repository.**
- If you lose the key and have no GPG authorisation, the encrypted content is **unrecoverable**. Back it up in at least two separate places.

### 6. Push

```bash
git push
```

## Unlocking elsewhere

```bash
git clone git@github.com:<user>/<repo>.git
cd <repo>
# at this point every file under Projects/ is binary ciphertext
git-crypt unlock ~/secret/devmanual.key
# after unlocking they are plaintext again
```

Anyone without git-crypt or without the key gets ciphertext, whether they clone or download the ZIP. A wrong key file fails with `not a valid git-crypt key file` and the files stay ciphertext.

## Authorising several people with GPG (optional)

Instead of sharing a key file, authorise each person's own GPG public key:

```bash
git-crypt init                                       # still run init first
git-crypt add-gpg-user --trusted alice@example.com   # creates a commit automatically
git push
```

- `add-gpg-user` commits `.git-crypt/keys/default/0/<fingerprint>.gpg`, the repository key encrypted to Alice's public key.
- If that public key is not yet trusted in your GPG keyring, you need `--trusted`, otherwise the command fails.

After cloning on her own machine, Alice unlocks without arguments (using her GPG private key):

```bash
git-crypt unlock
```

## Getting a "type a password" experience

git-crypt itself has no password; unlocking relies on a key file or a GPG private key. To get close to a password prompt, encrypt the exported key file once more with a passphrase:

```bash
# encrypt the key file
gpg --symmetric --cipher-algo AES256 --output devmanual.key.gpg ~/secret/devmanual.key

# user: type the passphrase to recover the key, then unlock the repository
gpg --decrypt --output /tmp/devmanual.key devmanual.key.gpg
git-crypt unlock /tmp/devmanual.key
rm /tmp/devmanual.key
```

Note: if you also publish `devmanual.key.gpg` in the repository, **all protection then depends on the strength of that passphrase**. Anyone can take the ciphertext and guess passphrases offline indefinitely, so use a long random one (5 or more random words). The companion scripts' `setup.sh --wrap-key` and `unlock.sh` automate both steps.

## Command cheat sheet

| Command | What it does |
|---|---|
| `git-crypt init` | Generate a key in the repository and configure the filter |
| `git-crypt status -e` | List the files the rules encrypt; plaintext already staged or committed carries a `WARNING` |
| `git-crypt status -u` | List the files that are **not** encrypted (all the others) |
| `git-crypt status -f` | Re-stage protected files that were staged as plaintext, this time encrypted (does **not** remove anything already committed) |
| `git-crypt export-key <file>` | Export the symmetric key |
| `git-crypt unlock [keyfile]` | Unlock; without an argument it uses your GPG private key |
| `git-crypt lock` | Lock again so the working tree files become ciphertext. Fails if the working tree is dirty; `--force` overrides (uncommitted changes may be lost) |
| `git-crypt add-gpg-user <ID>` | Authorise a user by GPG public key |

## Companion scripts (`tools/projects-crypt/`)

| Script | What it does |
|---|---|
| `purge-history.sh DEST` | In a **new clean clone** `DEST`, removes `Projects/` from every commit and puts your current plaintext `Projects/` back (untracked). The original repository is not modified |
| `setup.sh --key-out FILE [--wrap-key]` | One-time setup: `git-crypt init`, export the key, write `.gitattributes` and commit it on its own, encrypt `Projects/`, **verify every file is ciphertext before committing**, then commit. It never pushes |
| `verify.sh [--remote origin]` | Audits the index and **all commits**: every version of every file under `Projects/` must be ciphertext. With `--remote` it also fetches every branch and tag of the remote and audits those |
| `unlock.sh [KEY \| KEY.gpg]` | Unlocks. With a `.gpg` key it prompts for the passphrase and deletes the temporarily decrypted key afterwards; without an argument it uses GPG-user mode |

`setup.sh` refuses to run when plaintext `Projects/` is already in the history, and tells you to run `purge-history.sh` first. Every script has `--help`.

## What if plaintext was already committed

git-crypt **only protects what is committed afterwards**. If a file was ever committed as plaintext, it stays in the history, anyone can dig it out with `git log` once the repository is public, and `git-crypt status -f` cannot remove it. You must rewrite history to delete it from every commit.

First check whether it is in the history:

```bash
git log --all --oneline -- Projects
```

### With the companion scripts (recommended)

```bash
# 0. Commit notes/ and the scripts first. purge-history.sh needs a completely clean source tree
git add notes tools/projects-crypt && git commit -m "add git-crypt notes and scripts"

# 1. Build a clean clone without Projects history (the original is left alone)
tools/projects-crypt/purge-history.sh ../DevelopingManual-clean

# 2. Encrypt and audit in the clean clone
cd ../DevelopingManual-clean
tools/projects-crypt/setup.sh --key-out ~/secret/devmanual.key --wrap-key
tools/projects-crypt/verify.sh

# 3. You push (this rewrites the remote history)
git fetch origin && git push --force-with-lease origin main
git ls-remote origin                              # other branches and tags still hold the old plaintext: force-push or delete them
tools/projects-crypt/verify.sh --remote origin    # audit what the remote really stores

# 4. Only when everything passes, make the repository public
```

### By hand

```bash
cp -r Projects ../Projects.backup            # 1. back up first! filter-repo deletes Projects/ from the working tree
git clone --no-local <local repo path> ../repo-clean && cd ../repo-clean   # 2. work on a fresh clone
git filter-repo --path Projects --invert-paths   # 3. needs git-filter-repo installed; it removes origin
git remote add origin <repository URL>
# 4. set up git-crypt, put the backed-up Projects back, commit, push
```

### What rewriting history cannot clean up

- **Other branches and tags** on the remote: unless you force-push or delete them, the old plaintext stays reachable. `verify.sh --remote` finds them.
- **Anything already cloned, forked or cached** by someone else cannot be taken back.
- On GitHub, `refs/pull/*` (if a pull request ever existed) and links to old commit SHAs. According to GitHub's own documentation on removing sensitive data, old commits may remain reachable by SHA after a force-push until garbage collection, and fully removing them requires contacting GitHub support.
- So, **if this repository was ever pushed with plaintext and you now want it public, the safest route is to create a new empty repository, push the clean clone there, make the new one public, and delete the old one.**

## Limitations and cautions

- **File names, directory layout, file sizes, commit messages and change history are all public.** Anyone can see which projects exist and which files changed.
- Encryption is deterministic: identical content gives identical ciphertext, so others can tell whether two files are the same or whether a file changed. In a real run, 313 files produced only 306 distinct content objects, because some files are identical.
- Key rotation is not supported. If the key leaks, every historical version can be decrypted; and someone you authorised cannot be stopped from reading old content.
- GitHub shows no preview for encrypted files, and `.md` / `.svg` are not rendered.
- Ciphertext does not compress, so the repository grows. In a real run, about 29 MB of Projects (mostly md, svg, png) took `.git` from about 15 MB to about 28 MB. Changing a file even slightly changes the whole ciphertext and Git cannot delta-compress it, so frequently edited large files keep growing the repository.
- git-crypt also encrypts empty files (they become 22-byte ciphertexts) rather than skipping them.

## FAQ

**`git-crypt status -e` shows `WARNING: staged/committed version is NOT ENCRYPTED!`.**
The file matches an encryption rule but entered the index or a commit as plaintext. Make sure `.gitattributes` is committed, then run `git-crypt status -f` to re-stage it as ciphertext and commit. If the plaintext was already committed or pushed, also handle the history as described above.

**After cloning, the files are garbage.**
You have not unlocked yet. Run `git-crypt unlock <keyfile>` or `tools/projects-crypt/unlock.sh <keyfile>`.

**`git-crypt lock` says `Working directory not clean`.**
Commit or stash your changes first; use `--force` only when you are sure you do not need them.

**Is git-crypt enough if people must enter a password after downloading?**
Not directly. Use the "type a password" approach above, or switch to a password-protected archive (such as `7z -mhe=on`), which also hides file names.

**`setup.sh` says `already appears in earlier commits`.**
The history already contains plaintext. Run `purge-history.sh` first as described in "What if plaintext was already committed". Use `--allow-plaintext-history` only when this repository was never pushed or shared.

## References

- Official repository and README: <https://github.com/AGWA/git-crypt>
- git-filter-repo: <https://github.com/newren/git-filter-repo>
- GitHub documentation, "Removing sensitive data from a repository"
- Git attributes and filters: `man gitattributes`
