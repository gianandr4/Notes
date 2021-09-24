import requests,random

# def roulette(bet='black',wager=1):
#     payload = {'bet': bet, 'wager': wager}
#     url = 'https://www.roulette.rip/api/play'
#     x = requests.get(url=url, params=payload).json()
#     return float(x['bet']['payout'])

def roulette(wager=1):
    pockets = ["Red"] * 18 + ["Black"] * 18 + ["Green"] * 2
    roll = random.choice(pockets)
    if roll == "Red":
        return wager*2
    else:
        return 0

# bet: odd, even, low, high, red, black, green, or [0 through 36]
# wager: any number

def martingale(wager,goal,limit=False):
    bank = float(wager)
    temp_wager = float(wager)
    history = []
    while bank < goal:
        if limit:
            if bank<-limit or bank == -limit:break
        # DEDUCT CURRENT WAGEr
        bank -= temp_wager
        outcome = roulette(wager=temp_wager)
        bank+= float(outcome)
        if outcome == 0:
            temp_wager = temp_wager*2
            history.append({'status':'LOSE','wager':wager,'outcome':outcome,'bank':bank})
        else:
            temp_wager=float(wager)
            history.append({'status':'WIN ','wager':wager,'outcome':outcome,'bank':bank})
        print(history[-1])
    print('MARTINGALE',bank)
    return bank

def grand_martingale(wager,goal,limit=False):
    bank = float(wager)
    temp_wager = float(wager)
    history = []
    while bank < goal:
        if limit:
            if bank<-limit or bank == -limit:break
        # DEDUCT CURRENT WAGEr
        bank -= temp_wager
        outcome = roulette(wager=temp_wager)
        bank+= float(outcome)
        if outcome == 0:
            temp_wager = temp_wager*2 +wager
            history.append({'status':'LOSE','wager':wager,'outcome':outcome,'bank':bank})
        else:
            temp_wager=float(wager)
            history.append({'status':'WIN ','wager':wager,'outcome':outcome,'bank':bank})
        # print(history[-1])
    # print('     GRAND',bank)
    return bank


# mart=martingale(1,100)
# grnt = grand_martingale(1,100)

def main():
    bank = 0
    mart=0
    grnt=0
    for month in range(12):
        for day in range(30):
            # print('\nDAY: {}    '.format(day),end='')
            # mart = martingale(0.5, 1,limit=3)
            grnt = grand_martingale(5, 10,limit=35)
            bank += mart+grnt
        print('MONTHLY: ', bank)

    print('\nYEARLY: ',bank,'\n\n')
    return bank



amount = 100.0

for i in range(10):
    x=main()
    amount=amount+x
print(amount)





















