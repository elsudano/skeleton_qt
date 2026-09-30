#!/bin/bash
.venv/bin/pyside6-lupdate $(find main.py src -name '*.py') -no-obsolete -locations none -ts resources/translations/skeleton_es_ES.ts resources/translations/skeleton_en_US.ts
.venv/bin/pyside6-linguist resources/translations/skeleton_es_ES.ts resources/translations/skeleton_en_US.ts
.venv/bin/pyside6-lrelease -compress resources/translations/skeleton_es_ES.ts -qm resources/translations/skeleton_es_ES.qm
.venv/bin/pyside6-lrelease -compress resources/translations/skeleton_en_US.ts -qm resources/translations/skeleton_en_US.qm
.venv/bin/pyinstaller --noconfirm --clean skeleton_qt.spec
