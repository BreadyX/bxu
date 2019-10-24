#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <assert.h>
#include <errno.h>

#define TABLE_SIZE 10
#define VALUE_SIZE 10
#define KEY_SIZE   10

#define ENOTFOUND  -1

/* STRUCTS AND TYPES */
struct Node {
    char value[VALUE_SIZE + 1];
    char key[KEY_SIZE + 1];
    struct Node* next;
};
struct HashTable {
    struct Node* table[TABLE_SIZE];
};
typedef struct Node      Node_t;
typedef struct HashTable HashTable_t;

/* FUNCTIONS PROTOTYPES */
unsigned long hash(unsigned char key[KEY_SIZE]);
HashTable_t* create_hash_table();
int insert_item(HashTable_t* table, char key[KEY_SIZE], char value[VALUE_SIZE]);
int modify_item(HashTable_t* table, char key[KEY_SIZE], char new_value[VALUE_SIZE]);
int get_item(HashTable_t* table, char key[KEY_SIZE], char* value);
int remove_item(HashTable_t* table, char key[KEY_SIZE]);
void destroy_hash_table(HashTable_t* table);

/* FUNCTION IMPLEMENTATIONS */
int main(int argc, char** argv)
{
    HashTable_t* my_table = create_hash_table();
    char value[VALUE_SIZE] = "gay";
    int ret;

    insert_item(my_table, "str1", "val");
    ret = get_item(my_table, "str1", value);
    printf("%d %s\n", ret, value);
    return 0;

    destroy_hash_table(my_table);

    return 0;
}

unsigned long hash(unsigned char* str)
{
    /* Hash the `str` string into a unsigned long. The has will have a      *
     * range of 0 - (TABLE_SIZE - 1)                                        */
    unsigned long hash = 5381;
    int c;
    while ((c = *str++)) hash = ((hash << 5) + hash) + c;
    return hash % TABLE_SIZE;
}

HashTable_t* create_hash_table()
{
    /* Create a new HashTable and return a pointer to it.                   */
    return malloc((unsigned long) sizeof(HashTable_t));
}

int insert_item(HashTable_t* table, char* key, char* value)
{
    /* Insert a new item with key `key` and value `value` into the          *
     * HashTable pointed at by `table`                                      */
    unsigned long h;
    Node_t* to_append,
            *current;
    // Sanity checks
    if (!table) {
        fprintf(stderr, "Null table passed to function\n");
        return EINVAL;
    }
    if (strlen(key) > KEY_SIZE || strlen(value) > VALUE_SIZE) {
        fprintf(stderr, "Argument too big has been passed\n");
        return EINVAL;
    }
    // Create new node
    to_append = malloc(sizeof(Node_t));
    if (!to_append) {
        fprintf(stderr, "Not enough memory for new element\n");
        return ENOMEM;
    }
    h = hash((unsigned char*) key);
    strcpy(to_append->key, key);
    strcpy(to_append->value, value);
    to_append->next = NULL;
    // Add to table
    if (!table->table[h])
        table->table[h] = to_append;
    else {
        current = table->table[h];
        while (current) {
            if (strcmp(current->key, key) == 0) {
                fprintf(stderr, "Key %s already exists", key);
                return EINVAL;
            }
            current = current->next;
        }
        current->next = to_append;
    }
    return 0;
}

int modify_item(HashTable_t* table, char* key, char* new_value)
{
    /* Modify item with key `key` in HashTable `table` by assigning to it   *
     * the new value `new_value`.                                           */
    int exists;
    char* old_value;
    // sanity checks
    if (!table) {
        fprintf(stderr, "Null table passed to function\n");
        return EINVAL;
    }
    if (strlen(key) > KEY_SIZE || strlen(new_value) > VALUE_SIZE) {
        fprintf(stderr, "Value too long has been passed\n");
        return EINVAL;
    }

    exists = get_item(table, key, old_value);
    if (exists == ENOTFOUND) {
        fprintf(stderr, "Key %s doesn't exists", key);
        return EINVAL;
    }
    memset(old_value, '\0', sizeof(char) * (VALUE_SIZE + 1));
    strcpy(old_value, new_value);
    return 0;
}

int get_item(HashTable_t* table, char* key, char* value)
{
    /* Sets `value` to a pointer to the value of the element with key `key` in
     * table `table. If nothing is found or an error has occurred, `value` is
     * left untouched.
     *
     * If `value` is a NULL pointer, the function does not modify it, acting
     * like a has() function. */
    unsigned long h;
    Node_t* current;
    // Sanity checks
    if (!table) {
        fprintf(stderr, "Null table passed to function\n");
        return EINVAL;
    }
    if (strlen(key) > KEY_SIZE) {
        fprintf(stderr, "Value too long has been passed\n");
        return EINVAL;
    }
    // Find value
    h = hash((unsigned char*) key);
    current = table->table[h];
    while (current) {
        if (strcmp(current->key, key) == 0) {
            strcpy(value, current->value);
            return 0;
        }
        current = current->next;
    }
    return ENOTFOUND;
}

int remove_item(HashTable_t* table, char* key)
{
    unsigned long h;
    Node_t *current,
           *previous = NULL;
    // Sanity checks
    if (!table) {
        fprintf(stderr, "Null table passed to function\n");
        return EINVAL;
    }
    if (strlen(key) > KEY_SIZE) {
        fprintf(stderr, "Argument too big has been passed\n");
        return EINVAL;
    }
    h = hash((unsigned char*) key);
    current = table->table[h];
    while (current) {
        if (strcmp(current->key, key) == 0) {
            if (!previous)
                table->table[h] = current->next;
            else
                previous->next = current->next;
            free(current);
            return 0;
        } else {
            previous = current;
            current = current->next;
        }
    }
    fprintf(stderr, "Key %s doesn't exist", key);
    return EINVAL;
}

void destroy_hash_table(HashTable_t* table)
{
    /* Deallocates HashTable pointed at by `table` including items inside
     * it */
    Node_t *current, *next;
    if (!table) {
        fprintf(stderr, "Trying to destroy NULL table!");
        return;
    }
    for (int i = 0; i < TABLE_SIZE; i++) {
        current = table->table[i];
        while(!current->next) {
            next = current->next;
            free(current);
            current = next;
        }
    }
    free(table);
}
