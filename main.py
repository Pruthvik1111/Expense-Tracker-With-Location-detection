from datetime import datetime
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from starlette.middleware.sessions import SessionMiddleware
import hashlib

DATABASE_URL = "mysql+mysqlconnector://root:PruPra111904@localhost/expense_tracker"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# ── Models ──────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"
    id       = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email    = Column(String(150), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    expenses = relationship("Expense", back_populates="owner")


class Expense(Base):
    __tablename__ = "expenses"
    id         = Column(Integer, primary_key=True, index=True)
    title      = Column(String(100))
    category   = Column(String(100))
    amount     = Column(Float)
    user_id    = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now)
    latitude   = Column(Float, nullable=True)   # ← GPS lat
    longitude  = Column(Float, nullable=True)   # ← GPS lng
    owner      = relationship("User", back_populates="expenses")


Base.metadata.create_all(bind=engine)

# ── App setup ────────────────────────────────────────────
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="kodnest-secret-2026")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# ── Helpers ──────────────────────────────────────────────
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def get_current_user(request: Request):
    return request.session.get("user_id")


# ── Dashboard ────────────────────────────────────────────
@app.get("/")
def home(request: Request):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse("/login", status_code=302)

    db       = SessionLocal()
    user     = db.query(User).filter(User.id == user_id).first()
    expenses = db.query(Expense).filter(Expense.user_id == user_id).order_by(Expense.created_at.desc()).all()
    total    = sum(e.amount for e in expenses)
    db.close()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "expenses": expenses,
            "total":    total,
            "username": user.username if user else "User"
        }
    )


# ── Signup ───────────────────────────────────────────────
@app.get("/signup")
def signup_page(request: Request):
    if get_current_user(request):
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse(request=request, name="signup.html", context={"error": None})


@app.post("/signup")
def signup(request: Request,
           username: str = Form(...),
           email: str    = Form(...),
           password: str = Form(...)):
    db       = SessionLocal()
    existing = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing:
        db.close()
        return templates.TemplateResponse(
            request=request,
            name="signup.html",
            context={"error": "Username or email already exists."}
        )

    user = User(username=username, email=email, password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    request.session["user_id"] = user.id
    db.close()
    return RedirectResponse("/", status_code=302)


# ── Login ────────────────────────────────────────────────
@app.get("/login")
def login_page(request: Request):
    if get_current_user(request):
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse(request=request, name="login.html", context={"error": None})


@app.post("/login")
def login(request: Request,
          username: str = Form(...),
          password: str = Form(...)):
    db   = SessionLocal()
    user = db.query(User).filter(
        User.username == username,
        User.password == hash_password(password)
    ).first()
    db.close()

    if not user:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Invalid username or password."}
        )

    request.session["user_id"] = user.id
    return RedirectResponse("/", status_code=302)


# ── Logout ───────────────────────────────────────────────
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=302)


# ── Add Expense ──────────────────────────────────────────
@app.post("/add")
def add_expense(request: Request,
                title: str    = Form(...),
                category: str = Form(...),
                amount: float = Form(...),
                latitude: str  = Form(default=""),
                longitude: str = Form(default="")):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse("/login", status_code=302)

    # safely parse lat/lng — empty string or invalid → None
    try:
        lat = float(latitude) if latitude.strip() else None
        lng = float(longitude) if longitude.strip() else None
    except ValueError:
        lat, lng = None, None

    db      = SessionLocal()
    expense = Expense(
        title=title,
        category=category,
        amount=amount,
        user_id=user_id,
        created_at=datetime.now(),
        latitude=lat,
        longitude=lng
    )
    db.add(expense)
    db.commit()
    db.close()
    return RedirectResponse("/", status_code=303)


# ── Delete Expense ───────────────────────────────────────
@app.get("/delete/{expense_id}")
def delete_expense(expense_id: int, request: Request):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse("/login", status_code=302)

    db      = SessionLocal()
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == user_id
    ).first()

    if expense:
        db.delete(expense)
        db.commit()
    db.close()
    return RedirectResponse("/", status_code=303)