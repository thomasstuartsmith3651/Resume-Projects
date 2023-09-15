#include <stdio.h>
#include <stdlib.h>

typedef int Data; // binary tree to store integers


typedef struct node{Data d;struct node  *left;struct node *right;}Node;

typedef Node* BTree; //we define the tree as a pointer to a node and so a tree is actually n trees from recursion 

//this function is for 'in order' traversal which stores the integers in the standard order
void in_order(BTree root){
    if(root != NULL)
    {
        in_order(root->left);
        printf("%d\n", root->d);
        in_order(root->right);
    }
}

// Finds size of node and then initialises it to be generated for every now tree branch
Node *new_node(void){
    return malloc(sizeof(Node));
}
Node *init_node(Data d, Node *left, Node *right){
    Node *t;
    t = new_node();
    t->d = d; //we assign new values to each member of the struct (data and pointers) to allow recursion
    t->left = left;
    t->right = right;
    return t;
}

// This create trees function is used to generate intial tree and subtrees from nodes
BTree create_tree(Data a[], int i, int size){
    if (i>=size)
        return NULL;
    else
        return init_node(a[i], create_tree(a, i*2+1, size), create_tree(a, i*2+2, size));
    
}

// reads the file binary.txt {4 9 11 4 5} therefore expected output is 5 11 9 4
void read_file(FILE *ifp, int d[], int size){
	
    int i; 
    for(i = 0; i < size; i++){
        fscanf(ifp, "%d", &d[i]);
    }
}

int main(int argc, char *argv[]){
    
    FILE *ifp; 
    int n; 
    ifp = fopen(argv[1], "r"); // opening the file

    int data[n]; // creating array of size n to store binary tree order

    // run functions in order
    read_file(ifp, data, n);
    BTree b;
    b = create_tree(data, 0, n);
    in_order(b);
    fclose(ifp);
    return 0;
}