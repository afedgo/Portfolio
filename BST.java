
package Project3;

/**
 * Filename: BST.java
 * @author afedgo
 * Date:    February 17, 2020
 * Purpose: Create Binary search tree and sort in order. Generic class
 * @param <T>
 * @version: 1.0
 */

public class BST<T extends Comparable<T>>{ 

	/**
         * Class: BSTnode
         * Purpose: Create BST nodes for BST
         */
	class BSTnode{ 
		private T key; 
		private BSTnode left, right; 
                
                /**
                 * BSTnode constructor
                 * @param item 
                 */
		public BSTnode(T item){ 
			key = item; 
			left = right = null; 
		} 
	} 

	// Root of BST 
	private BSTnode root; 

	/**
         * BST constructor. Create a null tree
         */
	BST(){ 
	    root = null; 
	} 

	/**
         * Driver method. 
         * @param key 
         * @see insertNodeec
         */ 
	public void insertNode(T key){ 
	   root = insertNodeRec(root, key); 
	} 
	
	/**
         * Recursive method to insert key into tree
         * @param root
         * @param key
         * @return BSTnode
         */
	public BSTnode insertNodeRec(BSTnode root, T key){ 

		/* If the tree is empty, return a new node */
		if (root == null){ 
			root = new BSTnode(key); 
			return root; 
		} 

		/* Otherwise, recur down the tree */
		if (key.compareTo(root.key) <= 0){
			root.left = insertNodeRec(root.left, key); 
                }       
		else if (key.compareTo(root.key) > 0){
			root.right = insertNodeRec(root.right, key); 
                }
		/* return the (unchanged) node pointer */
		return root; 
	} 

	/**
         * Prints string that orders input
         * @see inorderRec
         * @return String of order
         */
        StringBuilder str = new StringBuilder();
	public String inOrder(){ 
	    return inOrderRec(root).toString(); 
	} 

	/**
         * Orders input
         * @param root
         * @return StringBuilder of input
         */ 
	public StringBuilder inOrderRec(BSTnode root){ 
		if (root != null) { 
			inOrderRec(root.left); 
			str.append(root.key.toString() + " ");
			inOrderRec(root.right); 
		} 
                return str;
	} 	
} 


