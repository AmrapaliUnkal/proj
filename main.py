from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import models
from datetime import datetime
from database import engine, Base, get_db
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

# Initialize FastAPI app
app = FastAPI()
Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define relative path for the frontend directory
frontend_path = Path(__file__).parent / "static"

# Ensure you mount the 'static' directory correctly for assets (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory=frontend_path ), name="static")

# Serve HTML files
@app.get("/", response_class=HTMLResponse)
def serve_index():
    index_file = frontend_path / "index.html"
    if index_file.exists():
        return index_file.read_text()
    raise HTTPException(status_code=404, detail="Index file not found.")

@app.get("/about", response_class=HTMLResponse)
def serve_about():
    about_file = frontend_path / "about.html"
    if about_file.exists():
        return about_file.read_text()
    raise HTTPException(status_code=404, detail="About page not found.")

@app.get("/contact", response_class=HTMLResponse)
def serve_contact():
    contact_file = frontend_path / "contact.html"
    if contact_file.exists():
        return contact_file.read_text()
    raise HTTPException(status_code=404, detail="Contact page not found.")

@app.get("/signin", response_class=HTMLResponse)
def serve_sign_in():
    sign_in_file = frontend_path / "signin.html"  # Corrected the file name here
    if sign_in_file.exists():
        return sign_in_file.read_text()
    raise HTTPException(status_code=404, detail="Sign-In page not found.")

@app.get("/option", response_class=HTMLResponse)
def serve_option():
    sign_in_file = frontend_path / "option.html"  # Corrected the file name here
    if sign_in_file.exists():
        return sign_in_file.read_text()
    raise HTTPException(status_code=404, detail="option page not found.")

@app.get("/book", response_class=HTMLResponse)
def serve_book():
    book = frontend_path / "book.html"  # Corrected the file name here
    if book.exists():
        return book.read_text()
    raise HTTPException(status_code=404, detail="book page not found.")


@app.get("/checkout", response_class=HTMLResponse)
def serve_checkout():
    book = frontend_path / "checkout.html"  # Corrected the file name here
    if book.exists():
        return book.read_text()
    raise HTTPException(status_code=404, detail="book page not found.")


#script file rendering API
@app.get("/script", response_class=HTMLResponse)
def serve_scriptJs():
    sign_in_file = frontend_path / "js/script.js"  # Corrected the file name here
    if sign_in_file.exists():
        return sign_in_file.read_text()
    raise HTTPException(status_code=404, detail="js page not found.")

#css file rendering
@app.get("/style", response_class=HTMLResponse)
def serve_style():
    sign_in_file = frontend_path / "css/style.css"  # Corrected the file name here
    if sign_in_file.exists():
        return sign_in_file.read_text()
    raise HTTPException(status_code=404, detail="css page not found.")

#availity rendering
@app.get("/availability", response_class=HTMLResponse)
def serve_availability():
    sign_in_file = frontend_path / "availability.html"  # Corrected the file name here
    if sign_in_file.exists():
        return sign_in_file.read_text()
    raise HTTPException(status_code=404, detail="availability html page not found.")

@app.get("/signup", response_class=HTMLResponse)
def serve_sign_up():
    sign_up_file = frontend_path / "signup.html"  # Corrected the file name here
    if sign_up_file.exists():
        return sign_up_file.read_text()
    raise HTTPException(status_code=404, detail="Sign-Up page not found.")

# User models for input
class UserCreate(BaseModel):
    username: str
    password: str

class RoomBooking(BaseModel):
    username: str
    room_number: int
    check_in_date: datetime
    check_out_date: datetime

class CheckoutRequest(BaseModel):
    booking_id:int

@app.post("/signup/")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = models.User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User signed up successfully!"}

@app.post("/login/")  # Corrected the endpoint to match login
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful!"}

@app.get("/rooms/")
def get_rooms(db: Session = Depends(get_db)):
    rooms = db.query(models.Room).filter(models.Room.is_available == True).all()
    if not rooms:
        return {"message": "No rooms are available"}
    return {"available_rooms": rooms}

@app.post("/book/")
def book_room(booking: RoomBooking, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == booking.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    room = db.query(models.Room).filter(models.Room.room_number == booking.room_number, models.Room.is_available == True).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not available")
    
    days_stayed = (booking.check_out_date - booking.check_in_date).days
    if days_stayed <= 0:
        raise HTTPException(status_code=400, detail="Invalid check-in/check-out dates")

    total_amount = room.price * days_stayed
    new_booking = models.Booking(
        user_id=user.id,
        room_number=room.room_number,
        check_in_date=booking.check_in_date,
        check_out_date=booking.check_out_date,
        total_amount=total_amount,
    )
    db.add(new_booking)
    room.is_available = False
    db.commit()
    db.refresh(new_booking)
    return {
        "message": f"Room {room.room_number} booked successfully under {user.username}",
        "booking_id": new_booking.booking_id,
        "total_amount": total_amount,
    }
                            
@app.post("/checkout/")
def checkout(request: CheckoutRequest, db: Session = Depends(get_db)):
    booking_id = request.booking_id
    booking = db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking_history = models.BookingHistory(
        booking_id=booking.booking_id,
        user_id=booking.user_id,
        room_number=booking.room_number,
        stay_duration=(booking.check_out_date - booking.check_in_date).days,
        total_amount=booking.total_amount,   
    )
    db.add(booking_history)

    room = db.query(models.Room).filter(models.Room.room_number == booking.room_number).first()
    if room:
        room.is_available = True

    db.delete(booking)
    db.commit()
    return {"message": f"Room {room.room_number} is now checked out and available again"}

@app.get("/booking-history/")
def get_booking_history(db: Session = Depends(get_db)):
    booking_history = db.query(models.BookingHistory).all()
    if not booking_history:
        return {"message": "No booking history available."}
    return {"booking_history": booking_history}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    