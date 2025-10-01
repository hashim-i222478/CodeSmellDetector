import java.util.Date;
import java.util.Calendar;

// CODE SMELL: Feature Envy - This class is overly interested in Member class data
// CODE SMELL: Duplicated Code - Validation logic is repeated multiple times
public class MemberValidator {
    
    // CODE SMELL: Large Parameter List - Too many parameters make this method hard to use
    public boolean validateMemberForBorrowing(Member member, String newName, String newEmail, 
                                            String newPhone, String newAddress, int maxBooks, 
                                            double maxFines, boolean checkHistory, boolean updateInfo, 
                                            boolean sendNotification, String notificationMessage) {
        
        // Duplicated validation code #1
        if (member.getName() == null || member.getName().trim().length() < 2) {
            return false;
        }
        if (member.getEmail() == null || !member.getEmail().contains("@") || !member.getEmail().contains(".")) {
            return false;
        }
        if (member.getPhoneNumber() == null || member.getPhoneNumber().length() < 10) {
            return false;
        }
        
        // Magic numbers throughout
        if (member.getBorrowedBooks().size() >= 5) { // Magic number
            return false;
        }
        
        if (member.getTotalFines() > 25.0) { // Magic number
            return false;
        }
        
        // Feature Envy - accessing too many Member details
        Date membershipDate = member.getMembershipDate();
        Calendar cal = Calendar.getInstance();
        cal.setTime(membershipDate);
        cal.add(Calendar.MONTH, -6); // Magic number
        
        if (checkHistory && member.getBorrowCount() > 50) { // Magic number
            return false;
        }
        
        return true;
    }
    
    // CODE SMELL: Duplicated Code - Same validation logic repeated
    public boolean validateMemberForRegistration(String name, String email, String phone, String address) {
        // Duplicated validation code #2
        if (name == null || name.trim().length() < 2) {
            return false;
        }
        if (email == null || !email.contains("@") || !email.contains(".")) {
            return false;
        }
        if (phone == null || phone.length() < 10) {
            return false;
        }
        if (address == null || address.trim().length() < 5) { // Magic number
            return false;
        }
        
        return true;
    }
    
    // Feature Envy - method that knows too much about Member internals
    public double calculateMemberRisk(Member member) {
        double risk = 0.0;
        
        // Accessing many Member properties (Feature Envy)
        risk += member.getBorrowedBooks().size() * 0.1; // Magic number
        risk += member.getTotalFines() * 0.05; // Magic number
        risk += member.getBorrowCount() * 0.02; // Magic number
        
        // Magic numbers for risk calculation
        if (member.getBorrowedBooks().size() > 3) { // Magic number
            risk += 1.5; // Magic number
        }
        
        if (member.getTotalFines() > 10.0) { // Magic number
            risk += 2.0; // Magic number
        }
        
        // More magic numbers
        Date membershipDate = member.getMembershipDate();
        long daysSinceMembership = (new Date().getTime() - membershipDate.getTime()) / (1000 * 60 * 60 * 24);
        if (daysSinceMembership < 30) { // Magic number
            risk += 1.0; // Magic number
        }
        
        return risk;
    }
}