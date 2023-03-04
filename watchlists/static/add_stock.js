$("#add-stock-btn").on("click", handleAddStock);

async function handleAddStock(e) {
  e.preventDefault();

  // Hide errors
  $("#stock-error").hide();

  // Get the symbol name
  if (!$("#stock-input").val()) {
    $("#stock-error").text("Please enter a stock symbol.");
    $("#stock-error").show();
    return;
  }
  const stockSymbol = $("#stock-input").val();
  const watchlistId = $("#stock-input").data().watchlistId;

  // Make POST request to add stock to watchlist
  const response = await axios.post(`/watchlists/${watchlistId}/addstock`, {
    symbol: stockSymbol,
  });

  // If error, display the msg. Else add symbol to the table
  if (response.data.error) {
    $("#stock-error").text(response.data.error);
    $("#stock-error").show();
    return;
  } else {
    const stock = response.data.stock;
    addStockToTable(stock);
    $("#no-stock-text").hide(); // Hide no stock msg
    $("#stocks-table").show(); // Show stocks table if hidden
    $("#stock-error").hide(); // Hide previous symbol errors
    $("#stock-input").val(""); // Set Add Symbol input to blank
  }
}

/**Add stock to watchlist stocks table */
function addStockToTable(stock) {
  const $stock = $(
    `<tr data-stock-id=${stock.id} data-watchlist-id=${stock.watchlist_id}>
      <td class="text-center">${stock.symbol}</td>
      <td class="text-center">${stock.name}</td>
      <td class="text-center">${stock.price}</td>
      <td class="text-center">
        <button class="btn btn-primary btn-sm">Trade</button>
      </td>
      <td class="text-center">
        <button class="btn btn-danger btn-sm btn-sm remove-stock-btn">Remove</button>
      </td>
    </tr>`
  );
  $(".watchlist-table").append($stock);
}
