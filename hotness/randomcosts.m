% rng shuffle;
booth_row = 10;
booth_column = 1;
ppl = 10;
queue = 0; % assuming no queue.
booth_value = rand(booth_row, booth_column) % booths assigned a random value between 0 and 1.
a = input('Enter distribution (normal, binomial, geometric) for starting money: ', 's');

if strcmp(a,'normal') % checks if normal distrubtion desired
    
    amean = input('Enter mean '); astdev = input('Enter standard deviation ');
    cust_wallet = floor(normrnd(amean,astdev, ppl,1)) % amount of money each customer starts off with
    booth_cost = floor(normrnd(amean,astdev,booth_row, booth_column)) % Integer value; booths' selling price
    value_of_buy = (amean+2*astdev)*booth_value % some parameter to determine whether user spends or not ((mean + 2*stdev)*booth value) 
    for ii = 1:booth_row
        for jj = 1:ppl
            if cust_wallet(jj,ii) >= booth_cost(ii)
                cust_wallet(jj,ii+1) = cust_wallet(jj,ii)-booth_cost(ii);
                booth_cost(ii, jj+1) = booth_cost(ii,jj) + booth_cost(ii,1);
            else
                cust_wallet(jj,ii+1) = cust_wallet(jj,ii);
                booth_cost(ii, jj+1) = booth_cost(ii,jj);
            end
        end
    end
    
    titlestr = strcat('N(',num2str(amean),',',num2str(astdev),'^2)');
            
elseif strcmp(a, 'binomial') % checks if binomial distribution desired
    
    n = input('Enter number of trials '); p = input('Enter probability of success of each trial ');
    cust_wallet = floor(binornd(n,p,ppl,1)) % Integer value
    booth_cost = floor(binornd(n,p,booth_row, booth_column)) % Integer value; booths' selling price
    for ii = 1:ppl
        for jj = 1:ppl
            if cust_wallet(jj,ii) >= booth_cost(ii)
                cust_wallet(jj,ii+1) = cust_wallet(jj,ii)-booth_cost(ii);
                booth_cost(ii, jj+1) = booth_cost(ii,jj) + booth_cost(ii,1);
            else
                cust_wallet(jj,ii+1) = cust_wallet(jj,ii);
                booth_cost(ii, jj+1) = booth_cost(ii,jj);
            end
        end
    end    
    
    titlestr = strcat('Bin(',num2str(n),',',num2str(p),')');
    
elseif strcmp(a, 'geometric') % checks if geometric distribution desired 
    
    p = input('Enter probability of success of each trial ');
    cust_wallet = floor(geornd(p, ppl,1)) % Integer value
    booth_cost = floor(geornd(p,booth_row, booth_column)) % Integer value; assigns to booths
    for ii = 1:ppl
        for jj = 1:ppl
            if cust_wallet(jj,ii) >= booth_cost(ii)
                cust_wallet(jj,ii+1) = cust_wallet(jj,ii)-booth_cost(ii);
                booth_cost(ii, jj+1) = booth_cost(ii,jj) + booth_cost(ii,1);
            else
                cust_wallet(jj,ii+1) = cust_wallet(jj,ii);
                booth_cost(ii, jj+1) = booth_cost(ii,jj);
            end
        end
    end
    
    titlestr = strcat('Geom(',num2str(p),')');
end

[x, line1, line2] = plotyy(0:booth_row,cust_wallet, 0:booth_row, booth_cost);
set(line1,'LineStyle','-.'); set(line2,'LineStyle', '-');
xlabel('Booth')
ylabel(x(1), 'Money after booth interaction'); ylabel(x(2), 'Booth revenue');
for jj = 1:ppl
    legend_string{jj} = strcat('C',num2str(jj));
end
for kk = (jj+1):(jj+booth_row)
    legend_string{kk} = strcat('B',num2str(kk));
end
legend(legend_string)
title(strcat(titlestr, ' distribution of  ', num2str(ppl), ' booth prices and customer wallets'))
