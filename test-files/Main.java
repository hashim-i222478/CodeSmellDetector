public class Main {
    public static void main(String[] args) {
        System.out.println("=== Library Management System ===");
        System.out.println("Demonstrating functionality with deliberate code smells\n");
        
        // Create library system
        LibrarySystem library = new LibrarySystem();
        
        // Add some books
        library.addBook("978-0134685991", "Effective Java", "Joshua Bloch", "Programming");
        library.addBook("978-0596009205", "Head First Design Patterns", "Eric Freeman", "Programming");
        library.addBook("978-0321356680", "Effective C++", "Scott Meyers", "Programming");
        
        // Add some members
        library.addMember("M001", "Ahmed Ali", "ahmed.ali@email.com", "1234567890", "123 Gulberg Lane");
        library.addMember("M002", "Fatima Khan", "fatima.khan@email.com", "0987654321", "456 DHA Avenue");
        
        // Demonstrate borrowing
        System.out.println("\n=== Borrowing Books ===");
        library.borrowBook("M001", "978-0134685991", 14, null, null, null, null, false, null, null, null);
        
        // Demonstrate new member creation during borrowing
        library.borrowBook("M003", "978-0596009205", 7, "Hassan Malik", "hassan.malik@email.com", 
                          "5551234567", "789 Johar Town", true, null, null, null);
        
        // Demonstrate search functionality
        System.out.println("\n=== Search Results ===");
        library.searchBooks("Java").forEach(System.out::println);
        
        // Demonstrate utilities
        System.out.println("\n=== Book Utilities Demo ===");
        BookUtilities utilities = new BookUtilities();
        Book book = library.getBook("978-0134685991");
        System.out.println(utilities.generateBookReport(book));
        
        // Demonstrate member validation
        System.out.println("\n=== Member Validation Demo ===");
        MemberValidator validator = new MemberValidator();
        Member member = library.getMember("M001");
        double risk = validator.calculateMemberRisk(member);
        System.out.println("Member risk score: " + risk);
        
        // Return books
        System.out.println("\n=== Returning Books ===");
        library.returnBook("978-0134685991");
        library.returnBook("978-0596009205");
        
        // Show system statistics
        System.out.println("\n=== System Statistics ===");
        System.out.println("Total Books: " + library.getTotalBooks());
        System.out.println("Total Members: " + library.getTotalMembers());
        System.out.println("Available Books: " + library.getAvailableBooks());
        
        // Run tests
        System.out.println("\n" + "=".repeat(50));
        runTests(library);
    }
    
    private static void runTests(LibrarySystem library) {
        System.out.println("Running Unit Tests...\n");
        
        int totalTests = 0;
        int passedTests = 0;
        
        // Test 1: Book management
        totalTests++;
        library.addBook("TEST001", "Test Book", "Test Author", "Fiction");
        Book testBook = library.getBook("TEST001");
        if (testBook != null && testBook.getTitle().equals("Test Book")) {
            System.out.println("✓ Test 1 PASSED: Book management");
            passedTests++;
        } else {
            System.out.println("✗ Test 1 FAILED: Book management");
        }
        
        // Test 2: Member management
        totalTests++;
        library.addMember("TEST001", "Zainab Hussain", "zainab.test@email.com", "1111111111", "Test Colony Karachi");
        Member testMember = library.getMember("TEST001");
        if (testMember != null && testMember.getName().equals("Zainab Hussain")) {
            System.out.println("✓ Test 2 PASSED: Member management");
            passedTests++;
        } else {
            System.out.println("✗ Test 2 FAILED: Member management");
        }
        
        // Test 3: Borrowing functionality
        totalTests++;
        boolean borrowResult = library.borrowBook("TEST001", "TEST001", 14, null, null, null, null, false, null, null, null);
        if (borrowResult && !testBook.isAvailable()) {
            System.out.println("✓ Test 3 PASSED: Book borrowing");
            passedTests++;
        } else {
            System.out.println("✗ Test 3 FAILED: Book borrowing");
        }
        
        // Test 4: Return functionality
        totalTests++;
        boolean returnResult = library.returnBook("TEST001");
        if (returnResult && testBook.isAvailable()) {
            System.out.println("✓ Test 4 PASSED: Book returning");
            passedTests++;
        } else {
            System.out.println("✗ Test 4 FAILED: Book returning");
        }
        
        // Test 5: Search functionality
        totalTests++;
        if (library.searchBooks("Test").size() > 0) {
            System.out.println("✓ Test 5 PASSED: Book search");
            passedTests++;
        } else {
            System.out.println("✗ Test 5 FAILED: Book search");
        }
        
        // Test 6: Validation utilities
        totalTests++;
        MemberValidator validator = new MemberValidator();
        boolean validationResult = validator.validateMemberForRegistration("Muhammad Usman", "usman.valid@email.com", "1234567890", "Model Town Lahore");
        if (validationResult) {
            System.out.println("✓ Test 6 PASSED: Member validation");
            passedTests++;
        } else {
            System.out.println("✗ Test 6 FAILED: Member validation");
        }
        
        // Test 7: Book utilities
        totalTests++;
        BookUtilities utilities = new BookUtilities();
        String report = utilities.generateBookReport(testBook);
        if (report.contains("BOOK REPORT")) {
            System.out.println("✓ Test 7 PASSED: Book utilities");
            passedTests++;
        } else {
            System.out.println("✗ Test 7 FAILED: Book utilities");
        }
        
        // Test 8: System statistics
        totalTests++;
        if (library.getTotalBooks() >= 4 && library.getTotalMembers() >= 3) {
            System.out.println("✓ Test 8 PASSED: System statistics");
            passedTests++;
        } else {
            System.out.println("✗ Test 8 FAILED: System statistics");
        }
        
        System.out.println("\n=== Test Summary ===");
        System.out.println("Total Tests: " + totalTests);
        System.out.println("Passed: " + passedTests);
        System.out.println("Failed: " + (totalTests - passedTests));
        System.out.println("Success Rate: " + (passedTests * 100 / totalTests) + "%");
    }
}