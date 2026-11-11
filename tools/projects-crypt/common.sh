#!/usr/bin/env bash
# Shared helpers for the projects-crypt scripts. Sourced by them, not run directly.

die()  { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
info() { printf '==> %s\n' "$*"; }
warn() { printf 'WARNING: %s\n' "$*" >&2; }

# need_cmd <command> <hint>
need_cmd() { command -v "$1" >/dev/null 2>&1 || die "'$1' not found. $2"; }

# Print the top-level directory of the repository containing the current directory.
repo_root() { git rev-parse --show-toplevel 2>/dev/null || die "not inside a git repository"; }

# The 10-byte header of every file git-crypt encrypts: \0 G I T C R Y P T \0
GITCRYPT_MAGIC='00474954435259505400'

# is_cipher_blob <git object>
# Succeeds when the blob is git-crypt ciphertext. A truly empty blob also succeeds:
# it carries no content, so there is nothing to leak.
is_cipher_blob() {
  local obj=$1 size head
  size=$(git cat-file -s "$obj") || return 2
  [ "$size" -eq 0 ] && return 0
  # '|| true': head closes the pipe early on big files, which would otherwise
  # trip 'set -o pipefail' in the callers.
  head=$(git cat-file blob "$obj" 2>/dev/null | head -c 10 | od -An -tx1 | tr -d ' \n') || true
  [ "$head" = "$GITCRYPT_MAGIC" ]
}

# check_dir_name <name>: the encrypted directory must be a plain relative path.
check_dir_name() {
  case "$1" in
    ''|.|/*|..|../*|*/..|*/../*) die "invalid directory name: '$1' (use a relative path such as Projects)" ;;
  esac
}
