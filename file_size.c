#include <stdio.h>
#include <stdlib.h>

/*
 * Simple utility to print the size (in bytes) of one or more files.
 * Usage:
 *   gcc file_size.c -o file_size
 *   ./file_size <file1> [file2 ...]
 */

/* Return the size of the given file in bytes, or -1 on error */
long get_file_size(const char *filename) {
    FILE *fp = fopen(filename, "rb");
    if (!fp) {
        perror(filename);
        return -1;
    }

    /* Seek to end to determine file length */
    if (fseek(fp, 0L, SEEK_END) != 0) {
        perror("fseek");
        fclose(fp);
        return -1;
    }

    long size = ftell(fp);
    fclose(fp);
    return size;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <file1> [file2 ...]\n", argv[0]);
        return EXIT_FAILURE;
    }

    for (int i = 1; i < argc; ++i) {
        long size = get_file_size(argv[i]);
        if (size >= 0) {
            printf("%s: %ld bytes\n", argv[i], size);
        } else {
            fprintf(stderr, "%s: unable to determine file size.\n", argv[i]);
        }
    }
    return EXIT_SUCCESS;
}