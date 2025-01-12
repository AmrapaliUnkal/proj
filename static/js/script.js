const API_BASE = "http://127.0.0.1:8000"; // Update if your backend URL changes

// Sign In
document.getElementById("signinForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch(`${API_BASE}/login/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    if (response.ok) {
        // alert("Login successful!");
        window.location.href = "/option";
    } else {
        alert(data.detail || "Login failed");
    }
});

// Sign Up
document.getElementById("signupForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("newUsername").value;
    const password = document.getElementById("newPassword").value;

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
            room_number,  // Ensure this is passed as a string, as expected by the API
            check_in_date: new Date(check_in_date).toISOString(),  // Convert to ISO string
            check_out_date: new Date(check_out_date).toISOString(), // Convert to ISO string
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
// Check-out
document.getElementById("checkoutForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    // Get booking ID from the form
    const booking_id = parseInt(document.getElementById("booking_id").value); // Convert to integer

    // Log to verify that booking_id is correctly parsed
    console.log("Booking ID:", booking_id);

    // Check if booking_id is a valid number
    if (isNaN(booking_id)) {
        alert("Invalid Booking ID");
        return;
    }

    // Make the request to the backend
    const response = await fetch(`${API_BASE}/checkout/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ booking_id }), // Send as JSON
    });

    // Log the response for debugging
    const data = await response.json();
    console.log("Response data:", data);

    if (response.ok) {
        alert(`Room checked out successfully!`);
        window.location.href = "/"; // Redirect after successful check-out
    } else {
        alert(data.detail || "Checkout failed");
    }
});


// Function to fetch available rooms
const fetchAvailableRooms = async () => {
    const tableBody = document.querySelector("#roomsTable tbody");
    try {
        const response = await fetch(`${API_BASE}/rooms/`);
        if (!response.ok) {
            throw new Error("Failed to fetch rooms data");
        }

        const data = await response.json();
        const rooms = data.available_rooms;

        // Clear existing rows
        tableBody.innerHTML = "";

        // Populate table with room data
        rooms.forEach((room) => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${room.room_number}</td>
                <td>${room.category}</td>
                <td>$${room.price}</td>
                <td>${room.is_available ? "Available" : "Booked"}</td>
            `;

            // Optional: Add a click event to rows
            row.addEventListener("click", () => {
                alert(`Room ${room.room_number} selected!`);
            });

            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error fetching rooms:", error);
    }
};

// Fetch rooms when the page loads
document.addEventListener("DOMContentLoaded", () => {
    fetchAvailableRooms();
});


