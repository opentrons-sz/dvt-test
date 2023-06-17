ReleaseVersion = "V0_1_0"

.PHONY: python3-build
python3-build:
	@echo "build"
	python3 -m pipenv run pyinstaller -F -n DevTest${ReleaseVersion} -i logo.ico  dvt_test.py --distpath release

.PHONY: python-build
python-build:
	@echo "build"
	python -m pipenv run pyinstaller -F -n DevTest${ReleaseVersion} -i logo.ico  dvt_test.py --distpath release

.PHONY: python-install
python-install:
	@echo "install pipenv"
	python -m pipenv install

.PHONY: python3-install
python3-install:
	@echo "install pipenv"
	python3 -m pipenv install

python-run:
	@echo "run"
	python -m pipenv run python dvt_test.py

python3-run:
	@echo "run"
	python3 -m pipenv run python dvt_test.py

.PHONY: git-clean
git-clean:
	@echo clean
	git rm -r --cached .
	git add .
	git commit -m "update .gitignore"
	git clean -F


