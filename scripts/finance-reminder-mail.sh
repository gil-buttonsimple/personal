#!/bin/bash
# Baobab-independent monthly finance reminder. Emails via Resend (curl).
# Source of truth for this file: personal repo scripts/finance-reminder-mail.sh.
# Fires on the 10th (systemd timer). Per-month stamp guards against double-send.
# No repo/CSV check by design: keeps zero git credentials on the cloud droplet.
KEYFILE=~/.config/finance-reminder/resend_key
STAMP=~/.config/finance-reminder/last-sent
TO="gil@buttonsimple.com"
month=$(date +%Y-%m)
[ -r "$KEYFILE" ] || { logger -t finance-reminder "no key"; exit 1; }
[ "$(cat "$STAMP" 2>/dev/null)" = "$month" ] && exit 0   # already sent this month
KEY=$(cat "$KEYFILE")
body="It is the 10th: monthly finance ritual.\n\n- Pull current balances (all accounts).\n- Pay both cards IN FULL: BofA ...6657 and Wells Fargo ...3834. No autopay, so nothing else catches a miss.\n- USAA Bill Pay takes days to settle; pay now, not near the due date.\n\nDetails: personal repo finance-obligations.md.\nSent from mesquite (baobab-independent)."
code=$(curl -s -o /tmp/fr-resp -w "%{http_code}" -X POST https://api.resend.com/emails \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d "{\"from\":\"Button Simple <support@buttonsimple.com>\",\"to\":[\"$TO\"],\"subject\":\"Finance: monthly ritual (pull balances + pay both cards)\",\"text\":\"$(printf "%b" "$body")\"}")
if [ "$code" = "200" ]; then echo "$month" > "$STAMP"; logger -t finance-reminder "sent $month"; else logger -t finance-reminder "FAILED http=$code $(cat /tmp/fr-resp)"; exit 1; fi
