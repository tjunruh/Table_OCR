clean:
	rm -rf dist/

pyinstaller: clean
	pyinstaller --noconsole --onedir Code/application/main_window.py --name Table_OCR --noconfirm --clean --add-data LabelBinarizer:LabelBinarizer --add-data Model:Model

build: pyinstaller
	test -d Settings && cp -r Settings dist/Table_OCR/
