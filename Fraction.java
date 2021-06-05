package Project3;

/**
 * Filename: Fraction.java
 * @author afedgo
 * Date: Feb 17, 2020
 * Purpose: To read, compare and print fractions
 * @version 1.0
 */
public class Fraction implements Comparable<Fraction> {
    private int numerator;
    private int denominator;
    private String key;
    /**
     * Fraction constructor. Throw error if not a fraction
     * @param fraction
     * @throws MalformedFractionException 
     */
    public Fraction(String fraction) throws MalformedFractionException{
        //Check if fraction is proper. If not then throw error
        String[] token = fraction.split("/");
        if (token.length != 2){
            throw new MalformedFractionException("Malformed Fraction " + fraction);
        }
        else{ 
            if(token[1].equals("0")){
                throw new MalformedFractionException("Malformed Fraction " + fraction);
            }
            else{
                this.numerator = Integer.parseInt(token[0]);
                this.denominator = Integer.parseInt(token[1]);
                this.key=fraction;
            }
        }
    }
    
    /**
     * Prints in fraction form
     * @return string of fraction representation
     */
    @Override
    public String toString(){
        return numerator + "/" + denominator;
    }
    
    /**
     * Compares two fractions
     * @param otherFraction
     * @return integer that explains order of two fractions
     */
    @Override
    public int compareTo(Fraction otherFraction){
        return (int)(numerator * otherFraction.denominator - 
                denominator * otherFraction.numerator);
    }
}


