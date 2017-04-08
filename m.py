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
    global timer

    def __init__(self, ident, spending,chance,wait):
        self.ident = ident
        self.spending = spending
        self.inqueue = 0
        self.chance = chance
        self.location = 0
        self.wait = wait
        self.alpha = random.expovariate(.5)



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
            if self.alpha <= timer:
                self.alpha = timer + random.expovariate(.5)

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


    def __init__(self,location,br):
        self.location = location
        self.queue = []
        self.sales = 0
        self.rate = br
        self.oalpha = []

        # time till next serve
        self.beta = random.expovariate(self.rate)




    # adds customer object to queue
    def addcust(self,cst):
        self.queue.append(cst)
        cst.inqueue = 1

    # checks to see if served customer
    def update(self):
        if len(self.queue) > 0:
            # sale occurs
            if self.beta <= timer:
                self.sales += 1
                self.queue[0].sale()
                self.queue.pop(0)


                # set next service time
                self.beta = timer + random.expovariate(self.rate)

    # had a customer 'visit' so add time to oalpha
    def touch(self):
        self.oalpha.append(float(timer))


    # returns avg of times
    def obsalpha(self):
        if len(self.oalpha) == 0:
            return 0.0
        else:
            #return len(self.oalpha)
            s = [self.oalpha[i+1] - self.oalpha[i] for i in range(len(self.oalpha) -1)]
            if len(s) == 0:
                return 0.0
            else:
                si = sum(s)/len(s)
                if si == 0:
                    return 0.0
                else:
                    return 1/float(si)
                #return sum(self.oalpha)/len(self.oalpha)






def inittrial(spending, chance, wait, betarate):
    global ct, timer
    global cust, active, booths



    timer = 0
    cust = []
    active = []
    booths = []

    # rate at customers appear to booth 0
    # beta alpha rates would be say 1/rate so 
    # for .5 = 2 = lambda or .1 = 10
    # this means avg is 10 'time units' till next event
    alpha = .5




    #makes times, this is same as # of customers
    ct = []
    t = 0
    for x in range(100000):
        t+= random.expovariate(alpha)
        ct.append(t)



    #make customers
    # customers are formed as cust[[booth location, times to spend], etc]
    for x in range(1000):
        cust.append(customer(x,spending,chance,wait))

    for x in range(100):
        booths.append(booth(x,betarate))



# increment time -> move customers -> update booths


def trial():
    global timer, ct, booths, cust, active
    timer = 0    


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

            elif c.inqueue == 0:

                booths[c.location].touch()

                if c.move() == True:
                    i = c.location
                    # booth has shorter line 
                    if len(booths[i].queue) < c.wait:
                        booths[i].addcust(c)
                        removals.append(idx)
                    # else cust moves on
                    else:
                        c.location += 1

            else:
                pass

        for x in sorted(removals,reverse=True):
            active.pop(x)


        timer +=1



total_sales = 0
trial_amt = 5

avg = [0] * 100
bavg = [0] * 100

fig1 = plt.figure()
ax1 = plt.subplot(111)
fig2 = plt.figure()
ax2 = plt.subplot(111)

tim = 0
for brate in [.01,.02,.03,.04,.05]:


    for tamt in range(trial_amt):


        # (# of times to spend, chance to spend, will pass if this many in queue, booth beta)
        inittrial(1,.1,1,brate)


        s = [ct[i+1] - ct[i] for i in range(len(ct) -1)]
        s = sum(s) / len(s)

        tim = 1/s

        trial()

        for b in booths:

            bavg[b.location]+= float(b.obsalpha())
            print b.location, b.obsalpha()
            avg[b.location]+=b.sales




        
        #reset
        timer = 0
        maxbooth = 100
        ct = []
        cust = []
        active = []
        booths = []



    for a,b in enumerate(avg):
        avg[a] = b/trial_amt

    for c,d in enumerate(bavg):
        bavg[c] = d/trial_amt
        

    x = []
    for i in range(100):
        x.append(i)

    ax1.plot(x,avg,label=brate)

    ax2.plot(x,bavg,label=brate)

    avg = [0] * 100
    bavg = [0] * 100

t = [0]* 100
for i in range(100):
    t[i] = tim
x = []
for i in range(100):
    x.append(i)


tim = 0
ax2.plot(x,t,label='base alpha')


plt.figure(fig1.number)
plt.legend(loc='upper right')
fig1.savefig('avg-wait1000.png')


plt.figure(fig2.number)
plt.legend(loc='upper right')
fig2.savefig('bavg-wait123.png')




