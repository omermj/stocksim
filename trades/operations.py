from flask import jsonify, g
from trades.models import Trade


class TradeOperations(object):
    """Utilities for trade operations"""

    @classmethod
    def enter_new_trade(cls, request):
        """Enters new trade based on JSON data received.

        Returns trade details if successful, else return error."""

        # Create the trade
        response = Trade.enter_trade(symbol=request.json["symbol"],
                                     trade_type=request.json["type"],
                                     qty=request.json["qty"],
                                     user_id=g.user.id)

        # If successful, return trade info as JSON, else return error as JSON
        if isinstance(response, Trade):
            return jsonify(response.to_dict())
        else:
            return jsonify(response)

    @classmethod
    def exit_trade(cls, trade_id):
        """Close trade by changing the trade status to close, updating the latest 
        price and exit date"""

        # Get trade
        trade = Trade.query.get(trade_id)

        # Close trade
        if trade.close():
            return jsonify({"result": "success"})
        else:
            return jsonify({"result": "error"})
