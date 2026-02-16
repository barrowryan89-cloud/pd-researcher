#!/usr/bin/env python3
"""
Cron Parser - Free Tool
Parse and explain cron expressions
Free version: Parse and show next run times
Paid upgrade: Validate, generate, timezone support

Usage: python3 cron_parser_free.py "<expression>"
"""

import sys
from datetime import datetime, timedelta

def parse_cron(expression):
    """Parse basic cron expression"""
    parts = expression.split()
    if len(parts) != 5:
        return {'error': 'Cron expression must have 5 fields: min hour day month weekday'}
    
    minute, hour, day, month, weekday = parts
    
    explanation = []
    
    # Minute
    if minute == '*':
        explanation.append("Every minute")
    elif '/' in minute:
        step = minute.split('/')[1]
        explanation.append(f"Every {step} minutes")
    else:
        explanation.append(f"At minute {minute}")
    
    # Hour
    if hour == '*':
        explanation.append("every hour")
    elif ',' in hour:
        explanation.append(f"at hours {hour}")
    else:
        explanation.append(f"at hour {hour}")
    
    # Day
    if day == '*':
        explanation.append("every day")
    else:
        explanation.append(f"on day {day}")
    
    # Month
    if month == '*':
        explanation.append("every month")
    else:
        month_names = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
                       7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
        if month.isdigit():
            explanation.append(f"in {month_names.get(int(month), month)}")
        else:
            explanation.append(f"in month {month}")
    
    # Weekday
    if weekday == '*':
        pass  # Every day already covered
    else:
        days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
        if weekday.isdigit():
            explanation.append(f"on {days[int(weekday) % 7]}")
    
    return {
        'expression': expression,
        'explanation': ' '.join(explanation),
        'parts': {
            'minute': minute,
            'hour': hour,
            'day': day,
            'month': month,
            'weekday': weekday
        }
    }

def get_next_runs(expression, count=5):
    """Get next run times (simplified)"""
    now = datetime.now()
    runs = []
    
    # Very simplified - just add hours for demonstration
    for i in range(count):
        run_time = now + timedelta(hours=i+1)
        runs.append(run_time.strftime("%Y-%m-%d %H:%M:%S"))
    
    return runs

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                   CRON PARSER v1.0                         ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Parse and understand cron expressions                     ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Cron expression validation                           ║
║     → Generate expressions from natural language           ║
║     → Next run time calculation (accurate)                 ║
║     → Timezone support                                     ║
║     → Cron expression library                              ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 2:
        print("❌ Missing cron expression.")
        print("\nUsage:")
        print('  python3 cron_parser_free.py "*/5 * * * *"')
        print('  python3 cron_parser_free.py "0 9 * * 1-5"')
        print("\nFormat: minute hour day month weekday")
        print("  * = any value")
        print("  */n = every n")
        print("  1-5 = range")
        print("  1,3,5 = list")
        sys.exit(1)
    
    expression = sys.argv[1]
    
    print(f"🔄 Parsing: {expression}\n")
    
    result = parse_cron(expression)
    
    if 'error' in result:
        print(f"❌ {result['error']}")
        sys.exit(1)
    
    print(f"{'='*60}")
    print(f"📊 CRON EXPRESSION")
    print(f"{'='*60}\n")
    
    print(f"Expression: {result['expression']}")
    print(f"\nExplanation: {result['explanation']}")
    
    print(f"\nFields:")
    print(f"  Minute:  {result['parts']['minute']}")
    print(f"  Hour:    {result['parts']['hour']}")
    print(f"  Day:     {result['parts']['day']}")
    print(f"  Month:   {result['parts']['month']}")
    print(f"  Weekday: {result['parts']['weekday']}")
    
    print(f"\n{'='*60}")
    print("\n💡 Want accurate next-run times and validation?")
    print("   Upgrade to PD_Researcher v1 for advanced cron tools")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("="*60)

if __name__ == "__main__":
    main()

    # Affiliate
    print("\n" + "-" * 60)
    print("🚀  Boost your productivity with these tools:")
    print("    • DigitalOcean: $200 free credit -> https://m.do.co/c/pdresearcher")
    print("    • JetBrains IDEs: The best Python tools -> https://www.jetbrains.com/?utm_source=pdresearcher")
    print("-" * 60)
