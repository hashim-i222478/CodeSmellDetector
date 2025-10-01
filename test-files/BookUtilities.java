import java.util.Date;
import java.util.Calendar;

// More examples of code smells
public class BookUtilities {
    
    // CODE SMELL: Duplicated Code - Same date calculation logic repeated
    public boolean isBookOverdue(Book book) {
        if (book.getDueDate() == null) {
            return false;
        }
        
        Date today = new Date();
        if (book.getDueDate().before(today)) {
            long overdueDays = (today.getTime() - book.getDueDate().getTime()) / (1000 * 60 * 60 * 24); // Magic numbers
            return overdueDays > 0;
        }
        return false;
    }
    
    // CODE SMELL: Duplicated Code - Same date calculation logic repeated again
    public long calculateOverdueDays(Book book) {
        if (book.getDueDate() == null) {
            return 0;
        }
        
        Date today = new Date();
        if (book.getDueDate().before(today)) {
            long overdueDays = (today.getTime() - book.getDueDate().getTime()) / (1000 * 60 * 60 * 24); // Magic numbers
            return overdueDays;
        }
        return 0;
    }
    
    // CODE SMELL: Feature Envy - This method is overly interested in Book's internal data
    public String generateBookReport(Book book) {
        StringBuilder report = new StringBuilder();
        
        // Accessing many Book properties (Feature Envy)
        report.append("=== BOOK REPORT ===\n");
        report.append("ISBN: ").append(book.getIsbn()).append("\n");
        report.append("Title: ").append(book.getTitle()).append("\n");
        report.append("Author: ").append(book.getAuthor()).append("\n");
        report.append("Category: ").append(book.getCategory()).append("\n");
        report.append("Available: ").append(book.isAvailable() ? "Yes" : "No").append("\n");
        
        if (!book.isAvailable()) {
            report.append("Borrower: ").append(book.getBorrowerMemberId()).append("\n");
            report.append("Due Date: ").append(book.getDueDate()).append("\n");
            
            // Magic numbers for fine calculation
            Date today = new Date();
            if (book.getDueDate().before(today)) {
                long overdueDays = (today.getTime() - book.getDueDate().getTime()) / (1000 * 60 * 60 * 24);
                double fineRate = 0.5; // Magic number - should be configurable
                if (book.getCategory().equals("Reference")) {
                    fineRate = 1.0; // Magic number
                } else if (book.getCategory().equals("Children")) {
                    fineRate = 0.25; // Magic number
                }
                double totalFine = overdueDays * fineRate;
                report.append("Overdue Days: ").append(overdueDays).append("\n");
                report.append("Fine Amount: $").append(totalFine).append("\n");
            }
        }
        
        report.append("==================\n");
        return report.toString();
    }
    
    // CODE SPELL: Magic Numbers - Hardcoded values throughout
    public boolean isPopularCategory(String category) {
        // Magic numbers for category popularity thresholds
        switch (category) {
            case "Fiction":
                return true; // Always considered popular
            case "Non-Fiction":
                return true; // Always considered popular
            case "Reference":
                return false; // Less popular
            case "Children":
                return true; // Popular
            default:
                return false;
        }
    }
}