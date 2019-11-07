#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <errno.h>
#include <time.h>

// CONSTATS
#ifndef TABLE_SIZE
    #define TABLE_SIZE 1000
#endif
#ifndef VALUE_SIZE
    #define VALUE_SIZE 10
#endif
#ifndef KEY_SIZE
    #define KEY_SIZE   10
#endif

// STATICS
static int collisions;

// TYPES
struct Node {
    char value[VALUE_SIZE + 1];
    char key[KEY_SIZE + 1];
    struct Node* next;
};
struct HashTable {
    struct Node* table[TABLE_SIZE];
    struct Node* tails[TABLE_SIZE];
};
typedef struct Node      Node_t;
typedef struct HashTable HashTable_t;

// FUNCTIONS
#if (defined(HT_DEBUG) && HT_DEBUG != 0)
    #define perr(...) fprintf(stderr, __VA_ARGS__)
    #define pdebug(...) fprintf(stdout, __VA_ARGS__)
    #define log_coll() do { \
        fprintf(stdout, "Debug: hash collision\n"); collisions++;} while (0)
#else
    #define perr(...) ;
    #define pdebug(...) ;
    #define log_coll() collisions++
#endif
unsigned long HT_hash(const unsigned char key[KEY_SIZE]);
HashTable_t *HT_create();
void HT_destroy(HashTable_t *table);
int HT_ins(HashTable_t *table, const char key[KEY_SIZE],
           const char value[VALUE_SIZE]);
// HT_del
int HT_has(HashTable_t *table, const char key[KEY_SIZE]);
// HT_get

unsigned long HT_hash(const unsigned char str[])
{
    /* Hash `str` into a unsigned long. The has will have a
     * range of 0 - (TABLE_SIZE - 1). */
    unsigned long hash = 5381;
    int c;
    while ((c = *(str++)))
        hash = ((hash << 5) + hash) + c;
    return hash % TABLE_SIZE;
}

HashTable_t* HT_create()
{
    /* Create a new HashTable and return a pointer to it.
     *
     * Each item of the HashTable is a key-value pair that contains
     * KEY_SIZE and VALUE_SIZE chars for key and value respectively
     * EXCLUDING the null terminator (key[KEY_SIZE + 1],
     * value[VALUE_SIZE + 1]).
     */
    return malloc((unsigned long) sizeof(HashTable_t));
}

void HT_destroy(HashTable_t* table)
{
    /* Deallocates HashTable pointed at by `table` including items inside
     * it */
    Node_t *current, *next;
    if (!table) {
        perr("Trying to destroy NULL table!");
        return;
    }
    for (int i = 0; i < TABLE_SIZE; i++) {
        current = table->table[i];
        while(current) {
            next = current->next;
            free(current);
            current = next;
        }
    }
    free(table);
}

int HT_ins(HashTable_t *table, const char key[], const char value[])
{
    /* Insert a new item with key `key` and value `value` into the HashTable
     * pointed at by `table`.
     * Note 1: `key` and `value` are copied into the element. They can be safely
     *         deallocated by external logic.
     * Note 2: if `key` and `value` exceed KEY_SIZE + 1 and VALUE_SIZE + 1
     *         respectively, truncation will take place. If different sizes are
     *         needed, override the aforemetioned macros before usage.
     */
    unsigned long h;
    Node_t *to_append;

    if (!table) {
        perr("Null table passed to function\n");
        return EINVAL;
    }
    // Create new node
    to_append = malloc(sizeof(Node_t));
    if (!to_append) {
        perr("Not enough memory for new element\n");
        return ENOMEM;
    }
    strncpy(to_append->key, key, (KEY_SIZE + 1) * sizeof(char));
    strncpy(to_append->value, value, (VALUE_SIZE + 1) * sizeof(char));
    to_append->key[KEY_SIZE] = '\0';
    to_append->value[VALUE_SIZE] = '\0';
    // Compute hash
    h = HT_hash((unsigned char*) to_append->key);
    // Add item if not already present
    if (HT_has(table, to_append->key) != 0) {
        if (!table->table[h]) {
            table->table[h] = to_append;
            table->tails[h] = to_append;
        } else {
            table->tails[h]->next = to_append;
            table->tails[h] = to_append;
        }
        return 0;
    } else {
        perr("Item with key %s already present\n", to_append->key);
        free(to_append);
        return EINVAL;
    }
}

int HT_del(HashTable_t *table, const char key[])
{
    return 0;
}

int HT_has(HashTable_t *table, const char key[])
{
    /* Check if key `key` is present in HashTable `table`. If present return 0,
     * else return -1.
     * Note: if `key` is bigger than KEY_SIZE + 1, then it will be truncated.
     */
    char san_key[KEY_SIZE + 1];
    unsigned long h;
    Node_t *current;
    // Sanitize
    strncpy(san_key, key, (KEY_SIZE + 1) * sizeof(char));
    san_key[KEY_SIZE] = '\0';
    // Search
    h = HT_hash((unsigned char*) san_key);
    current = table->table[h];
    while (current) {
        if (strcmp(current->key, san_key) == 0)
            return 0;
        current = current->next;
    }
    return -1;
}

int main(void) { HT_create(); return 0; }
