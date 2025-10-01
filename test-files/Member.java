import java.util.ArrayList;
import java.util.List;
import java.util.Date;

public class Member {
    private String memberId;
    private String name;
    private String email;
    private String phoneNumber;
    private String address;
    private Date membershipDate;
    private List<String> borrowedBooks;
    private int borrowCount;
    private double totalFines;
    
    public Member(String memberId, String name, String email, String phoneNumber, String address) {
        this.memberId = memberId;
        this.name = name;
        this.email = email;
        this.phoneNumber = phoneNumber;
        this.address = address;
        this.membershipDate = new Date();
        this.borrowedBooks = new ArrayList<>();
        this.borrowCount = 0;
        this.totalFines = 0.0;
    }
    
    // Getters and setters
    public String getMemberId() { return memberId; }
    public String getName() { return name; }
    public String getEmail() { return email; }
    public String getPhoneNumber() { return phoneNumber; }
    public String getAddress() { return address; }
    public Date getMembershipDate() { return membershipDate; }
    public List<String> getBorrowedBooks() { return borrowedBooks; }
    public int getBorrowCount() { return borrowCount; }
    public double getTotalFines() { return totalFines; }
    
    public void setName(String name) { this.name = name; }
    public void setEmail(String email) { this.email = email; }
    public void setPhoneNumber(String phoneNumber) { this.phoneNumber = phoneNumber; }
    public void setAddress(String address) { this.address = address; }
    public void setBorrowCount(int borrowCount) { this.borrowCount = borrowCount; }
    public void setTotalFines(double totalFines) { this.totalFines = totalFines; }
    
    public void addBorrowedBook(String isbn) {
        borrowedBooks.add(isbn);
        borrowCount++;
    }
    
    public void removeBorrowedBook(String isbn) {
        borrowedBooks.remove(isbn);
    }
    
    @Override
    public String toString() {
        return "Member{" +
                "memberId='" + memberId + '\'' +
                ", name='" + name + '\'' +
                ", email='" + email + '\'' +
                ", borrowedBooks=" + borrowedBooks.size() +
                '}';
    }
}