// New Trade Form Submission
$("#new-trade-form").on("submit", handleNewTradeSubmission);

// Handle form submission
async function handleNewTradeSubmission(e) {
  e.preventDefault();

  // Make POST request to enter new trade
  const response = await axios.post("/trades/new", {
    symbol: $("#symbol").val(),
    type: $("input[name='type']:checked").val(),
    qty: parseInt($("#qty").val()),
  });

  // If trade is entered successfully
  if (response.data.result !== "unsuccessful") {
    const trade = response.data;
    $("#trade-response").text(
      `The trade is successfully placed. Bought ${trade.qty} shares of 
      ${trade.symbol} at $${trade.entry_price} (Ticket# ${trade.trade_id})`
    );
    $("#trade-response").addClass("text-success");
    $("#enter-trade-output").removeClass("d-none");

    // reset form
    $("#new-trade-form").trigger("reset");
  }
  // In case of an error
  else {
    $("#trade-response").text(
      "An error occured while entering the trade. Please try again later."
    );
    $("#trade-response").addClass("text-danger");
    $("#enter-trade-output").removeClass("d-none");
  }
}
