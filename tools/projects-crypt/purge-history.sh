#!/usr/bin/env bash
# Build a CLEAN clone of this repository in which NAME/ (default: Projects) has never existed
# in any commit, and put your current plaintext NAME/ back next to it as untracked files.
# The original repository is not modified. Run setup.sh in the clean clone afterwards.
#
# Usage: tools/projects-crypt/purge-history.sh [--src DIR] [--dir NAME] DEST
#
#   DEST       new directory for the clean clone (must not exist yet).
#   --src DIR  repository to clean (default: the repository you are in).
#   --dir NAME directory to remove from history (default: Projects).
#
# Requirements: git-filter-repo, and a completely clean working tree in the source
# (commit everything first: files that are not committed are NOT carried to DEST).
#
# Afterwards:
#   cd DEST
#   tools/projects-crypt/setup.sh --key-out ~/secret/devmanual.key --wrap-key
#   tools/projects-crypt/verify.sh
#   git fetch origin && git push --force-with-lease origin main     # YOU run this; it rewrites
#                                                                    # the remote history
#   git ls-remote origin                                  # every OTHER branch/tag still holds
#                                                         # the old plaintext: force-push or delete it
#   tools/projects-crypt/verify.sh --remote origin        # then audit what the remote really has
# History is rewritten, so all commit IDs change. All branches of SRC come along as local
# branches; commits that only touched NAME/ disappear. Anything that was already cloned, forked
# or cached from the old remote keeps the plaintext, and so do GitHub's refs/pull/* if any pull
# request ever existed. For the strongest result push the clean clone to a NEW repository.
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=common.sh
. "$HERE/common.sh"

SRC='' DIR=Projects DEST=''
while [ $# -gt 0 ]; do
  case "$1" in
    --src) [ $# -ge 2 ] || die "--src needs a value"; SRC=$2; shift 2 ;;
    --dir) [ $# -ge 2 ] || die "--dir needs a value"; DIR=$2; shift 2 ;;
    -h|--help) sed -n '2,/^set -e/p' "$0" | sed '$d' | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) die "unknown argument: $1 (try --help)" ;;
    *) [ -z "$DEST" ] || die "only one DEST allowed"; DEST=$1; shift ;;
  esac
done

need_cmd git "Install git."
need_cmd git-filter-repo "Install it, e.g. 'sudo apt install git-filter-repo' or 'pip install git-filter-repo'."
[ -n "$DEST" ] || die "DEST is required (see --help)"
DIR=${DIR%/}
check_dir_name "$DIR"

if [ -z "$SRC" ]; then SRC=$(repo_root); fi
SRC=$(cd "$SRC" && git rev-parse --show-toplevel 2>/dev/null) || die "--src is not a git repository"
[ -d "$SRC/$DIR" ] || die "'$DIR' not found in $SRC"
DEST=$(realpath -m -- "$DEST")
[ ! -e "$DEST" ] || die "$DEST already exists; choose a new directory"
case "$DEST" in "$SRC"|"$SRC"/*) die "DEST must be outside the source repository" ;; esac

[ -z "$(git -C "$SRC" status --porcelain --untracked-files=all)" ] ||
  die "the source working tree is not clean. Commit (or remove) everything first, e.g.
       git add notes tools/projects-crypt && git commit -m 'add git-crypt notes and scripts'
       Anything uncommitted would be missing from the clean clone."

ORIGIN_URL=$(git -C "$SRC" remote get-url origin 2>/dev/null || true)
touched=$(git -C "$SRC" rev-list --all --count -- "$DIR")
info "$DIR/ is touched by $touched commit(s) in $SRC; removing it from every commit"

git clone --quiet --no-local "$SRC" "$DEST"
git -C "$DEST" filter-repo --quiet --path "$DIR" --invert-paths

if [ -n "$(git -C "$DEST" rev-list --all --max-count=1 -- "$DIR")" ]; then
  die "'$DIR' is still reachable in $DEST after filtering; do not use it"
fi

info "Restoring your current $DIR/ as untracked files"
cp -a -- "$SRC/$DIR" "$DEST/$DIR"

# filter-repo drops the origin remote on purpose; put the real one back (nothing is pushed).
if [ -n "$ORIGIN_URL" ]; then
  git -C "$DEST" remote add origin "$ORIGIN_URL"
  info "origin -> $ORIGIN_URL (not fetched, not pushed)"
fi

cat <<EOF

Clean clone ready: $DEST
  history without $DIR/ : $(git -C "$DEST" rev-list --all --count) commit(s)
  plaintext $DIR/       : present in the working tree, untracked

Next:
  cd "$DEST"
  tools/projects-crypt/setup.sh --key-out ~/secret/devmanual.key --wrap-key
  tools/projects-crypt/verify.sh
  # push yourself, then: tools/projects-crypt/verify.sh --remote origin
EOF
