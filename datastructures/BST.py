"""
BST.py - AVL binary search tree

Author: Owen Ringrose
Date: 4/17/2026

Insertion logic from: https://www.geeksforgeeks.org/dsa/insertion-in-an-avl-tree/ Expanded this to add rest of BST functions

**** Revision History ****
-4/17/2026: implemented basic AVL structure
-4/19/2026: Added get top_n
"""



from datastructures.array import ArrayList
from datastructures.stack import Stack

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1
    

class BST:
    def __init__(self):
        self.head = None
        self.elements = 0

    def _get_tree_height(self, x):
        """Helper function so we do not have to do a bunch of if statements when checking height"""
        if isinstance(x, Node):
            return x.height
        else:
            return 0
        
    def _get_balance(self, node):
        """Gets the balance factor of a node"""
        if node is None:
            return 0
        return self._get_tree_height(node.left) - self._get_tree_height(node.right)

    def _min_value_node(self, node):
        """Gets the minimum value of a subtree at root node"""
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def right_rotate(self, y):
        """ Performs a right rotation of a subtree. Y is the root of the subtree. returns the new root"""
        x = y.left
        z = x.right

        # Swap x and y
        x.right = y
        y.left = z

        #update heights
        y.height = 1 + max(self._get_tree_height(y.left), self._get_tree_height(y.right))
        x.height = 1 + max(self._get_tree_height(x.left), self._get_tree_height(x.right))
    
        return x
    
    def left_rotate(self,y):
        """ Performs a left rotation of a subtree. Y is the root of the subtree. returns the new root"""
        x = y.right
        z = x.left

        # Swap x and y
        x.left = y
        y.right = z

        #update heights
        y.height = 1 + max(self._get_tree_height(y.left), self._get_tree_height(y.right))
        x.height = 1 + max(self._get_tree_height(x.left), self._get_tree_height(x.right))

        return x
    
    def _insert(self, node, key):
        """Recursive insert function"""
        if node is None:
            self.elements += 1
            return Node(key)

        # Standard Insertion logic
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node

        # Update the height
        node.height = 1 + max(self._get_tree_height(node.left),
                            self._get_tree_height(node.right))

        # Get balance factor
        balance = self._get_balance(node)

        # Balance the tree

        # LEFT LEFT
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)

        # RIGHT RIGHT
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)

        # LEFT RIGHT
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # RIGHT LEFT
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def insert(self, key):
        """Insert an element into the BST"""
        self.head = self._insert(self.head, key)

    def delete(self, key):
        """Delete a key from the BST"""
        self.head = self._delete(self.head, key)

    def _delete(self, node, key):
        """Recursive delete function"""
        if node is None:
            return node

        # BST delete
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Node found

            # 0 or 1 child
            if node.left is None:
                self.elements -= 1
                return node.right
            elif node.right is None:
                self.elements -= 1
                return node.left

            # 2 children
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)
            self.elements -= 1  # FIX: missing decrement for 2-child case

        # If tree had one node
        if node is None:
            return node

        # Update height
        node.height = 1 + max(self._get_tree_height(node.left),
                            self._get_tree_height(node.right))

        

        # balance tree

        balance = self._get_balance(node)  # FIX: consistent balance usage

        
        # left left rotation
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self.right_rotate(node)

        # left left rotation
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # right right rotation
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self.left_rotate(node)

        # right left rotation
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def search(self, key):
        """Return element from BST"""
        return self._search(self.head, key)

    def _search(self, node, key):
        """Recursive element search"""
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)
    
    def get_elements_sorted(self):
        """Returns all elements in order from smallest to largest, inorder traversal"""
        stack = Stack()
        current = self.head
        result = ArrayList()

        # Basically this is Depth First Seaarch
        while current is not None or len(stack) > 0:
            # Go as left as possible
            while current is not None:
                stack.push(current)
                current = current.left

            # Process node
            current = stack.pop()
            result.append(current.key)

            # Visit right subtree
            current = current.right

        return result
    
    def range_query(self, low, high):
        """ Ranged query of BST, returns array of elements between low and high """
        stack = Stack()
        current = self.head
        result = ArrayList()

        while len(stack) > 0 or current is not None:

            while current is not None:
                if current.key >= low:
                    stack.push(current)
                    current = current.left
                else:
                    current = current.right

            if len(stack) == 0:
                break

            current = stack.pop()

            if current.key > high:
                break

            if low <= current.key <= high:
                result.append(current.key)

            current = current.right

        return result
    
    def get_top_n(self, n):
        """Return the top n elements. Returns items in an ArrayList"""
        stack = Stack()
        top_n = ArrayList()
        current = self.head

        if n <= 0:
            return top_n

        # Depth First basically
        while current is not None or len(stack) > 0:
            # explore right nodes first
            while current is not None:
                stack.push(current)
                current = current.right

            current = stack.pop()
            top_n.append(current.key)
            # If we reach n items exit early
            if len(top_n) == n:
                return top_n
            current = current.left
        return top_n

            

    def __len__(self):
        """
        Get the length of the BST
        """
        # TODO: Return the size
        return self.elements
    
    
    def __contains__(self, key):
        return self.search(key) is not None