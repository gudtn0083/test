#ifndef KEYBOARD_H
#define KEYBOARD_H

#include <stdbool.h>

/* Maximum number of keys on a standard 104-key keyboard */
#define MAX_KEYS 104

/* Representation of an individual key */
typedef struct {
    char label[8];          /* Key cap label, e.g., "A", "Enter" */
    int  row;               /* Physical row index (0-based) */
    int  col;               /* Physical column index (0-based) */

    unsigned short scanCode;/* Hardware/firmware scan code */
    bool isModifier;        /* Modifier key? (Shift, Ctrl, Alt …) */
    bool isToggled;         /* Toggle state (CapsLock, NumLock …) */
} Key;

/* Representation of an entire keyboard */
typedef struct {
    int totalKeys;          /* Actual number of populated keys */
    Key keys[MAX_KEYS];     /* Flat array of all keys */

    /* Global toggle states */
    bool numLock;
    bool capsLock;
    bool scrollLock;

    /* Optional vendor/model identification */
    char vendor[32];
    char model[32];
} Keyboard;

#endif /* KEYBOARD_H */