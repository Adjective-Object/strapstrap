.PHONY test:
.PHONY index:

test:
	python ./strapstrapdown.py ./example/example.mkd ./example/output.html

index:
	python ./strapstrapdown.py ./index.mkd ./index.html
