#ifndef IMAGE_H
#define IMAGE_H

unsigned char *load_image_rgb(const char *filename, int *w, int *h);
void           free_image(unsigned char *data);

#endif // IMAGE_H