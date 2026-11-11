#!/usr/bin/env bash
# Audit: is every version of every file under NAME/ (default: Projects) stored as git-crypt
# ciphertext, in the index and in ALL commits reachable from any ref? Run it before you make
# the repository public. Exit status 0 = clean, 1 = plaintext found or rule missing.
#
# Usage: tools/projects-crypt/verify.sh [--dir NAME] [--remote NAME]
#
#   --remote NAME  also fetch EVERY branch and tag of that remote (read-only, into temporary
#                  refs that are removed again) and audit them. Use this after pushing: a branch
#                  or tag you forgot on the remote keeps the old plaintext reachable. GitHub's
#                  hidden refs/pull/* refs cannot be audited or removed this way.
#
# This only inspects NAME/. It says nothing about the rest of the repository.
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=common.sh
. "$HERE/common.sh"

DIR=Projects REMOTE=''
while [ $# -gt 0 ]; do
  case "$1" in
    --dir) [ $# -ge 2 ] || die "--dir needs a value"; DIR=$2; shift 2 ;;
    --remote) [ $# -ge 2 ] || die "--remote needs a value"; REMOTE=$2; shift 2 ;;
    -h|--help) sed -n '2,/^set -e/p' "$0" | sed '$d' | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) die "unknown argument: $1 (try --help)" ;;
  esac
done
need_cmd git "Install git."
DIR=${DIR%/}
check_dir_name "$DIR"
cd "$(repo_root)"

fail=0

if [ -n "$REMOTE" ]; then
  cleanup_remote_refs() { git for-each-ref --format='delete %(refname)' refs/verify-remote | git update-ref --stdin; }
  trap cleanup_remote_refs EXIT
  info "Fetching all branches and tags of '$REMOTE' into temporary refs"
  git fetch --quiet --no-tags "$REMOTE" \
    '+refs/heads/*:refs/verify-remote/heads/*' '+refs/tags/*:refs/verify-remote/tags/*'
  info "remote refs audited: $(git for-each-ref --format='%(refname:strip=3)' refs/verify-remote | tr '\n' ' ')"
fi

# 1. the rule must be committed, otherwise new files would be added in plaintext
if git cat-file -e HEAD:.gitattributes 2>/dev/null &&
   git show HEAD:.gitattributes | grep -qxF "$DIR/** filter=git-crypt diff=git-crypt"; then
  info "rule present in HEAD:.gitattributes"
else
  warn "HEAD:.gitattributes has no '$DIR/** filter=git-crypt diff=git-crypt' rule (run setup.sh)"
  fail=1
fi

# 2. every distinct blob under DIR, in the index and in every commit
declare -A seen=()
total=0 bad=0

audit_blob() {   # audit_blob <sha> <label>
  local sha=$1 label=$2
  [ -z "${seen[$sha]+x}" ] || return 0
  seen[$sha]=1
  total=$((total + 1))
  if ! is_cipher_blob "$sha"; then
    bad=$((bad + 1))
    [ "$bad" -gt 20 ] || printf 'PLAINTEXT  %s  %s\n' "${sha:0:10}" "$label"
  fi
}

while IFS= read -r -d '' rec; do        # index: "mode sha stage<TAB>path"
  rest=${rec#* }; sha=${rest%% *}; path=${rec#*$'\t'}
  audit_blob "$sha" "index:$path"
done < <(git ls-files -s -z -- "$DIR")

while IFS= read -r commit; do           # history: "mode type sha<TAB>path"
  while IFS= read -r -d '' rec; do
    meta=${rec%%$'\t'*}; path=${rec#*$'\t'}
    rest=${meta#* }; type=${rest%% *}; sha=${rest##* }
    [ "$type" = blob ] || continue
    audit_blob "$sha" "${commit:0:7}:$path"
  done < <(git ls-tree -r -z "$commit" -- "$DIR")
done < <(git rev-list --all -- "$DIR")

if [ "$bad" -gt 20 ]; then warn "... and $((bad - 20)) more plaintext blobs not listed"; fi
if [ "$bad" -ne 0 ]; then
  warn "$bad of $total distinct blobs under $DIR/ are NOT encrypted"
  fail=1
fi

if [ "$fail" -eq 0 ]; then
  if [ "$total" -eq 0 ]; then
    warn "found no files under $DIR/ at all; is the directory name right?"
    exit 1
  fi
  info "OK: all $total distinct blobs under $DIR/ (index + all history) are git-crypt ciphertext"
  info "Reminder: this checks only $DIR/. File names, directory layout and commit messages stay public."
  exit 0
fi
exit 1
