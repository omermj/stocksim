//---------------------------
// Table Row Click Handle
//---------------------------

$(".trades-table button").on("click", handleTradeRowClick);

function handleTradeRowClick(e) {
  const tradeId = $(this).data().tradeId;
  const prefix = window.APP_PREFIX || "";

  window.location = `${prefix}/trades/${tradeId}`;
}
