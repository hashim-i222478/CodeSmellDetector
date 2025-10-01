import java.util.*;
import java.text.SimpleDateFormat;

// CODE SMELL: God Class (Blob) - This class handles too many responsibilities
public class LibrarySystem {
    private Map<String, Book> books;
    private Map<String, Member> members;
    private List<String> transactionHistory;
    private Map<String, Double> categoryFines;
    private Scanner scanner;
    private SimpleDateFormat dateFormat;
    
    public LibrarySystem() {
        this.books = new HashMap<>();
        this.members = new HashMap<>();
        this.transactionHistory = new ArrayList<>();
        this.categoryFines = new HashMap<>();
        this.scanner = new Scanner(System.in);
        this.dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        initializeCategoryFines();
    }
    
    private void initializeCategoryFines() {
        categoryFines.put("Fiction", 0.5);
        categoryFines.put("Non-Fiction", 0.75);
        categoryFines.put("Reference", 1.0);
        categoryFines.put("Children", 0.25);
    }
    
    // CODE SMELL: Long Method - This method is excessively long and does too much
    public boolean borrowBook(String memberId, String isbn, int borrowDays, String memberName, 
                             String memberEmail, String memberPhone, String memberAddress, 
                             boolean isNewMember, String bookTitle, String bookAuthor, String bookCategory) {
        
        // Validate member exists or create new one
        Member member = members.get(memberId);
        if (member == null && isNewMember) {
            // Create new member with validation
            if (memberName == null || memberName.trim().length() < 2) {
                System.out.println("Invalid member name. Must be at least 2 characters.");
                return false;
            }
            if (memberEmail == null || !memberEmail.contains("@") || !memberEmail.contains(".")) {
                System.out.println("Invalid email format.");
                return false;
            }
            if (memberPhone == null || memberPhone.length() < 10) {
                System.out.println("Invalid phone number. Must be at least 10 digits.");
                return false;
            }
            if (memberAddress == null || memberAddress.trim().length() < 5) {
                System.out.println("Invalid address. Must be at least 5 characters.");
                return false;
            }
            
            member = new Member(memberId, memberName, memberEmail, memberPhone, memberAddress);
            members.put(memberId, member);
            System.out.println("New member created: " + memberName);
        } else if (member == null) {
            System.out.println("Member not found: " + memberId);
            return false;
        }
        
        // Check member borrowing limits based on membership type and history
        if (member.getBorrowedBooks().size() >= 5) { // Magic number
            System.out.println("Member has reached maximum borrowing limit of 5 books.");
            return false;
        }
        
        if (member.getTotalFines() > 25.0) { // Magic number
            System.out.println("Member has outstanding fines exceeding $25.00. Cannot borrow.");
            return false;
        }
        
        // Validate book exists or create new one
        Book book = books.get(isbn);
        if (book == null) {
            if (bookTitle != null && bookAuthor != null && bookCategory != null) {
                book = new Book(isbn, bookTitle, bookAuthor, bookCategory);
                books.put(isbn, book);
                System.out.println("New book added to library: " + bookTitle);
            } else {
                System.out.println("Book not found and insufficient information to create new book.");
                return false;
            }
        }
        
        // Check if book is available
        if (!book.isAvailable()) {
            System.out.println("Book is currently not available: " + book.getTitle());
            
            // Calculate estimated return date based on current borrower
            if (book.getDueDate() != null) {
                Calendar cal = Calendar.getInstance();
                cal.setTime(book.getDueDate());
                System.out.println("Estimated return date: " + dateFormat.format(cal.getTime()));
                
                // Check if book is overdue
                Date today = new Date();
                if (book.getDueDate().before(today)) {
                    long overdueDays = (today.getTime() - book.getDueDate().getTime()) / (1000 * 60 * 60 * 24);
                    double fine = overdueDays * categoryFines.get(book.getCategory());
                    System.out.println("Book is overdue by " + overdueDays + " days. Fine: $" + fine);
                }
            }
            return false;
        }
        
        // Calculate due date
        Calendar cal = Calendar.getInstance();
        cal.add(Calendar.DAY_OF_MONTH, borrowDays);
        Date dueDate = cal.getTime();
        
        // Process the borrowing
        book.setAvailable(false);
        book.setDueDate(dueDate);
        book.setBorrowerMemberId(memberId);
        member.addBorrowedBook(isbn);
        
        // Record transaction
        String transaction = "BORROW: Member " + memberId + " borrowed book " + isbn + 
                           " (" + book.getTitle() + ") on " + dateFormat.format(new Date()) + 
                           " due " + dateFormat.format(dueDate);
        transactionHistory.add(transaction);
        
        // Print confirmation with details
        System.out.println("=== BORROWING CONFIRMATION ===");
        System.out.println("Member: " + member.getName() + " (" + memberId + ")");
        System.out.println("Book: " + book.getTitle() + " by " + book.getAuthor());
        System.out.println("ISBN: " + isbn);
        System.out.println("Category: " + book.getCategory());
        System.out.println("Borrow Date: " + dateFormat.format(new Date()));
        System.out.println("Due Date: " + dateFormat.format(dueDate));
        System.out.println("Borrowing Period: " + borrowDays + " days");
        System.out.println("Daily Fine Rate: $" + categoryFines.get(book.getCategory()));
        System.out.println("Books Currently Borrowed: " + member.getBorrowedBooks().size());
        System.out.println("Total Books Borrowed (Lifetime): " + member.getBorrowCount());
        System.out.println("==============================");
        
        return true;
    }
    
