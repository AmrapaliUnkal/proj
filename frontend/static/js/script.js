const API_BASE = "http://127.0.0.1:8000"; // Update if your backend URL changes

// Sign In
document.getElementById("signinForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch(`${API_BASE}/login/`, {  // Corrected the endpoint to match login
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    if (response.ok) {
        alert("Login successful!");
        window.location.href = "/";
    } else {
        alert(data.detail || "Login failed");
    }
});

// Sign Up
document.getElementById("signupForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch(`${API_BASE}/signup/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    if (response.ok) {
        alert("User signed up successfully!");
        window.location.href = "/signin";
    } else {
        alert(data.detail || "Sign-up failed");
    }
});

// Booking a Room
document.getElementById("bookRoomForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const room_number = document.getElementById("room_number").value;
    const check_in_date = document.getElementById("check_in_date").value;
    const check_out_date = document.getElementById("check_out_date").value;

    const response = await fetch(`${API_BASE}/book/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            username,
            room_number,
            check_in_date: new Date(check_in_date).toISOString(),
            check_out_date: new Date(check_out_date).toISOString(),
        }),
    });

    const data = await response.json();
    if (response.ok) {
        alert(`Room ${room_number} booked successfully!`);
        window.location.href = "/"; // Redirect after successful booking
    } else {
        alert(data.detail || "Booking failed");
    }
});

// Check-out
document.getElementById("checkoutForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const booking_id = document.getElementById("booking_id").value;

    const response = await fetch(`${API_BASE}/checkout/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: { "booking_id":booking_id },
    });

    const data = await response.json();
    if (response.ok) {
        alert(`Room checked out successfully!`);
        window.location.href = "/"; // Redirect after successful check-out
    } else {
        alert(data.detail || "Checkout failed");
    }
});
