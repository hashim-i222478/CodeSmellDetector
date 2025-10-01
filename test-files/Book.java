import java.util.Date;

public class Book {
    private String isbn;
    private String title;
    private String author;
    private String category;
    private boolean isAvailable;
    private Date dueDate;
    private String borrowerMemberId;
    
    public Book(String isbn, String title, String author, String category) {
        this.isbn = isbn;
        this.title = title;
        this.author = author;
        this.category = category;
        this.isAvailable = true;
        this.dueDate = null;
        this.borrowerMemberId = null;
    }
    
    // Getters and setters
    public String getIsbn() { return isbn; }
    public String getTitle() { return title; }
    public String getAuthor() { return author; }
    public String getCategory() { return category; }
    public boolean isAvailable() { return isAvailable; }
    public Date getDueDate() { return dueDate; }
    public String getBorrowerMemberId() { return borrowerMemberId; }
    
    public void setAvailable(boolean available) { isAvailable = available; }
    public void setDueDate(Date dueDate) { this.dueDate = dueDate; }
    public void setBorrowerMemberId(String borrowerMemberId) { this.borrowerMemberId = borrowerMemberId; }
    
    @Override
    public String toString() {
        return "Book{" +
                "isbn='" + isbn + '\'' +
                ", title='" + title + '\'' +
                ", author='" + author + '\'' +
                ", category='" + category + '\'' +
                ", isAvailable=" + isAvailable +
                '}';
    }
}