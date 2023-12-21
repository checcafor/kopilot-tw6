// select the elements with class "notifications"
const notifications = document.querySelector(".notifications");

// object containing details for different types of toasts (success, error, warning, info)
const toastDetails = {
    timer: 5000,                            // duration for which each toast will be displayed (5 seconds)
    success: {
        icon: 'fa-circle-check',            // icon class for success toast
    },
    error: {
        icon: 'fa-circle-xmark',            // icon class for error toast
    },
    warning: {
        icon: 'fa-triangle-exclamation',    // icon class for warning toast
    },
    info: {
        icon: 'fa-circle-info',             // icon class for info toast
    }
}

// function to remove a toast element
const removeToast = (toast) => {
    toast.classList.add("hide");                        // adding "hide" class to initiate CSS transition for hiding
    if(toast.timeoutId) clearTimeout(toast.timeoutId);  // clearing the timeout for the toast
    setTimeout(() => toast.remove(), 5000);             // removing the toast after 500ms
}

// function to create and display a toast
const createToast = (id, msg) => {
    const { icon } = toastDetails[id];              // getting the icon class and text for the toast based on the id passed
    const toast = document.createElement("li");     // creating a new 'li' element for the toast
    toast.className = `toast ${id}`;                // setting the classes for the toast
    // setting the inner HTML for the toast
    toast.innerHTML = `<div class="column">
                         <i class="fa-solid ${icon}"></i>
                         <span>${msg}</span>
                      </div>
                      <i class="fa-solid fa-xmark" onclick="removeToast(this.parentElement)"></i>`;
    notifications.appendChild(toast);   // append the toast to the notification ul
    // setting a timeout to remove the toast after the specified duration
    toast.timeoutId = setTimeout(() => removeToast(toast), toastDetails.timer);
}