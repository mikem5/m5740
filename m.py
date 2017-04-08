import math
import random
import time
import matplotlib.pyplot as plt



# global timer
timer = 0
maxbooth = 100


ct = []
cust = []
active = []
booths = []



class customer(object):


    def __init__(self, ident, spending,chance,wait):
        self.ident = ident
        self.spending = spending
        self.inqueue = 0
        self.chance = chance
        self.location = 0
        self.wait = wait



    def check(self):
        return self.location, self.spending, self.inqueue

    def sale(self):
        self.spending -= 1
        self.inqueue = 0
        if self.spending > 0:
            self.location += 1
        # left
        else:
            self.location = maxbooth + 1

    def move(self):
        if self.inqueue == 0:
            #chance to enter current line
            if random.random() < self.chance:
                return True
            else:
                self.location += 1
                return False
        else:
            return False


class booth(object):
    global timer


    def __init__(self,location,betarate):
        self.location = location
        self.queue = []
        self.sales = 0
        self.rate = betarate
        self.oalpha = []


        # time till next serve
        self.beta = random.expovariate(self.rate)




    # adds customer object to queue
    def addcust(self,customer):
        self.queue.append(customer)
        customer.inqueue = 1

    # checks to see if served customer
    def update(self):
        if len(self.queue) > 0:
            # sale occus
            if self.beta <= timer:
                self.sales += 1
                self.queue[0].sale()
                self.queue.pop(0)


                # set next service time
                self.beta += random.expovariate(self.rate)

    # had a customer 'visit' so add time to oalpha
    def touch(self):
        self.oalpha.append(timer)


    # returns avg of times
    def obsalpha(self):
        if len(self.oalpha) == 0:
            return 0
        else:
            return sum(self.oalpha)/len(self.oalpha)






def inittrial(spending, chance, wait, betarate):
    global ct
    global cust, active, booths


    # rate at customers appear to booth 0
    # beta alpha rates would be say 1/rate so 
    # for .5 = 2 = lambda or .1 = 10
    # this means avg is 10 'time units' till next event
    alpha = .5




    #makes times, this is same as # of customers
    ct = []
    t = 0
    for x in range(1000):
        t+= random.expovariate(alpha)
        ct.append(t)



    #make customers
    # customers are formed as cust[[booth location, times to spend], etc]
    for x in range(1000):
        cust.append(customer(x,spending,chance,wait))

    for x in range(maxbooth):
        booths.append(booth(x,betarate))
        
    print("making",len(booths),len(cust))

    # no active customers right now
    active = []



# increment time -> move customers -> update booths


def trial():
    global timer, ct


    ci = 0
    while(len(cust)>0 or len(active)>0):



        for b in booths:
            b.update()

        if timer >= ci:
            if len(cust) > 0:
                # remove first cust object and put in active list
                active.append(cust.pop(0))

            if len(ct) > 0:
                ci = ct.pop(0)



        removals= []

        for idx,c in enumerate(active):
            if c.location >= 100:
                removals.append(idx)
                continue

            if c.inqueue == 0:

                booths[c.location].touch()

                if c.move() == True:
                    i = c.location
                    # booth has shorter line 
                    if len(booths[i].queue) < c.wait:
                        booths[i].addcust(c)
                    # else cust moves on
                    else:
                        c.location += 1


        for x in sorted(removals,reverse=True):
            active.pop(x)


        timer +=1



total_sales = 0
trial_amt = 100

avg = [0] * 100

for brate in [.01,.05,.1,.5]:
    for x in range(trial_amt):


        # (# of times to spend, chance to spend, will pass if this many in queue, booth beta)
        inittrial(1,.1,1000,brate)
        trial()

        for b in booths:

            avg[b.location]+=b.obsalpha()
#            avg[b.location]+=b.sales


            total_sales+=b.sales


        
        #reset
        timer = 0
        maxbooth = 100
        ct = []
        cust = []
        active = []
        booths = []



    for i,x in enumerate(avg):
        avg[i] = x/trial_amt
        print(x, x/trial_amt)


    x = []
    for i in range(100):
        x.append(i)



    plt.plot(x,avg)


x = []
for i in range(100):
    x.append(i)


#makes times, this is same as # of customers
ct = []
t = 0
for d in range(1000):
    t+= random.expovariate(.5)
    ct.append(t)
    print t

for i in range(100):
    avg[i]=sum(ct)/len(ct)

plt.plot(x,avg)


plt.show()
