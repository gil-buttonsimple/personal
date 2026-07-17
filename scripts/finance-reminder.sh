#!/bin/bash
# Monthly finance ritual reminder. Self-clearing.
#
# Fires ONLY when the ritual is actually outstanding: on/after the 10th of the
# month, with no snapshot row in finance-balances.csv dated this month. Doing
# the snapshot IS the acknowledgment -- there is no "done" button, and a done
# ritual silently stops the nagging.
#
# Runs daily; escalates by persisting. Ten weeks of silence becomes impossible.
# See finance-obligations.md. No autopay on cards (deliberate), so this is the
# only thing standing between the founder and a missed payment.

CSV="/home/gil/dev/personal/finance-balances.csv"
DAY_OF_MONTH=10

day=$(date +%-d)
month=$(date +%Y-%m)

[ "$day" -lt "$DAY_OF_MONTH" ] && exit 0
[ -r "$CSV" ] || { logger -t finance-reminder "CSV unreadable: $CSV"; exit 1; }

# Already done this month? Stay quiet.
if cut -d, -f1 "$CSV" | grep -q "^$month-"; then
  exit 0
fi

overdue=$(( day - DAY_OF_MONTH ))
if [ "$overdue" -eq 0 ]; then
  urgency="normal"; when="Due today."
else
  urgency="critical"; when="${overdue} day(s) overdue."
fi

notify-send -u "$urgency" -t 20000 \
  "Finance: monthly ritual" \
  "$when Pull balances + pay the two cards (BofA 6657, WF 3834). No autopay -- nothing else catches this."
paplay /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null
logger -t finance-reminder "fired: $month not snapshotted, $overdue day(s) past the ${DAY_OF_MONTH}th"
