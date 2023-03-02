//---------------------------
// Alert functions
//---------------------------

// Short Alert
export function showAlert(msg, category) {
  $("#alert-msg").text(msg);
  $("#alert").addClass("alert-" + category);
  $("#alert").show();
}

// Hide Alert
export function hideAlert() {
  $("#alert").hide();
}

// Put alert message and type in cookie
export function putAlertInCookie(msg, category) {
  localStorage.setItem("alertMessage", msg);
  localStorage.setItem("alertType", category);
}

// Get alert message and type from cookie
export function showAlertFromCookie() {
  const alertMessage = localStorage.getItem("alertMessage");
  const alertType = localStorage.getItem("alertType");

  // If alert exists in cookie, show and delete cookie
  if (alertMessage) {
    // Clear the error message from the cookie and return
    showAlert(alertMessage, alertType)
    localStorage.removeItem("alertMessage");
    localStorage.removeItem("alertType");
  }
}
