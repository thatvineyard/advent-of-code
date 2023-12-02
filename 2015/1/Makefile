PY = python 

test:floor.py
	ifeq (python floor.py "(())", 0)
		@echo "PASSED"
	else
		@echo "(()) FAILED"
	ifeq (python floor.py ()(), 0)
		@echo "PASSED"
	else
		@echo "()() FAILED"
	ifeq (python floor.py (((, 3)
		@echo "PASSED"
	else
		@echo "((( FAILED"
	ifeq (python floor.py (()(()(, 3)
		@echo "PASSED"
	else
		@echo "(()(()( FAILED"
	ifeq (python floor.py ))(((((, 3)
		@echo "PASSED"
	else
		@echo "))((((( FAILED"
	ifeq (python floor.py ()), -1)
		@echo "PASSED"
	else
		@echo "()) FAILED"
	ifeq (python floor.py ))(, -1)
		@echo "PASSED"
	else
		@echo "))( FAILED"
	ifeq (python floor.py ))), -3)
		@echo "PASSED"
	else
		@echo "))) FAILED"
	ifeq (python floor.py )())()), -3)
		@echo "PASSED"
	else
		@echo ")())()) FAILED"
