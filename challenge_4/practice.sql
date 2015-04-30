-- What customers are from the UK?
select * from Customers where Country='UK'

-- What is the name of the customer who has the most orders?
select ContactName, count(*) as count
  from Customers join Orders
  on Customers.CustomerID = Orders.CustomerID
  group by ContactName
  order by count desc;

  -- What supplier has the highest average product price?
