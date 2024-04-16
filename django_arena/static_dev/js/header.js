header_notifications_button = document.getElementById("header-notifications-button")
header_notifications_menu_list = document.getElementById("menu-header-notifications-list")

notifications = document.querySelectorAll(".menu-header__notifications-list__remove")

for (let i = 0; i < notifications.length; i++) {
    notifications[i].addEventListener("click", (e) => {
        let listItem = notifications[i].closest('li');
        listItem.parentNode.removeChild(listItem);
        const url = "http://" + window.location.host + "/" + "notifications/delete/" + notifications[i].getAttribute("data-delete")
        const options = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        };
        fetch(url, options)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    })
}

header_notifications_button.addEventListener("click", (e) => {
    let cur = header_notifications_menu_list.style.display
    if (cur === "block") {
        header_notifications_menu_list.style.display = "none"
    } else {
        header_notifications_menu_list.style.display = "block"
    }
})