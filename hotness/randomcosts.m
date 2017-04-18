% rng shuffle;
booth_row = 10000;
booth_column = 1;
ppl = 10000;
queue = 0; % assuming no queue.
booth_value = rand(booth_row, booth_column) % booths assigned a random value between 0 and 1.
a = input('Enter distribution (normal, binomial, geometric, uniform) for starting money: ', 's');

if strcmp(a,'normal') % checks if normal distrubtion desired
    
    amean = input('Enter mean '); astdev = input('Enter standard deviation ');
    cust_wallet = abs(floor(normrnd(amean,astdev, ppl,1))); % amount of money each customer starts off with
    booth_cost = abs(floor(normrnd(amean,astdev,booth_row, booth_column))); % Integer value; booths' selling price
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
    cust_wallet = floor(binornd(n,p,ppl,1)); % Integer value
    booth_cost = floor(binornd(n,p,booth_row, booth_column)); % Integer value; booths' selling price
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
    cust_wallet = floor(geornd(p, ppl,1)); % Integer value
    booth_cost = floor(geornd(p,booth_row, booth_column)); % Integer value; assigns to booths
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
    
elseif strcmp(a, 'uniform') % checks if geometric distribution desired 
    
    cust_wallet = floor(100*rand(ppl,1)) % Integer value
    booth_cost = floor(100*rand(booth_row, booth_column)) % Integer value; assigns to booths
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
    
    titlestr = strcat('Uniform');
end

figure(1);
x = plot(0:booth_row,cust_wallet);
set(x,'LineStyle','-.'); 
xlabel('Booth')
ylabel('Money after booth interaction'); 
% for jj = 1:ppl
%     legend_string{jj} = strcat('C',num2str(jj));
% end
% for kk = (jj+1):(jj+booth_row)
%     legend_string{kk} = strcat('B',num2str(kk));
% end
% legend(legend_string)
title(strcat(titlestr, ' distribution of  ', num2str(ppl), 'Customer wallets'))

figure(2);
y = plot(0:booth_row, booth_cost);
set(y,'LineStyle', '-');
xlabel('Booth')
ylabel( 'Booth revenue');
title(strcat(titlestr, ' distribution of  ', num2str(ppl), 'Booth prices'))
