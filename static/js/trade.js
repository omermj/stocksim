//---------------------------
// Table Row Click Handle
//---------------------------

$(".trades-table button").on("click", handleTradeRowClick);

function handleTradeRowClick(e) {
  const tradeId = $(this).data().tradeId;

  window.location = `/trades/${tradeId}`;
}

