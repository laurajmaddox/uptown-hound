# ===============================================
# shop/constants.py
# ===============================================


# List of country codes eligible for domestic shipping rates
DOMESTIC_SHIP_NATIONS = [
    'AS', 'CA', 'FM', 'GU', 'MH', 'MP', 'PR', 'PW', 'US', 'VI',
]

# Domestic shipping rate ranges
DOMESTIC_SHIP_RATES = (
    (100, 9), (75, 7), (50, 6), (25, 5), (0, 3),
)

# International shipping rate ranges
INTL_SHIP_RATES = (
    (100, 12), (75, 10), (50, 9), (25, 8), (0, 5),
)

# Status choices for Order model
ORDER_STATUS_CHOICES = (
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
)
