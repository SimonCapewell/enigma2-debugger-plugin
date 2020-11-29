#!/bin/bash
rm -rf build
mkdir -p build/usr/lib/enigma2/python/Plugins/SystemPlugins/Debugger
(cd src; find . -name \*.py | cpio -pvduma ../build/usr/lib/enigma2/python/Plugins/SystemPlugins/Debugger)
mkdir -p build/tmp/debugger-install/
#cp ez_setup.py build/tmp/debugger-install/
(cd build; tar cvzf data.tar.gz ./usr ./tmp)
(cd CONTROL; tar cvzf ../build/control.tar.gz ./*)
(cd build; echo "2.0" > debian-binary)
VERSION=`fgrep Version: CONTROL/control | sed -e 's/Version: *//'`
mkdir -p dist
rm -f dist/enigma2-plugin-extensions-debugger_${VERSION}.ipk
(cd build; ar -r ../dist/enigma2-plugin-extensions-debugger_${VERSION}.ipk ./debian-binary ./*.tar.gz)
(cd dist; ar t enigma2-plugin-extensions-debugger_${VERSION}.ipk)
(cd dist; ar t enigma2-plugin-extensions-debugger_${VERSION}.ipk)
cp dist/enigma2-plugin-extensions-debugger_${VERSION}.ipk /media/et8500/Plugins
