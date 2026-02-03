from fastapi import FastAPI, Response, Cookie, Request
from fastapi.responses import JSONResponse
from typing import Annotated
import uuid
from datetime import datetime, timedelta
import json

app = FastAPI()

# Real-world use case 1: Session Management
@app.get("/login")
async def login(response: Response, username: str):
    """Create a session cookie when user logs in"""
    session_id = str(uuid.uuid4())
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,  # Prevents JavaScript access (XSS protection)
        secure=True,  # Only sent over HTTPS
        samesite="lax",  # CSRF protection
        max_age=3600  # 1 hour expiration
    )
    return {
        "message": f"User {username} logged in successfully",
        "session_id": session_id
    }

@app.get("/profile")
async def get_profile(session_id: Annotated[str | None, Cookie()] = None):
    """Read session cookie to authenticate user"""
    if not session_id:
        return {"error": "Not authenticated - please login"}
    return {
        "message": "User profile data",
        "session_id": session_id,
        "user": "John Doe",
        "email": "john@example.com"
    }

@app.get("/logout")
async def logout(response: Response):
    """Delete session cookie on logout"""
    response.delete_cookie("session_id")
    return {"message": "Logged out successfully"}


# Real-world use case 2: User Preferences/Theme
@app.get("/set-theme")
async def set_theme(response: Response, theme: str = "light"):
    """Save user's theme preference"""
    response.set_cookie(
        key="theme",
        value=theme,
        max_age=30*24*60*60  # 30 days
    )
    return {"message": f"Theme set to {theme}"}

@app.get("/get-theme")
async def get_theme(theme: Annotated[str | None, Cookie()] = "light"):
    """Retrieve user's theme preference"""
    return {"theme": theme}


# Real-world use case 3: Shopping Cart
@app.get("/add-to-cart")
async def add_to_cart(
    response: Response,
    product_id: int,
    cart: Annotated[str | None, Cookie()] = None
):
    """Add item to shopping cart stored in cookie"""
    cart_items = json.loads(cart) if cart else []
    cart_items.append(product_id)
    
    response.set_cookie(
        key="cart",
        value=json.dumps(cart_items),
        max_age=7*24*60*60  # 7 days
    )
    return {
        "message": f"Product {product_id} added to cart",
        "cart": cart_items
    }

@app.get("/view-cart")
async def view_cart(cart: Annotated[str | None, Cookie()] = None):
    """View shopping cart contents"""
    cart_items = json.loads(cart) if cart else []
    return {
        "cart_items": cart_items,
        "total_items": len(cart_items)
    }


# Real-world use case 4: User Language Preference
@app.get("/set-language")
async def set_language(response: Response, lang: str = "en"):
    """Set user's preferred language"""
    response.set_cookie(
        key="language",
        value=lang,
        max_age=365*24*60*60  # 1 year
    )
    return {"message": f"Language set to {lang}"}

@app.get("/welcome")
async def welcome(language: Annotated[str | None, Cookie()] = "en"):
    """Display welcome message in user's language"""
    messages = {
        "en": "Welcome to our website!",
        "es": "¡Bienvenido a nuestro sitio web!",
        "fr": "Bienvenue sur notre site web!",
        "de": "Willkommen auf unserer Website!"
    }
    return {"message": messages.get(language, messages["en"])}


# Real-world use case 5: Analytics/Tracking (GDPR-compliant)
@app.get("/accept-cookies")
async def accept_cookies(response: Response):
    """User accepts cookie consent"""
    response.set_cookie(
        key="cookie_consent",
        value="accepted",
        max_age=365*24*60*60  # 1 year
    )
    response.set_cookie(
        key="visitor_id",
        value=str(uuid.uuid4()),
        max_age=365*24*60*60
    )
    return {"message": "Cookie consent accepted"}

@app.get("/track-visit")
async def track_visit(
    cookie_consent: Annotated[str | None, Cookie()] = None,
    visitor_id: Annotated[str | None, Cookie()] = None
):
    """Track visitor only if consent given"""
    if cookie_consent == "accepted":
        return {
            "tracked": True,
            "visitor_id": visitor_id,
            "timestamp": datetime.now().isoformat()
        }
    return {"tracked": False, "message": "Consent required for tracking"}


# Real-world use case 6: Remember Me functionality
@app.get("/login-remember")
async def login_remember(
    response: Response,
    username: str,
    remember_me: bool = False
):
    """Login with optional 'remember me' feature"""
    session_id = str(uuid.uuid4())
    max_age = 30*24*60*60 if remember_me else 3600  # 30 days vs 1 hour
    
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=max_age
    )
    
    if remember_me:
        response.set_cookie(
            key="username",
            value=username,
            max_age=30*24*60*60
        )
    
    return {
        "message": f"User {username} logged in",
        "remember_me": remember_me,
        "session_duration": "30 days" if remember_me else "1 hour"
    }


# Real-world use case 7: Multiple cookies example
@app.get("/items/")
async def read_items(
    ads_id: Annotated[str | None, Cookie()] = None,
    session_id: Annotated[str | None, Cookie()] = None,
    theme: Annotated[str | None, Cookie()] = "light",
    language: Annotated[str | None, Cookie()] = "en"
):
    """Read multiple cookies at once"""
    return {
        "ads_id": ads_id,
        "session_id": session_id,
        "theme": theme,
        "language": language,
        "authenticated": session_id is not None
    }


# Real-world use case 8: Cookie security best practices
@app.get("/secure-login")
async def secure_login(response: Response, username: str):
    """Demonstrate secure cookie settings"""
    session_token = str(uuid.uuid4())
    
    # Session cookie with all security flags
    response.set_cookie(
        key="secure_session",
        value=session_token,
        httponly=True,      # Prevent XSS attacks
        secure=True,        # HTTPS only
        samesite="strict",  # Strict CSRF protection
        max_age=1800,       # 30 minutes
        domain=None,        # Current domain only
        path="/"            # Available throughout the site
    )
    
    return {
        "message": "Secure session created",
        "security_features": [
            "HttpOnly - XSS protection",
            "Secure - HTTPS only",
            "SameSite=Strict - CSRF protection",
            "Short expiration - 30 minutes"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)