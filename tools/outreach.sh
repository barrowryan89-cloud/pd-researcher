#!/bin/bash
# Outreach Automation Script
# Usage: ./outreach.sh <platform> <message_file>

PLATFORM=$1
MESSAGE_FILE=$2

if [ -z "$PLATFORM" ] || [ -z "$MESSAGE_FILE" ]; then
    echo "Usage: $0 <platform> <message_file>"
    echo "Platforms: twitter, reddit, discord, email"
    echo "Example: $0 twitter content/twitter_thread_airdrop_farming.txt"
    exit 1
fi

echo "📤 Outreach Automation"
echo "======================"
echo "Platform: $PLATFORM"
echo "Message: $MESSAGE_FILE"
echo ""

if [ ! -f "$MESSAGE_FILE" ]; then
    echo "❌ Message file not found: $MESSAGE_FILE"
    exit 1
fi

echo "📝 Message Preview:"
echo "---"
head -20 "$MESSAGE_FILE"
echo "---"
echo ""

case $PLATFORM in
    twitter)
        echo "🐦 Twitter Actions:"
        echo "  1. Copy text from $MESSAGE_FILE"
        echo "  2. Post as thread (split at 280 chars)"
        echo "  3. Pin first tweet"
        echo "  4. Reply to comments within 1 hour"
        echo "  5. Retweet after 12 hours"
        ;;
    reddit)
        echo "📱 Reddit Actions:"
        echo "  1. Post to r/CryptoCurrency at 8-10 AM EST"
        echo "  2. Cross-post to r/Solana"
        echo "  3. Respond to comments immediately"
        echo "  4. Edit with link after 6 hours if popular"
        ;;
    discord)
        echo "💬 Discord Actions:"
        echo "  1. Join Solana/AI agent servers"
        echo "  2. Post in relevant channels"
        echo "  3. DM interested users"
        echo "  4. Don't spam - add value first"
        ;;
    email)
        echo "📧 Email Actions:"
        echo "  1. Load contact list"
        echo "  2. Personalize each email"
        echo "  3. Send in batches (avoid spam filters)"
        echo "  4. Track opens/clicks"
        ;;
    *)
        echo "❌ Unknown platform: $PLATFORM"
        exit 1
        ;;
esac

echo ""
echo "✅ Ready for human execution"
