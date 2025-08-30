import { putAlertInCookie, showAlertFromCookie } from "../../static/js/alert.js";

//---------------------------
// Trade Close Button Click
//---------------------------

$("#close-trade-btn").on("click", handleTradeClose);

async function handleTradeClose(e) {
  e.preventDefault();

  const tradeId = $(this).data().tradeId;
  const prefix = window.APP_PREFIX || "";
  const response = await axios.put(`${prefix}/trades/${tradeId}/close`);

  // Hide modal
  $("#closeTradeModal").modal("hide");

  // Store the alert message and type in a cookie
  // Based on response, store the alert message and type in a cookie

  if (response.data.result === "success") {
    putAlertInCookie("The trade is successfully closed.", "success");
  } else {
    putAlertInCookie(
      "An error occurred while closing the trade. Please try again.",
      "danger"
    );
  }

  // if (response.data.result === "success") {
  //   localStorage.setItem("alertMessage", "The trade is successfully closed.");
  //   localStorage.setItem("alertType", "alert-success");
  // } else {
  //   localStorage.setItem(
  //     "alertMessage",
  //     "An error occurred while closing the trade. Please try again."
  //   );
  //   localStorage.setItem("alertType", "alert-danger");
  // }

  // Reload the page
  location.reload();
}

// Retrieve the alert message from the cookie and display it
showAlertFromCookie();
// let alertMessage = localStorage.getItem("alertMessage");
// let alertType = localStorage.getItem("alertType");

// if (alertMessage) {
//   $("#alert").text(alertMessage);
//   $("#alert").addClass(alertType);
//   $("#alert").show();

//   // Clear the error message from the cookie or local storage
//   localStorage.removeItem("alertMessage");
//   localStorage.removeItem("alertType");
// }
