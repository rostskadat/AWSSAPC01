-- as per https://docs.aws.amazon.com/redshift/latest/gsg/rs-gsg-try-query.html
-- Get definition for the sales table.
SET query_group TO 'AccountingQueryGroup';
SELECT *    
FROM pg_table_def    
WHERE tablename = 'sales';
RESET query_group;

-- Find total sales on a given calendar date.
SET query_group TO 'EngineeringQueryGroup';
SELECT sum(qtysold) 
FROM   sales, date 
WHERE  sales.dateid = date.dateid 
AND    caldate = '2008-01-05';
RESET query_group;

-- Find top 10 buyers by quantity.
SET query_group TO 'AccountingQueryGroup';
SELECT firstname, lastname, total_quantity 
FROM   (SELECT buyerid, sum(qtysold) total_quantity
        FROM  sales
        GROUP BY buyerid
        ORDER BY total_quantity desc limit 10) Q, users
WHERE Q.buyerid = userid
ORDER BY Q.total_quantity desc;
RESET query_group;


-- Find events in the 99.9 percentile in terms of all time gross sales.
SET query_group TO 'EngineeringQueryGroup';
SELECT eventname, total_price 
FROM  (SELECT eventid, total_price, ntile(1000) over(order by total_price desc) as percentile 
       FROM (SELECT eventid, sum(pricepaid) total_price
             FROM   sales
             GROUP BY eventid)) Q, event E
       WHERE Q.eventid = E.eventid
       AND percentile = 1
ORDER BY total_price desc;
RESET query_group;
