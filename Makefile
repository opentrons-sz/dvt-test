.PHONY: build-win
build-win:
	@echo "build-win"
	python -m pipenv run pyinstaller -F -i logo.ico dvt_test.py --distpath win-dist

.PHONY: build-app
build-app:
	@echo "build-app"
	python -m pipenv run py2applet --make-setup baba.py

.PHONY: install
install:
	@echo "install pipenv"
	python -m pipenv install