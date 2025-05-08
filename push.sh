#!/usr/bin/env bash

error() {
  echo "$1"
  exit 1
}

JEKYLL="bundle exec jekyll"

ALRIGHT_THEN="$(cat ~/.alright_then)"
FTP_DEST="$(cat ~/.ftp_dest)"
TARGET="blog"

${JEKYLL} build -d "${TARGET}" || error "Build failed."

lftp -c "open ftp://cmjbteo:${ALRIGHT_THEN}@${FTP_DEST}; cd www/blog; lcd _site; mirror -R --delete" || error "Push failed."
#find "${TARGET}" -type f -exec curl -u "cmjbteo:${ALRIGHT_THEN}" --ftp-create-dirs -T {} ftp://"${FTP_DEST}"/\{\} \;

echo "Done!"
