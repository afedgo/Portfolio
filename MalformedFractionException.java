
package Project3;

/**
 * Filename: MalformedFractionException.java
 * @author afedgo
 * Date:    Feb 18, 2020
 * @version 1.0
 * @see Exception
 */

public class MalformedFractionException extends Exception{

    /**
     * Creates error message with a fraction with improper format
     * @param message
     */
    public MalformedFractionException(String message){
        super(message);
    }   
}
