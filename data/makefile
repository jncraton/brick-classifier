all: part-classifier.onnx

part-classifier.onnx: render.py train.py
	python3 render.py
	python3 brickowl.py
	python3 train.py

clean:
	rm -rf -- */
	rm -f geckodriver.log