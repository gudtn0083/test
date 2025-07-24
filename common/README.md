Animal Image Classifier in C
=================================

This is a very small example project that shows how you could classify simple
animal pictures (cat / dog / bird / …) by color–histogram similarity using the
k-nearest-neighbour (k-NN) algorithm.

Limitations
-----------
* The program only understands binary PPM (``.ppm`` *P6*) images.  Use a tool
  such as ImageMagick to convert other formats, e.g. ``convert foo.jpg foo.ppm``.
* The approach is *very* naïve.  Accuracy depends heavily on how you prepare the
  training images.

Building
--------
```bash
# inside the workspace root
cc -std=c99 -Wall -O2 -lm -o animal_classifier \
   main.c dataset.c image.c feature.c classifier.c
```

Running
-------
```
./animal_classifier <dataset_dir> <image.ppm>
```
* ``dataset_dir`` must contain one sub-directory **per label** (e.g. ``cat``,
  ``dog`` …).  Each sub-directory should hold a couple of ``.ppm`` example
  images of that animal.
* ``<image.ppm>`` is the picture you want to classify.