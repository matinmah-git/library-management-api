from sqlalchemy.orm import Session

from app.database.database import sessionlocal
from app.models.user import User
from app.models.category import Category
from app.models.book import Book
from app.models.loan import Loan
from app.models.review import Review


def seed_database():
    db: Session = sessionlocal()

    try:
        if db.query(Category).first():
            print("Database already seeded.")
            return

        categories = [
            Category(name="Programming"),
            Category(name="Computer Science"),
            Category(name="Artificial Intelligence"),
            Category(name="Cybersecurity"),
            Category(name="Database"),
            Category(name="Networking"),
            Category(name="Operating Systems"),
            Category(name="Software Engineering"),
        ]

        db.add_all(categories)
        db.commit()

        categories = {
            category.name: category.id
            for category in db.query(Category).all()
        }

        books = [
            Book(
                title="Clean Code",
                author="Robert C. Martin",
                isbn="9780132350884",
                description="A handbook of agile software craftsmanship.",
                total_copies=5,
                available_copies=5,
                category_id=categories["Software Engineering"],
            ),
            Book(
                title="The Pragmatic Programmer",
                author="Andrew Hunt",
                isbn="9780135957059",
                description="Modern software engineering practices.",
                total_copies=4,
                available_copies=4,
                category_id=categories["Software Engineering"],
            ),
            Book(
                title="Python Crash Course",
                author="Eric Matthes",
                isbn="9781718502703",
                description="Beginner-friendly Python programming.",
                total_copies=8,
                available_copies=8,
                category_id=categories["Programming"],
            ),
            Book(
                title="Fluent Python",
                author="Luciano Ramalho",
                isbn="9781492056355",
                description="Advanced Python programming.",
                total_copies=3,
                available_copies=3,
                category_id=categories["Programming"],
            ),
            Book(
                title="FastAPI in Action",
                author="Richard Hundt",
                isbn="9781617298660",
                description="Building APIs using FastAPI.",
                total_copies=6,
                available_copies=6,
                category_id=categories["Programming"],
            ),
            Book(
                title="Designing Data-Intensive Applications",
                author="Martin Kleppmann",
                isbn="9781449373320",
                description="Modern database systems and distributed applications.",
                total_copies=5,
                available_copies=5,
                category_id=categories["Database"],
            ),
            Book(
                title="Database System Concepts",
                author="Abraham Silberschatz",
                isbn="9780078022159",
                description="Comprehensive database textbook.",
                total_copies=4,
                available_copies=4,
                category_id=categories["Database"],
            ),
            Book(
                title="Computer Networking: A Top-Down Approach",
                author="James Kurose",
                isbn="9780136681557",
                description="Networking fundamentals.",
                total_copies=7,
                available_copies=7,
                category_id=categories["Networking"],
            ),
            Book(
                title="TCP/IP Illustrated",
                author="W. Richard Stevens",
                isbn="9780201633467",
                description="TCP/IP protocol reference.",
                total_copies=2,
                available_copies=2,
                category_id=categories["Networking"],
            ),
            Book(
                title="Operating System Concepts",
                author="Abraham Silberschatz",
                isbn="9781119800361",
                description="Operating system principles.",
                total_copies=5,
                available_copies=5,
                category_id=categories["Operating Systems"],
            ),
            Book(
                title="Modern Operating Systems",
                author="Andrew S. Tanenbaum",
                isbn="9780137618880",
                description="Modern operating system design.",
                total_copies=6,
                available_copies=6,
                category_id=categories["Operating Systems"],
            ),
            Book(
                title="Artificial Intelligence: A Modern Approach",
                author="Stuart Russell",
                isbn="9780134610993",
                description="Classic AI textbook.",
                total_copies=4,
                available_copies=4,
                category_id=categories["Artificial Intelligence"],
            ),
            Book(
                title="Hands-On Machine Learning",
                author="Aurelien Geron",
                isbn="9781098125974",
                description="Machine learning with Scikit-Learn and TensorFlow.",
                total_copies=5,
                available_copies=5,
                category_id=categories["Artificial Intelligence"],
            ),
            Book(
                title="Deep Learning",
                author="Ian Goodfellow",
                isbn="9780262035613",
                description="Deep learning fundamentals.",
                total_copies=2,
                available_copies=2,
                category_id=categories["Artificial Intelligence"],
            ),
            Book(
                title="Hacking: The Art of Exploitation",
                author="Jon Erickson",
                isbn="9781593271442",
                description="Low-level hacking techniques.",
                total_copies=4,
                available_copies=4,
                category_id=categories["Cybersecurity"],
            ),
            Book(
                title="The Web Application Hacker's Handbook",
                author="Dafydd Stuttard",
                isbn="9781118026472",
                description="Web application security.",
                total_copies=5,
                available_copies=5,
                category_id=categories["Cybersecurity"],
            ),
            Book(
                title="Black Hat Python",
                author="Justin Seitz",
                isbn="9781718501126",
                description="Python for penetration testing.",
                total_copies=6,
                available_copies=6,
                category_id=categories["Cybersecurity"],
            ),
            Book(
                title="Introduction to Algorithms",
                author="Thomas H. Cormen",
                isbn="9780262046305",
                description="Algorithms textbook.",
                total_copies=3,
                available_copies=3,
                category_id=categories["Computer Science"],
            ),
            Book(
                title="Computer Systems: A Programmer's Perspective",
                author="Randal Bryant",
                isbn="9780134092669",
                description="Computer architecture and systems.",
                total_copies=4,
                available_copies=4,
                category_id=categories["Computer Science"],
            ),
            Book(
                title="Structure and Interpretation of Computer Programs",
                author="Harold Abelson",
                isbn="9780262510875",
                description="Classic computer science book.",
                total_copies=2,
                available_copies=2,
                category_id=categories["Computer Science"],
            ),
        ]

        db.add_all(books)
        db.commit()

        print("Sample data inserted successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()