    public boolean returnBook(String isbn) {
        Book book = books.get(isbn);
        if (book == null) {
            System.out.println("Book not found: " + isbn);
            return false;
        }
        
        if (book.isAvailable()) {
            System.out.println("Book is not currently borrowed: " + book.getTitle());
            return false;
        }
        
        Member member = members.get(book.getBorrowerMemberId());
        Date today = new Date();
        double fine = 0.0;
        
        // Calculate fine if overdue
        if (book.getDueDate().before(today)) {
            long overdueDays = (today.getTime() - book.getDueDate().getTime()) / (1000 * 60 * 60 * 24);
            fine = overdueDays * categoryFines.get(book.getCategory());
            member.setTotalFines(member.getTotalFines() + fine);
        }
        
        // Process return
        book.setAvailable(true);
        book.setDueDate(null);
        member.removeBorrowedBook(isbn);
        book.setBorrowerMemberId(null);
        
        // Record transaction
        String transaction = "RETURN: Book " + isbn + " returned on " + dateFormat.format(today) + 
                           (fine > 0 ? " with fine $" + fine : "");
        transactionHistory.add(transaction);
        
        System.out.println("Book returned successfully" + (fine > 0 ? " with fine: $" + fine : ""));
        return true;
    }
    
    public void addBook(String isbn, String title, String author, String category) {
        if (books.containsKey(isbn)) {
            System.out.println("Book with ISBN " + isbn + " already exists.");
            return;
        }
        
        Book book = new Book(isbn, title, author, category);
        books.put(isbn, book);
        System.out.println("Book added successfully: " + title);
    }
    
    public void addMember(String memberId, String name, String email, String phone, String address) {
        if (members.containsKey(memberId)) {
            System.out.println("Member with ID " + memberId + " already exists.");
            return;
        }
        
        Member member = new Member(memberId, name, email, phone, address);
        members.put(memberId, member);
        System.out.println("Member added successfully: " + name);
    }
    
    public List<Book> searchBooks(String query) {
        List<Book> results = new ArrayList<>();
        for (Book book : books.values()) {
            if (book.getTitle().toLowerCase().contains(query.toLowerCase()) ||
                book.getAuthor().toLowerCase().contains(query.toLowerCase()) ||
                book.getIsbn().contains(query)) {
                results.add(book);
            }
        }
        return results;
    }
    
    public Member getMember(String memberId) {
        return members.get(memberId);
    }
    
    public Book getBook(String isbn) {
        return books.get(isbn);
    }
    
    public List<String> getTransactionHistory() {
        return new ArrayList<>(transactionHistory);
    }
    
    public int getTotalBooks() {
        return books.size();
    }
    
    public int getTotalMembers() {
        return members.size();
    }
    
    public int getAvailableBooks() {
        int count = 0;
        for (Book book : books.values()) {
            if (book.isAvailable()) count++;
        }
        return count;
    }
}