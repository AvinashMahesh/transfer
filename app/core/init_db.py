"""
Database initialization script
"""
from sqlalchemy.orm import Session
from app.core.database import engine, Base, SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.initiative import Initiative, InitiativeStatus, InitiativeDuration

def init_db():
    """Initialize database with tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")

def seed_sample_data():
    """Seed database with sample data for testing"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            print("Database already contains data. Skipping seed.")
            return
        
        print("Seeding sample data...")
        
        # Default password for all test accounts: "password123"
        default_password_hash = get_password_hash("password123")
        
        # Create sample users
        import json
        
        analyst = User(
            email="analyst@deloitte.com",
            password_hash=default_password_hash,
            full_name="John Analyst",
            role=UserRole.ANALYST,
            bio="Strategy consultant with 3 years experience",
            practice="Strategy",
            skills=json.dumps(["Python", "Data Analysis", "PowerBI", "Financial Modeling"]),
            interests=json.dumps(["AI", "Healthcare", "Innovation"]),
            industries=json.dumps(["Healthcare", "Financial Services"]),
            experience_years=3,
            certifications=json.dumps(["PMP", "Six Sigma"])
        )
        
        leader = User(
            email="leader@deloitte.com",
            password_hash=default_password_hash,
            full_name="Sarah Leader",
            role=UserRole.LEADER,
            bio="Senior manager leading innovation initiatives",
            practice="Technology",
            skills=json.dumps(["AI/ML", "Cloud Computing", "Team Leadership"]),
            interests=json.dumps(["Innovation", "Technology", "Mentoring"]),
            industries=json.dumps(["Technology", "Healthcare"]),
            experience_years=8
        )
        
        admin = User(
            email="admin@deloitte.com",
            password_hash=default_password_hash,
            full_name="Admin User",
            role=UserRole.ADMIN,
            practice="Operations"
        )
        
        db.add_all([analyst, leader, admin])
        db.commit()
        db.refresh(leader)
        
        # Create sample initiatives
        initiative1 = Initiative(
            title="AI Healthcare Research Pod",
            description="Join our research team exploring AI applications in healthcare. We're investigating how machine learning can improve patient outcomes and reduce costs. Looking for analysts with data science skills and healthcare knowledge.",
            practice_area="Technology",
            skills_needed=json.dumps(["Python", "Machine Learning", "Data Analysis", "Healthcare Knowledge"]),
            industries=json.dumps(["Healthcare"]),
            tags=json.dumps(["AI", "Healthcare", "Research", "Machine Learning"]),
            time_commitment="5-10 hours/week",
            duration=InitiativeDuration.ONGOING,
            role_type="Researcher",
            contact_person="Sarah Leader",
            contact_email="leader@deloitte.com",
            status=InitiativeStatus.OPEN,
            owner_id=leader.id
        )
        
        initiative2 = Initiative(
            title="Innovation Hub - GenAI Applications",
            description="The Innovation Hub is launching a new workstream focused on Generative AI applications for client solutions. We're looking for creative thinkers to prototype AI-powered tools and conduct market research.",
            practice_area="Technology",
            skills_needed=json.dumps(["Python", "GenAI", "Prototyping", "Research"]),
            industries=json.dumps(["Technology", "Consulting"]),
            tags=json.dumps(["GenAI", "Innovation", "Prototyping"]),
            time_commitment="10 hours/week",
            duration=InitiativeDuration.SHORT_TERM,
            duration_details="3 months",
            role_type="Innovation Analyst",
            contact_person="Sarah Leader",
            contact_email="leader@deloitte.com",
            status=InitiativeStatus.OPEN,
            owner_id=leader.id
        )
        
        initiative3 = Initiative(
            title="Financial Services Digital Transformation",
            description="Help develop thought leadership on digital transformation in banking and financial services. Research emerging technologies, interview clients, and contribute to white papers.",
            practice_area="Strategy",
            skills_needed=json.dumps(["Research", "Financial Services", "Writing", "Client Engagement"]),
            industries=json.dumps(["Financial Services", "Banking"]),
            tags=json.dumps(["Digital Transformation", "Financial Services", "Research"]),
            time_commitment="5 hours/week",
            duration=InitiativeDuration.ONGOING,
            role_type="Research Analyst",
            contact_person="Sarah Leader",
            contact_email="leader@deloitte.com",
            status=InitiativeStatus.ACTIVE,
            owner_id=leader.id
        )
        
        initiative4 = Initiative(
            title="Sustainability Volunteering - Pro Bono",
            description="Volunteer opportunity to help non-profit organizations develop sustainability strategies. Work directly with NGOs on climate action initiatives.",
            practice_area="Risk & Sustainability",
            skills_needed=json.dumps(["Strategy", "Sustainability", "Project Management"]),
            industries=json.dumps(["Non-Profit", "Environmental"]),
            tags=json.dumps(["Volunteering", "Sustainability", "Pro Bono", "Climate"]),
            time_commitment="3-5 hours/week",
            duration=InitiativeDuration.SHORT_TERM,
            duration_details="6 months",
            role_type="Strategy Consultant",
            contact_person="Sarah Leader",
            contact_email="leader@deloitte.com",
            status=InitiativeStatus.OPEN,
            owner_id=leader.id
        )
        
        db.add_all([initiative1, initiative2, initiative3, initiative4])
        db.commit()
        
        print("✓ Sample data seeded successfully!")
        print(f"  - Created {db.query(User).count()} users")
        print(f"  - Created {db.query(Initiative).count()} initiatives")
        print("\n📧 Test Account Credentials:")
        print("  Email: analyst@deloitte.com | Password: password123 | Role: Analyst")
        print("  Email: leader@deloitte.com  | Password: password123 | Role: Leader")
        print("  Email: admin@deloitte.com   | Password: password123 | Role: Admin")
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    seed_sample_data()
