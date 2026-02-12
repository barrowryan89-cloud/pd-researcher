#!/usr/bin/env python3
import json
import sys

def get_prices(slug):
    import urllib.request
    url = f"https://gamma-api.polymarket.com/events?slug={slug}"
    with urllib.request.urlopen(url) as resp:
        data = json.loads(resp.read())[0]
    
    market = data['markets'][0]
    prices = market.get('outcomePrices', ['N/A', 'N/A'])
    return {
        'question': market['question'],
        'yes': prices[0] if len(prices) > 0 else 'N/A',
        'no': prices[1] if len(prices) > 1 else 'N/A', 
        'volume24h': data.get('volume24hr', 0),
        'updated': data.get('updatedAt', 'N/A')
    }

markets = [
    'us-strikes-iran-by',
    'starmer-out-in-2025', 
    'will-trump-pardon-ghislaine-maxwell',
    'another-us-government-shutdown-by-february-14',
    'fed-decision-in-march-885'
]

for slug in markets:
    try:
        p = get_prices(slug)
        print(f"{slug}|{p['question']}|{p['yes']}|{p['no']}|{p['volume24h']}|{p['updated']}")
    except Exception as e:
        print(f"{slug}|ERROR|{e}")
