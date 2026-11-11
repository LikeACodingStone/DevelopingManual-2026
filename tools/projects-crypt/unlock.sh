#!/usr/bin/env bash
# Unlock the encrypted directory after cloning, so the files become readable.
#
# Usage:
#   tools/projects-crypt/unlock.sh KEYFILE        # raw git-crypt key
#   tools/projects-crypt/unlock.sh KEYFILE.gpg    # passphrase-protected key: you type the password
#   tools/projects-crypt/unlock.sh                # GPG-user mode (your GPG private key was authorised)
#
# For the *.gpg form the key is decrypted to a private temporary file that is deleted right after.
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=common.sh
. "$HERE/common.sh"

case "${1:-}" in -h|--help) sed -n '2,/^set -e/p' "$0" | sed '$d' | sed 's/^# \{0,1\}//'; exit 0 ;; esac
[ $# -le 1 ] || die "at most one argument (try --help)"

need_cmd git "Install git."
need_cmd git-crypt "Install it first, e.g. 'sudo apt install git-crypt'."
cd "$(repo_root)"

if [ $# -eq 0 ]; then
  info "git-crypt unlock (GPG user mode)"
  git-crypt unlock
else
  KEY=$1
  [ -f "$KEY" ] || die "no such file: $KEY"
  case "$KEY" in
    *.gpg)
      need_cmd gpg "Needed to open a passphrase-protected key."
      umask 077
      TMP=$(mktemp)
      trap 'rm -f "$TMP"' EXIT
      info "Decrypting $KEY (gpg asks for the passphrase)"
      gpg --quiet --yes --decrypt --output "$TMP" "$KEY"
      info "git-crypt unlock"
      git-crypt unlock "$TMP"
      ;;
    *)
      info "git-crypt unlock"
      git-crypt unlock "$KEY"
      ;;
  esac
fi
info "Unlocked. The encrypted files are now readable in the working tree."
