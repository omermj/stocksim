//---------------------------
// Trade Enter
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
  const response = await axios.post("/trades/", {
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
      $("#trade-response").text(response.data.error);
      $("#trade-response").addClass("text-danger");
      $("#enter-trade-output").removeClass("d-none");
    }
  }

  // Else, show the trade entry results
  else {
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
}

//---------------------------
// Trade Exit
//---------------------------

$("#portfolio-table").on("click", "#trade-exit-btn", handleTradeExit);

async function handleTradeExit(e) {
  e.preventDefault();

  // Get the Trade ID
  const tradeId = $(this).data().tradeId;

  // Send PUT rquest to exit trade
  const response = await axios.put(`/trades/${tradeId}`);

  // If successful, update portfolio and closed trades
  if (response.data["result"] === "successful") {
    // Update recent trades and closed posiitons table
    $(this).parents("tr").remove();
    addClosedTrade(response.data);

    // Update account metrics
    const userId = response.data["user_id"];
    const userInfo = await axios.get(`/users/${userId}/info`);
    console.log(userInfo);
    $("#account-balance").html(parseCurrency(userInfo.data["account_balance"]));
    $("#equity").html(parseCurrency(userInfo.data["equity"]));
    $("#buying-power").html(parseCurrency(userInfo.data["margin_available"]));
    $("#realized-gain").html(parseCurrency(userInfo.data["realized_gain"]));
    $("#unrealized-gain").html(parseCurrency(userInfo.data["unrealized_gain"]));
  }
}

function addClosedTrade(trade) {
  const $tr = `<tr>
                <td>
                  ${trade.trade_id}
                </td>
                <td>
                  ${moment(trade.exit_date)
                    .utc()
                    .format("YYYY/MM/DD - hh:mm A")}
                </td>
                <td class="text-center">
                  ${trade.symbol}
                </td>
                <td class="text-center">
                  ${trade.type}
                </td>
                <td class="text-center">
                  ${trade.qty}
                </td>
                <td class="text-center">
                  ${trade.entry_price}
                </td>
                <td class="text-center">
                  ${trade.exit_price}
                </td>
                <td class="text-center">
                  ${trade.pnl}
                </td>
              </tr>`;

  $("#tbody-closed-trades").append($tr);
}

function parseCurrency(num) {
  return (
    "$" +
    num.toLocaleString("en-US", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })
  );
}
