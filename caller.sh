#!/usr/bin/env bash

SCRIPT=`realpath -s $0`
SCRIPTPATH=`dirname $SCRIPT`

cd $SCRIPTPATH
uv run pdfmanip.py "$@"
