import random

random.seed(42)

ADMIN_USERNAMES = ['admin_Pik', 'admin_andreas', 'admin_BigNick', 'stefadmin', 'friday_admin', 'mlazoy_as_admin']
ADMIN_PASSWORDS = ['admin1', 'admin2', 'admin3', 'admin4', 'admin5', 'admin6']

ADMIN_USERNAME, ADMIN_PASSWORD = random.choice(list(zip(ADMIN_USERNAMES, ADMIN_PASSWORDS)))

