PYTHON=python3
TIMED_PYTHON=time $(PYTHON)

tiny-data:
	$(PYTHON) ./gen-mat.py --rows=12 --cols=12 a.data
	$(PYTHON) ./gen-mat.py --rows=12 --cols=12 b.data

small-data:
	$(PYTHON) ./gen-mat.py --rows=120 --cols=120 a.data
	$(PYTHON) ./gen-mat.py --rows=120 --cols=120 b.data

medium-data:
	$(TIMED_PYTHON) ./gen-mat.py --rows=1200 --cols=120 a.data
	$(TIMED_PYTHON) ./gen-mat.py --rows=1200 --cols=120 b.data

large-data:
	$(TIMED_PYTHON) ./gen-mat.py --rows=12000 --cols=1200 a.data
	$(TIMED_PYTHON) ./gen-mat.py --rows=12000 --cols=1200 b.data

test-seq:
	$(PYTHON) ./mat-add.py a.data b.data c.data

test-mpi:
	mpiexec --np 4 python3 ./mpi-mat-add.py a.data b.data c.data

handout:
	mkdir -p handout
	cp Makefile *.py *.txt handout
	rm handout/mat-add-mpi.py
	tar zcvf handout.tar.gz handout

clean:
	$(RM) ?.data
	$(RM) -r __pycache__
	$(RM) -r handout.tar.gz handout
