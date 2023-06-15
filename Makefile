.PHONY: build-win
build-win:
	@echo "build-win"
	pipenv run pyinstaller -F -i logo.ico dvt_test.py --distpath win-dist