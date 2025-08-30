//---------------------------
// Trade Entry
//---------------------------

// New Trade Form Submission
$("#new-trade-form").on("submit", handleNewTradeSubmission);

// Handle form submission
async function handleNewTradeSubmission(e) {
  e.preventDefault();

  // Hide all previous errors
  $("#symbol-error").addClass("d-none");
  $("#qty-error").addClass("d-none");
  $("#enter-trade-output").addClass("d-none");

  // Make POST request to enter new trade
  const prefix = window.APP_PREFIX || "";
  const response = await axios.post(`${prefix}/trades/new`, {
    symbol: $("#symbol").val(),
    type: $("input[name='type']:checked").val(),
    qty: parseInt($("#qty").val()),
  });

  // If there is an error from server, show it on page:
  if ("error" in response.data) {
    if (response.data.error.type === "symbol") {
      $("#symbol-error").text(response.data.error.message);
      $("#symbol-error").removeClass("d-none");
    }
    if (response.data.error.type === "qty") {
      $("#qty-error").text(response.data.error.message);
      $("#qty-error").removeClass("d-none");
    }
    if (response.data.error.type === "others") {
      $("#other-error").text(response.data.error.message);
      $("#other-error").removeClass("d-none");
    }
  }

  // Else, show the trade entry results
  else {
    const trade = response.data;
    const tradeType = trade.type === "buy" ? "Bought" : "Sold";
    $("#trade-response").text(
      `The trade is successfully placed. ${tradeType} ${trade.qty} shares of
      ${trade.symbol} at $${trade.entry_price} (Ticket# ${trade.trade_id})`
    );
    $("#confirmationModal").modal("show");

    // reset form
    $("#new-trade-form").trigger("reset");
  }
}
