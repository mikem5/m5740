import math
import random
import time
import matplotlib.pyplot as plt
import numpy as np



# global timer
timer = 0
maxbooth = 100

# = a / .1
alpha = 2


cust = []
active = []
booths = []


def comloc(loc):
    return loc[0]*10 + loc[1]



class customer(object):
    global timer,alpha

    def __init__(self, ident, spending,chance,wait):
        self.ident = ident
        self.spending = spending
        self.inqueue = 0
        self.chance = chance

        start_row = np.random.randint(9)
        self.location = [start_row,0]
        self.wait = wait
        self.alpha = np.random.poisson(alpha)


        self.used_rows = [start_row]

    def check(self):
        return self.location, self.spending, self.inqueue

    def sale(self):
        self.spending -= 1
        self.inqueue = 0
        if self.spending > 0:
            self.location_move()
        # left
        else:
            self.location = [100,100]



    def location_move(self):
        if self.location[1] == 9:
            if len(self.used_rows) >= 10 :
                self.location = [10,10]
            else:

                a = [i for i in range(10) if i not in self.used_rows]
                row = np.random.choice(a)
                self.used_rows.append(row)
                self.location[0] = row
                self.location[1] = 0

        #if self.location[1] == 9:
        #    self.location[0] += 1
        #    self.location[1] = 0
        else:
            self.location[1]+=1
 

    def move(self):
        if self.inqueue == 0:
            #if timer >= self.alpha and self.location > [0,0]:
            #    self.alpha = timer + np.random.poisson(alpha)
                #chance to enter current line
            #    if random.random() <= self.chance * booths[self.location[0] + self.location[1]].hotness:
            #       return True
            #    else:
            #        self.location_move() 
            #        return False
            #else: #self.location == [0,0]:
                #chance to enter current line
            if np.random.rand() <= self.chance * booths[comloc(self.location)].hotness:
#                print comloc(self.location)
                return True
            else:
                self.location_move() 
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
        self.oalpha = [0]
        self.lostcust = 0

        # probability mixing with customer probability,
        # base chance of attracting a customer
        #
        # can change distribution for testing?
#        self.hotness = 1
        #self.hotness  = np.random.uniform()
        self.hotness = abs(np.random.normal(0,.1))
        #self.hotness = np.random.exponential(scale=.1)


        # time till next serve
#        self.beta = np.random.poisson(self.rate)
        self.beta = 0



    # adds customer object to queue
    def addcust(self,cst):
        self.queue.append(cst)
        cst.inqueue = 1

    # checks to see if served customer
    def update(self):
        if len(self.queue) > 0:
            # sale occurs
            if timer >= 0: #self.beta:
                self.sales += 1
                self.queue[0].sale()
                self.queue.pop(0)


                # set next service time
                self.beta = timer + np.random.poisson(self.rate)



    # had a customer 'visit' so add time to oalpha
    def touch(self):
        self.oalpha.append(float(timer))


    # returns avg of times
    def obsalpha(self):
        if len(self.oalpha) == 0:
            return 0.0
        else:
            s = [self.oalpha[i+1] - self.oalpha[i] for i in range(len(self.oalpha) -1)]
            if len(s) == 0:
                return float(0.0)
            else:
                si = sum(s)/len(s)
                if si == 0:
                    return float(0.0)
                else:
                    #return si
                    return 1/float(si)






def inittrial(spending, chance, wait, betarate):
    global timer
    global cust, active, booths



    timer = 0.0
    cust = []
    active = []
    booths = []


    #make customers
    # customers are formed as cust[[booth location, times to spend], etc]
    for x in range(1000):
        cust.append(customer(x,spending,chance,wait))

    for x in range(10):
        for y in range(10):
            booths.append(booth([x,y],betarate))



# increment time -> move customers -> update booths


def trial():
    global timer, booths, cust, active
    timer = 0


    current_alpha = np.random.poisson(alpha)

    ci = 0
    while(len(cust)>0 or len(active)>0):



        if timer >= current_alpha:
            if len(cust) > 0:
                # remove first cust object and put in active list
                active.append(cust.pop(0))


            current_alpha = timer + np.random.poisson(alpha)


        for b in booths:
            b.update()


        removals= []

        for idx,c in enumerate(active):
            if comloc(c.location) >= 100:
                removals.append(idx)

            elif c.inqueue == 0:


                if c.move() == True:

                    i = comloc(c.location)
                    # booth has shorter line 
                    # just ignore queue for now
                    #if len(booths[i].queue) >= 0:
                    if True:
                        booths[i].addcust(c)
                        removals.append(idx)
                        booths[i].touch()
                  
                    # else cust moves on

                    else:
                        c.location_move()
                        booths[i].lostcust +=1
            else:
                pass

        if len(removals) > 0:
#            print removals, len(active)
            for x in sorted(removals,reverse=True):
#                print x, active[x].location, active[x].inqueue
                active.pop(x)




        timer +=1





    for i in range(10):
        for b in booths:
            b.update()

        timer +=1



total_sales = 0



# total amount of trials we run
trial_amt = 1000

avg = [0] * 100
bavg = [0] * 100
lost = [0] * 100

fig1 = plt.figure()
ax1 = plt.subplot(111)
fig2 = plt.figure()
ax2 = plt.subplot(111)
fig3 = plt.figure()
ax3 = plt.subplot(111)


tim = 0

b1 = []


for var in [.1,.2,.3,.4,.5]:

    for tamt in range(trial_amt):


        # (# of times to spend, chance to spend, will pass if this many in queue, booth beta)
        inittrial(1,var,1,1)


#        s = [ct[i+1] - ct[i] for i in range(len(ct) -1)]
#        s = sum(s) / len(s)

#        tim = 1/s

        trial()

        for b in booths:

            bavg[comloc(b.location)]+= b.obsalpha()
            avg[comloc(b.location)]+=b.sales
            lost[comloc(b.location)]+=b.lostcust



        
        #reset
        timer = 0
        maxbooth = 100
        cust = []
        active = []
        booths = []



    for a,b in enumerate(avg):
        avg[a] = b/trial_amt

    for c,d in enumerate(bavg):
        bavg[c] = d/trial_amt
        
    for c,d in enumerate(lost):
        lost[c] = d/trial_amt


    b1.append([var, avg[0], avg[1], avg[2],avg[3], avg[4], avg[5],sum(avg)])



    x = []
    for i in range(100):
        x.append(i)

    ax1.plot(x,avg,label=var)

    ax2.plot(x,bavg,label=var)
    ax3.plot(x,lost,label=var)


    avg = [0] * 100
    bavg = [0] * 100
    lost = [0]*100


x = []
for i in range(100):
    x.append(i)



plt.figure(fig1.number)
plt.legend(loc='upper right')
fig1.savefig('avg-wait1.png')


plt.figure(fig2.number)
plt.legend(loc='upper right')
fig2.savefig('bavg-wait1.png')

plt.figure(fig3.number)
plt.legend(loc='upper right')
fig3.savefig('lost-wait1.png')




