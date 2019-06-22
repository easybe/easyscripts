#!/bin/sh
# Generate an SVN-compatible diff against the tip of the tracking branch
#
# usage: git-svn-diff [git-diff-args] > an-svn.patch

TRACKING_BRANCH=$(git config --get svn-remote.svn.fetch | sed -e 's/.*:refs\/remotes\///')
SVN_REV=$(git svn info | grep 'Last Changed Rev:' | sed -E 's/^.*: ([[:digit:]]*)/\1/')
ARGS=$(git rev-list --date-order --max-count=1 $TRACKING_BRANCH)
[ $# -gt 0 ] && ARGS="$@"

git diff --no-prefix $ARGS |
sed -e "/--- \/dev\/null/{ N; s|^--- /dev/null\n+++ \(.*\)|--- \1	(revision 0)\n+++ \1	(working copy)|;}" \
    -e "s/^--- .*/&	(revision $SVN_REV)/" \
    -e "s/^+++ .*/&	(working copy)/" \
    -e "s/^\(@@.*@@\).*/\1/" \
    -e "s/^diff --git [^[:space:]]*/Index:/" \
    -e "s/^index.*/===================================================================/" \
    -e "/^new file mode [0-9]\+$/d" \
    --binary
