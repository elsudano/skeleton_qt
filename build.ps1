pyside6-lupdate (Get-ChildItem -Recurse -Filter *.py main.py, src | ForEach-Object FullName) -no-obsolete -locations none -ts resources/translations/skeleton_es_ES.ts resources/translations/skeleton_en_US.ts
pyside6-linguist resources/translations/skeleton_es_ES.ts resources/translations/skeleton_en_US.ts
pyside6-lrelease -compress resources/translations/skeleton_es_ES.ts -qm resources/translations/skeleton_es_ES.qm
pyside6-lrelease -compress resources/translations/skeleton_en_US.ts -qm resources/translations/skeleton_en_US.qm
pyinstaller --noconfirm --clean skeleton_qt.spec