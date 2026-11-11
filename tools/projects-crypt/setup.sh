#!/usr/bin/env bash
# One-time setup: encrypt a directory (default: Projects) in this repository with git-crypt.
#
# Usage:
#   tools/projects-crypt/setup.sh --key-out FILE [--wrap-key] [--dir NAME] [--allow-plaintext-history]
#
#   --key-out FILE   where to save the exported git-crypt key. Required. Must be OUTSIDE the
#                    repository and must not exist yet. Whoever holds this file can decrypt.
#   --wrap-key       also write FILE.gpg: the key encrypted with a passphrase (gpg will prompt).
#                    This is how you get a "type a password" unlock; see unlock.sh.
#   --dir NAME       directory to encrypt (default: Projects).
#   --allow-plaintext-history
#                    continue even though NAME already appears in earlier commits. Only safe if
#                    this repository has NEVER been pushed or shared. Otherwise run
#                    purge-history.sh first.
#
# What it does, in order (it never pushes):
#   1. checks preconditions (git-crypt installed, nothing staged, no plaintext history)
#   2. git-crypt init, then exports the key (so a later failure cannot lose it)
#   3. adds "NAME/** filter=git-crypt diff=git-crypt" to .gitattributes and commits that alone
#   4. stages NAME/ through the encryption filter, verifies EVERY staged file is ciphertext,
#      and only then commits
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=common.sh
. "$HERE/common.sh"

KEY_OUT='' WRAP=0 DIR=Projects ALLOW_HISTORY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --key-out) [ $# -ge 2 ] || die "--key-out needs a value"; KEY_OUT=$2; shift 2 ;;
    --wrap-key) WRAP=1; shift ;;
    --dir) [ $# -ge 2 ] || die "--dir needs a value"; DIR=$2; shift 2 ;;
    --allow-plaintext-history) ALLOW_HISTORY=1; shift ;;
    -h|--help) sed -n '2,/^set -e/p' "$0" | sed '$d' | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) die "unknown argument: $1 (try --help)" ;;
  esac
done

need_cmd git "Install git."
need_cmd git-crypt "Install it first, e.g. 'sudo apt install git-crypt'."
[ "$WRAP" -eq 0 ] || need_cmd gpg "Needed for --wrap-key, e.g. 'sudo apt install gnupg'."
[ -n "$KEY_OUT" ] || die "--key-out FILE is required (see --help)"
DIR=${DIR%/}
check_dir_name "$DIR"

ROOT=$(repo_root)
cd "$ROOT"
[ -d "$DIR" ] || die "directory '$DIR' not found in $ROOT"

KEY_ABS=$(realpath -m -- "$KEY_OUT")
case "$KEY_ABS" in
  "$ROOT"|"$ROOT"/*) die "the key must be stored outside the repository (got $KEY_ABS)" ;;
esac
[ ! -e "$KEY_ABS" ] || die "$KEY_ABS already exists; remove it or pick another --key-out"
if [ "$WRAP" -eq 1 ] && [ -e "$KEY_ABS.gpg" ]; then die "$KEY_ABS.gpg already exists"; fi

git diff --cached --quiet || die "there are staged changes; commit or unstage them first"

INITIALIZED=0
[ -f "$(git rev-parse --git-path git-crypt/keys/default)" ] && INITIALIZED=1

if [ "$INITIALIZED" -eq 0 ] && [ -n "$(git rev-list --all --max-count=1 -- "$DIR")" ]; then
  if [ "$ALLOW_HISTORY" -eq 1 ]; then
    warn "'$DIR' is already in the git history in PLAINTEXT. Do not publish this repository."
  else
    die "'$DIR' already appears in earlier commits, which would stay readable in the history.
       Run tools/projects-crypt/purge-history.sh first (it builds a clean clone), then run this
       script there. Use --allow-plaintext-history only if this repo was never pushed or shared."
  fi
fi

# 1. init + key export
if [ "$INITIALIZED" -eq 0 ]; then
  info "git-crypt init"
  git-crypt init
else
  info "git-crypt already initialised, reusing its key"
fi

info "Exporting key -> $KEY_ABS"
mkdir -p "$(dirname "$KEY_ABS")"
( umask 077; git-crypt export-key "$KEY_ABS" )
if [ "$WRAP" -eq 1 ]; then
  info "Protecting the key with a passphrase -> $KEY_ABS.gpg (gpg will prompt; use a long random one)"
  ( umask 077; gpg --symmetric --cipher-algo AES256 --output "$KEY_ABS.gpg" "$KEY_ABS" )
fi

# 2. .gitattributes (must be committed BEFORE the files, and must not match itself)
RULE="$DIR/** filter=git-crypt diff=git-crypt"
touch .gitattributes
if ! grep -qxF "$RULE" .gitattributes; then
  if [ -s .gitattributes ] && [ -n "$(tail -c 1 .gitattributes)" ]; then echo >> .gitattributes; fi
  printf '%s\n' "$RULE" >> .gitattributes
fi
case "$(git check-attr filter -- .gitattributes)" in
  *unspecified) ;;
  *) die ".gitattributes would itself be encrypted; fix the rules in .gitattributes" ;;
esac
git add .gitattributes
if ! git diff --cached --quiet -- .gitattributes; then
  info "Committing .gitattributes"
  git commit -q -m "Configure git-crypt for $DIR/" -- .gitattributes
fi

# 3. encrypt: stage new files, and re-stage already tracked ones through the filter
info "Encrypting $DIR/"
git add -- "$DIR"
git add --renormalize -- "$DIR"

# 4. verify every staged file is ciphertext BEFORE committing
n=0 bad=0
while IFS= read -r -d '' rec; do
  rest=${rec#* }; sha=${rest%% *}; path=${rec#*$'\t'}
  n=$((n + 1))
  if ! is_cipher_blob "$sha"; then bad=$((bad + 1)); warn "not encrypted: $path"; fi
done < <(git ls-files -s -z -- "$DIR")
[ "$n" -gt 0 ] || die "no files found under $DIR"
if [ "$bad" -ne 0 ]; then
  git reset -q -- "$DIR"
  die "$bad of $n files were not encrypted; unstaged them and committed nothing"
fi

if git diff --cached --quiet; then
  info "Nothing new to commit ($n files already encrypted)"
else
  git commit -q -m "Encrypt $DIR/ with git-crypt"
  info "Committed $n encrypted files"
fi

cat <<EOF

Done. Every file under $DIR/ is stored as ciphertext. Your working copy stays readable.

  Key file : $KEY_ABS$( [ "$WRAP" -eq 1 ] && printf '\n  Wrapped  : %s.gpg  (passphrase-protected copy)' "$KEY_ABS" )
  BACK UP THE KEY OUTSIDE THIS REPOSITORY, in at least two places.
  Without it (or the passphrase) the encrypted files cannot be recovered.

Next (nothing has been pushed):
  tools/projects-crypt/verify.sh     # audit the whole history for plaintext
  git log --stat | head -40          # look at what will be published
  git push ...                       # when you are satisfied; a rewritten history needs --force-with-lease
  tools/projects-crypt/verify.sh --remote origin   # after pushing: check the remote's branches and
                                                   # tags too, BEFORE making the repository public
EOF
