#!/bin/bash
VERSION="1.2.7"
# make distro
rm -rf build
mkdir -p build
mkdir -p sis
#cp -v utils.py build/
#cp -v xtext.py build/
cp -v default.py build/
cp -v geoinputbase.py build/
cp -v geoinput.py build/
cp -v geoinputslider.py build/
cp -v versions.py build/
cp -v utils.py build/
cp -v res/manual.html build/
TARGET=geoinput-$VERSION.sis
MERGED_TARGET=geoinput-127.sis
# create sis-filex
#ensymble.py py2sis --uid=0xe3e34da2 --appname="geinput" --shortcaption="geoinput" --version=$VERSION --vendor="Lado Kumsiashvili" --verbose build geoinput-${VERSION}.sis
ensymble.py py2sis --textfile=res/info.txt --vendor="Lado Kumsiashvili" --appname="geoinput" --uid=0x20027ad1 --caps=SwEvent --verbose --icon=res/geo_flag.svgt --version=$VERSION build sis/$TARGET
ensymble.py mergesis sis/$TARGET libs/envy-1.0.4.sis libs/keypress-1.0.6.sis libs/appswitch-1.0.3.sis libs/applist-1.0.0.sis sis/$MERGED_TARGET
rm -rf build
