#!/usr/bin/env python3
"""Place a Twilio outbound call that speaks a short PD-style message.

Requires env:
- TWILIO_ACCOUNT_SID
- TWILIO_AUTH_TOKEN
- TWILIO_FROM_NUMBER
- TWILIO_TO_NUMBER (default recipient)

Usage:
  python tools/twilio_call.py                # calls TWILIO_TO_NUMBER
  python tools/twilio_call.py +1415...       # calls provided number
  python tools/twilio_call.py --text "..."   # override spoken text
"""

import os, sys
import requests


def env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise SystemExit(f"Missing env var: {name}")
    return v


def main():
    sid = env("TWILIO_ACCOUNT_SID")
    token = env("TWILIO_AUTH_TOKEN")
    from_number = env("TWILIO_FROM_NUMBER")
    default_to = env("TWILIO_TO_NUMBER")

    to_number = default_to
    text = (
        "Ryan. It’s PD. Quick ping. "
        "Your next leverage move is: post the ten links thread, then publish the research agent starter kit on Gumroad. "
        "Reply here if you want me to queue the next three posts."
    )

    args = sys.argv[1:]
    if args:
        if args[0] == "--text":
            text = " ".join(args[1:]).strip()
        elif args[0].startswith("+"):
            to_number = args[0]
        elif args[0] in ("-h", "--help"):
            print(__doc__)
            return

    # Basic TwiML: say the message.
    twiml = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<Response>
  <Say voice=\"alice\">{text}</Say>
</Response>"""

    url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Calls.json"
    data = {
        "To": to_number,
        "From": from_number,
        "Twiml": twiml,
    }

    r = requests.post(url, data=data, auth=(sid, token), timeout=30)
    if r.status_code >= 300:
        raise SystemExit(f"Twilio error {r.status_code}: {r.text}")

    payload = r.json()
    print("Call initiated:", payload.get("sid"))


if __name__ == "__main__":
    main()
