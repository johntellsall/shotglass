SOURCE := ~/jsrc/shotglass/SOURCE
S_CORE := $(SOURCE)/coreutils

all:

ls:
	ls -d $(SOURCE)/*

core:
	(cd $(S_CORE); rg --files -g '!tests/')
	(cd $(S_CORE); rg --files -g '!tests/') | wc -l
	(cd $(S_CORE); rg --files -g 'src/**') | wc -l
	wc -l $(S_CORE)/src/echo.c
	wc -l $(S_CORE)/src/*.c | tail -1
	# (cd $(S_CORE); wc -l src/*.c) | sort -nr | head -10
