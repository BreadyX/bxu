#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <errno.h>
#include "./ht.h"

unsigned long HT_hash(const unsigned char *str)
{
    /* Hash `str` into a unsigned long. The hash will have a
     * range of 0 - (TABLE_SIZE - 1). */
    unsigned long hash = 5381;
    int c;
    while ((c = *(str++)))
        hash = ((hash << 5) + hash) + c;
    return hash % TABLE_SIZE;
}

HashTable_t *HT_create()
{
    /* Create a new HashTable and return a pointer to it. */
    return malloc((unsigned long) sizeof(HashTable_t));
}

void HT_destroy(HashTable_t *table, bool free_strings)
{
    /* Deallocates HashTable pointed at by `table` including items inside
     * it. If `free_strings` is flag is true, then also free the strings in each
     * item.
     *
     * Note 1: if `free_strings` is true and one of the strings pointed at by
     *  one of elements in the HashTable is not allocated in heap the program
     *  WILL crash (free() error).
     */
    Node_t *current, *next;
    if (!table) {
        perr("Trying to destroy NULL table!\n");
        return;
    }
    for (int i = 0; i < TABLE_SIZE; i++) {
        current = table->table[i];
        while(current) {
            next = current->next;
            if (free_strings) {
                free(current->key);
                free(current->value);
            }
            free(current);
            current = next;
        }
    }
    free(table);
}

int HT_ins(HashTable_t *table, char *key, char *value)
{
    /* Insert a new item with key `key` and value `value` into the HashTable
     * pointed at by `table`.
     *
     * Note 1: `key` and `value` must be null-terminated strings allocated in
     *  heap. Deallocating them before removing them from the HashTable will
     *  lead to undefined behaviour.
     */
    unsigned long h;
    Node_t *to_append;
    if (!table) {
        perr("Null table passed to function\n");
        return EINVAL;
    }
    if (!key || !value) {
        perr("Null key/value passed to function\n");
        return EINVAL;
    }
    // Create new node
    to_append = malloc(sizeof(Node_t));
    if (!to_append) {
        perr("Not enough memory for new element\n");
        return ENOMEM;
    }
    to_append->key = key;
    to_append->value = value;
    // Add item if not already present
    if (HT_has(table, to_append->key) != 0) {
        h = HT_hash((unsigned char*) to_append->key);
        if (!table->table[h]) {
            table->table[h] = to_append;
            table->tails[h] = to_append;
        } else {
            table->tails[h]->next = to_append;
            to_append->prev = table->tails[h];
            table->tails[h] = to_append;
        }
        return 0;
    } else {
        perr("Item with key %s already present\n", to_append->key);
        free(to_append);
        return EINVAL;
    }
}

int HT_del(HashTable_t *table, char *key, bool free_strings)
{
    /* Delete item with key `key` from `table`. If `free_strings` is true, then
     * the strings pointed at by the item will also be freed, otherwise they are
     * left untouched.
     *
     * Note 1: passing `free_strings` during removal of an item which points to
     *  strings not allocated in heap will cause an error (free() error).
     */
    Node_t *to_del;
    unsigned long h;
    if (!table) {
        perr("Null table passed to function\n");
        return EINVAL;
    }
    if (!key) {
        perr("Null key passed to function\n");
        return EINVAL;
    }
    to_del = HT_get_node(table, key);
    if (!to_del) {
        pdebug("Passed key not in HashTable\n");
        return HT_ENOTFOUND;
    }
    if (free_strings) {
        free(to_del->key);
        free(to_del->value);
    }
    if (to_del->prev)
        to_del->prev->next = to_del->next;
    else
        table->table[h] = to_del->next;
    free(to_del);
    return 0;
}

int HT_has(HashTable_t *table, const char *key)
{
    /* Check if key `key` is present in HashTable `table`. If present return 0,
     * else return a negative number.
     */
    Node_t *found = HT_get_node(table, key);
    if (!found)
        return -1;
    return 0;
}

Node_t *HT_get_node(HashTable_t *table, const char *key)
{
    /* Return a poitner to Node in the HashTable with key `key`.
     * If no match is found, NULL is returned.
     */
    unsigned long h;
    Node_t *current;
    // Search
    if (!key) {
        perr("Null key passed to function");
        return NULL;
    }
    h = HT_hash((unsigned char*) key);
    current = table->table[h];
    while (current) {
        /* if (strcmp(current->key, key) == 0) */
        if (current->key == key)
            return current;
        current = current->next;
    }
    return NULL;
}

char *HT_get_value(HashTable_t *table, const char *key)
{
    /* Return a pointer to value of the item in the HashTable with key `key`.
     * If no match is found, NULL is returned.
     */
    Node_t *found = HT_get_node(table, key);
    if (!found)
        return NULL;
    return found->value;
}
