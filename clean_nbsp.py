import re

# মূল কোড ফাইল
with open('bot.py', encoding='utf-8') as f:
    text = f.read()

# U+00A0 (non-breaking space) কে সাধারণ স্পেসে পরিবর্তন
cleaned = re.sub('\u00A0', ' ', text)

# নতুন ফাইলে লিখে রাখুন
with open('bot_fixed.py', 'w', encoding='utf-8') as f:
    f.write(cleaned)

print("Created bot_fixed.py without NBSP characters.")
