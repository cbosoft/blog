#!/usr/bin/env bash

ALRIGHT_THEN="$(cat ~/.alright_then)"
FTP_DEST="$(cat ~/.ftp_dest)"
TARGET="blog"

jekyll build -d "${TARGET}" || exit 1

find "${TARGET}" -type f -exec curl -u "cmjbteo:${ALRIGHT_THEN}" --ftp-create-dirs -T {} ftp://"${FTP_DEST}"/\{\} \;
