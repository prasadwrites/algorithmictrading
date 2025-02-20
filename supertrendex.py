//@version=6
strategy("Supertrend Strategy EX", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=15)

atrPeriod = input(10, "ATR Length")
factor = input.float(3.0, "Factor", step = 0.01)

import AlphaCentauri66367/PineTradingbotWebhook/7 as tv //TBOT
webhookKey = "WebhookReceived:0b293b" //TBOT
qty = 10 //TBOT

[_, direction] = ta.supertrend(factor, atrPeriod)




if ta.change(direction) < 0
    msg = tv.makeWebhookJson(webhookKey,"Long#1", 'strategy.entrylong',qty) //TBOT
    strategy.entry("My Long Entry Id", strategy.long, alert_message = msg)

if ta.change(direction) > 0
    msg1 = tv.makeWebhookJson(webhookKey,"Short#1", 'strategy.entryshort',qty) //TBOT
    strategy.entry("My Short Entry Id", strategy.short, alert_message = msg1)

//plot(strategy.equity, title="equity", color=color.black, linewidth=2, style=plot.style_areabr)
