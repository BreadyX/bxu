// CONSTANTS
#ifndef TABLE_SIZE
    #define TABLE_SIZE 1000
#endif
#ifndef VALUE_SIZE
    #define VALUE_SIZE 10
#endif
#ifndef KEY_SIZE
    #define KEY_SIZE   10
#endif

#define HT_ENOTFOUND -1

// STATICS
static int collisions;

// TYPES
struct Node {
    char *value;
    char *key;
    struct Node *prev;
    struct Node *next;
    // Pointer to the hash in the hash array
};
struct HashTable {
    struct Node *table[TABLE_SIZE];
    struct Node *tails[TABLE_SIZE];
    // array of the current hashes
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
unsigned long HT_hash(const unsigned char *key);
HashTable_t *HT_create();
void HT_destroy(HashTable_t *table, bool free_strings);
int HT_ins(HashTable_t *table, char *key, char *value);
int HT_del(HashTable_t *table, char *key, bool free_strings);
int HT_has(HashTable_t *table, const char *key);
Node_t *HT_get_node(HashTable_t *table, const char *key);
char *HT_get_value(HashTable_t *table, const char *key);
