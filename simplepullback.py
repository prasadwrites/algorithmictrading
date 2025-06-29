// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// @version=5
strategy("Simple Pullback Strategy", 
     overlay=true, 
     initial_capital=10000,
     default_qty_type=strategy.cash, 
     default_qty_value=10000, // 100% of balance invested on each trade
     commission_type=strategy.commission.cash_per_contract, 
     commission_value=0.005) // Interactive Brokers rate

import AlphaCentauri66367/PineTradingbotWebhook/7 as tv //TBOT
webhookKey = "WebhookReceived:0b293b" //TBOT
//qty = input.int(title="Units", defval= 100 ,display = display.data_window) //TBOT


// Get user input
i_ma1           = input.int(title="MA 1 Length", defval=60, step=10, group="Strategy Parameters", tooltip="Long-term MA")
i_ma2           = input.int(title="MA 2 Length", defval=10, step=10, group="Strategy Parameters", tooltip="Short-term MA")
i_stopPercent   = input.float(title="Stop Loss Percent", defval=0.10, step=0.1, group="Strategy Parameters", tooltip="Failsafe Stop Loss Percent Decline")
i_lowerClose    = input.bool(title="Exit On Lower Close", defval=false, group="Strategy Parameters", tooltip="Wait for a lower-close before exiting above MA2")
i_startTime     = input.time(title="Start Filter", defval=timestamp("01 Jan 2024 13:30 +0000"), group="Time Filter", tooltip="Start date & time to begin searching for setups")
i_endTime       = input.time(title="End Filter", defval=timestamp("1 Jan 2099 19:30 +0000"), group="Time Filter", tooltip="End date & time to stop searching for setups")

// Get indicator values
ma1 = ta.sma(close, i_ma1)
ma2 = ta.sma(close, i_ma2)

// Check filter(s)
f_dateFilter = time >= i_startTime and time <= i_endTime

// Check buy/sell conditions
var float buyPrice = 0
buyCondition    = close > ma1 and close < ma2 and strategy.position_size == 0 and f_dateFilter
sellCondition   = close > ma2 and strategy.position_size > 0 and (not i_lowerClose or close < low[1])
stopDistance    = strategy.position_size > 0 ? ((buyPrice - close) / close) : na
stopPrice       = strategy.position_size > 0 ? buyPrice - (buyPrice * i_stopPercent) : na
stopCondition   = strategy.position_size > 0 and stopDistance > i_stopPercent

var int qty = 0
// Enter positions
if buyCondition[1]
    buyPrice := close
    qty := math.floor(10000/buyPrice)
    msg = tv.makeWebhookJson(webhookKey,"SimplePullBackStrategy_Long", 'strategy.entrylong', qty) //TBOT
    strategy.entry(id="Long",  direction=strategy.long,  alert_message = msg)
 



// Exit positions
if sellCondition or stopCondition
    //qty := int( math.abs ( strategy.position_size) )
    msg = tv.makeWebhookJson(webhookKey,"SimplePullBackStrategy_Exit", 'strategy.entryshort', qty) //TBOT
    strategy.close(id="Long",  comment="Exit" + (stopCondition ? "SL=true" : ""), alert_message=msg)




// Draw pretty colors
plot(buyPrice, color=color.lime, style=plot.style_linebr)
plot(stopPrice, color=color.red, style=plot.style_linebr, offset=-1)
plot(ma1, color=color.blue)
plot(ma2, color=color.orange)