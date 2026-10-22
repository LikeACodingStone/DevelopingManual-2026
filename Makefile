.PHONY: test test-media demo

test:
	python3 tools/check_handbook.py

test-media:
	python3 tools/check_handbook.py --media

demo:
	python3 examples/pcm-read-write/pcm_demo.py --output /tmp/pcm-demo
