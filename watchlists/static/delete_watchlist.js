import { putAlertInCookie, showAlertFromCookie } from "/static/js/alert.js";

//---------------------------
// Delete Watchlist Handler
//---------------------------

$("#delete-watchlist-btn").on("click", handleWatchlistDelete);

async function handleWatchlistDelete(e) {
  e.preventDefault();

  // Get watchlist id
  const watchlistId = $(this).data().watchlistId;

  // Make DELETE request to server
  const prefix = window.APP_PREFIX || "";
  const response = await axios.delete(`${prefix}/watchlists/${watchlistId}`);

  // Hide modal
  $("#deleteWatchlist").modal("hide");

  // Based on response, store the alert message and type in a cookie
  if (response.data.result === "success") {
    putAlertInCookie("The watchlist is successfully deleted.", "success");
  } else {
    putAlertInCookie(
      "An error occurred while deleting the watchlist. Please try again.",
      "danger"
    );
  }

  // Reload the page
  window.location.href = `${prefix}/watchlists`;
}

// Retrieve the alert message from cookie and display it
showAlertFromCookie();
