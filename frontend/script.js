let userId = null;

function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch("http://localhost:5000/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            userId = data.user_id;
            window.location.href = "dashboard.html";
        } else {
            document.getElementById("msg").innerText = data.message;
        }
    });
}

function placeOrder() {
    const item = document.getElementById("item").value;
    fetch("http://localhost:5000/order", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({user_id: userId, item})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("notification").innerText = data.message;
        fetchOrders();
    });
}

function fetchOrders() {
    fetch(`http://localhost:5000/orders/${userId}`)
    .then(res => res.json())
    .then(data => {
        const ordersList = document.getElementById("orders");
        ordersList.innerHTML = "";
        data.orders.forEach(order => {
            const li = document.createElement("li");
            li.innerText = order;
            ordersList.appendChild(li);
        });
    });
}

window.onload = function() {
    if (userId) fetchOrders();
}

