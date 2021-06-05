package Project3;


/**
 * filename: P3GUI.java
 * @author afedgo
 * Date:    February 17, 2020
 * Purpose: Create a GUI that creates a BST and performs a sort
 * @version 1.0
 * @see BST.java
 */




//Import packages
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JTextField;
import javax.swing.JRadioButton;
import javax.swing.ButtonGroup;
import javax.swing.BorderFactory;
import java.awt.GridLayout;
import java.awt.FlowLayout;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;


public class P3GUI extends JFrame{
    //Gui declarations
    private JButton sortBtn;
    private JTextField inputTxt, resultTxt;
    private JLabel inputLbl, resultLbl;
    private JRadioButton ascendingRadio, descendingRadio, intRadio, fractRadio;
    
    /**
     * Constructor that formats the JFrame
     */
    public P3GUI(){
        setTitle("Binary Search Tree Sort");
        setLayout(new FlowLayout());
        setSize(450,250);
        setResizable(false);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        addComponentsToPane();
    } 
    /**
     * Adds labels, text fields, buttons, and radio buttons to j frame
     */
    public void addComponentsToPane(){
        //Jpanel for input
        JPanel in = new JPanel();
        in.setLayout(new FlowLayout());
        //Jpanel for result
        JPanel out = new JPanel();
        out.setLayout(new FlowLayout());
        //jpanel for button
        JPanel btn = new JPanel();
        btn.setLayout(new GridLayout(1,1));
        btn.setPreferredSize(new Dimension(230,40));
        //jpanel for sorting radio buttons
        JPanel radioSort = new JPanel();
        radioSort.setLayout(new GridLayout(2,1));
        radioSort.setPreferredSize(new Dimension(200,80));
        //jpanel for radio types
        JPanel radioType = new JPanel();
        radioType.setLayout(new GridLayout(2,1));
        radioType.setPreferredSize(new Dimension(200,80));
        
       //Input field
        inputLbl = new JLabel("Original List ");
        in.add(inputLbl);
        inputTxt = new JTextField(35);
        in.add(inputTxt);
        add(in);
        
        //Result field
        resultLbl = new JLabel("   Sorted List");
        out.add(resultLbl);
        resultTxt = new JTextField(35);
        resultTxt.setEditable(false);
        out.add(resultTxt);   
        add(out);
        
        //add Sort button
        sortBtn = new JButton("Perform Sort");
        btn.add(sortBtn);
        add(btn);
        
        //Sort radio
        ascendingRadio = new JRadioButton("Ascending",true);
        descendingRadio = new JRadioButton("Descending");
        ButtonGroup sort = new ButtonGroup();
        sort.add(ascendingRadio);
        sort.add(descendingRadio);
        radioSort.add(ascendingRadio);
        radioSort.add(descendingRadio);
        radioSort.setBorder(BorderFactory.createTitledBorder("Sort Order"));
        add(radioSort);
        
        //Type radio
        intRadio = new JRadioButton("Integer",true);
        fractRadio = new JRadioButton("Fraction");
        ButtonGroup type = new ButtonGroup();
        type.add(intRadio);
        type.add(fractRadio);
        radioType.add(intRadio);
        radioType.add(fractRadio);
        radioType.setBorder(BorderFactory.createTitledBorder("Numeric Type"));
        add(radioType);
        
        //action for eval button
        sortBtn.addActionListener(new ActionListener() {
            @Override
            /**
             * Action event: sorts input
             */
            public void actionPerformed(ActionEvent e) {
                //tokenize based off of whitespace
                String[] tokens = inputTxt.getText().split("\\s+");
                long size = tokens.length;
                //Create tree
                BST root = new BST();
                int error = 0;
                //Goes through every token to add to ree
                for (int i = 0; i < size; i++){
                    //If integer is requested add integers to tree
                    if (intRadio.isSelected()){
                        try{
                             root.insertNode(Integer.parseInt(tokens[i]));
                        }
                        //Throw error if non-integer. Delete result text
                        catch(NumberFormatException nfe){
                            error = 1;
                            resultTxt.setText(" ");
                            JOptionPane.showMessageDialog(null, 
                                    "Non-numeric input");
                        }
                    }
                    //If fraction is selected add fractions to tree
                    else{
                        try{
                            root.insertNode(new Fraction (tokens[i]));
                        }
                        //if fraction not proper throw error and delete result
                        catch(MalformedFractionException mfe){
                            error = 1;
                            resultTxt.setText(" ");
                            JOptionPane.showMessageDialog(null,mfe);
                        }
                    }
                }
                //If ascending sort requested and building tree did not
                //throw an error than fill the result field with ascending order
                if (ascendingRadio.isSelected() && error == 0){
                    resultTxt.setText(root.inOrder());
                }
                //If descending sort requested and building tree did not throw
                // an error than fill the result field with descending order
                else if (descendingRadio.isSelected() && error == 0){
                    String[] num = root.inOrder().split(" ");
                    int iterate = num.length;
                    StringBuilder reverse = new StringBuilder();
                    //iterate through result backwards
                    for (int i = iterate - 1; i >= 0; i--){
                        reverse.append(num[i] + " ");
                    }
                    resultTxt.setText(reverse.toString());
                }
                //check for duplicates
                String[] dup = root.inOrder().split(" ");
                int dupSize = dup.length;
                int flag = 0;
                for (int i = 0; i<dupSize-1;i++){
                    if (dup[i].equals(dup[++i])){
                        flag = 1;
                    }
                }
                //If duplicate and  no error produced then show message that
                //explains there were duplicates
                if(flag == 1 && error == 0){
                    JOptionPane.showMessageDialog(null,
                            "The input contains duplicates");
                }
                //If no duplicates and no error message produced then show
                //message that explains there were no duplicates
                else if (flag == 0 && error == 0){
                    JOptionPane.showMessageDialog(null,
                            "The input does not contain duplicates");
                }   
            }
        });  
    }
    
    /**
     * Create GUI app and show it
     * @param args 
     */
    public static void main(String[]args ){
        P3GUI app = new P3GUI();
        app.setVisible(true);    
    }
}
