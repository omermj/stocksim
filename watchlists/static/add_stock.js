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
  console.log(response);

  // If error, display the msg else add symbol to the table
  if (response.data.error) {
    $("#stock-error").text(response.data.error);
    $("#stock-error").show();
    return;
  } else {
    const stock = response.data.stock;
    addStockToTable(stock);
    $("#no-stock-text").hide();
    $("#stocks-table").show();
    $("#stock-error").hide();
    $("#stock-input").val("");


  }
}

function addStockToTable(stock) {
  const $stock = $(
    `<tr data-stock-id="${stock.id}">
                    <td class="text-center">${stock.symbol}</td>
                    <td class="text-center">${stock.name}</td>
                    <td class="text-center">${stock.price}</td>
                    <td class="text-center">
                      <button class="btn btn-primary btn-sm">Trade</button>
                    </td>
                    <td class="text-center">
                      <button class="btn btn-danger btn-sm">Remove</button>
                    </td>
                  </tr>`
  );
  $(".watchlist-table").append($stock);
}
