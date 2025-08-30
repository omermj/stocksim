import {
  putAlertInCookie,
  showAlertFromCookie,
  hideAlert,
  showAlert,
} from "../../static/js/alert.js";

$(".watchlist-table").on("click", ".trade-btn", tradeRequest);

async function tradeRequest(e) {
  e.preventDefault();

  // Hide alerts and errors
  $("#stock-error").hide();
  hideAlert();

  // Get watchlist and stock id
  const stockId = $(this).parents("tr").data().stockId;
  const prefix = window.APP_PREFIX || "";
  window.location.href = `${prefix}/trades/new?stockid=${stockId}`;
}
