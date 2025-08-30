import {
  putAlertInCookie,
  showAlertFromCookie,
  hideAlert,
  showAlert,
} from "../../static/js/alert.js";

$(".watchlist-table").on("click", ".remove-stock-btn", handleRemoveStock);

async function handleRemoveStock(e) {
  e.preventDefault();

  // Hide alerts and errors
  $("#stock-error").hide();
  hideAlert();

  // Get watchlist and stock id
  const watchlistId = $(this).parents("tr").data().watchlistId;
  const stockId = $(this).parents("tr").data().stockId;

  // Make a DELETE request
  const prefix = window.APP_PREFIX || "";
  const response = await axios.delete(
    `${prefix}/watchlists/${watchlistId}/removestock/${stockId}`
  );

  // If error, display results
  if (response.data.error) {
    showAlert(
      "Error removing stock from watchlist. Please refresh the page and try again.",
      "danger"
    );
  } else {
    // Else remove stock from watchlist
    $(this).parents("tr").remove();

    // If no other items in watchlist, hide table and show No stocks label
    if ($(".watchlist-table tr").length === 0) {
      $("#stocks-table").hide();
      $("#no-stock-text").show();
    }
  }
}
