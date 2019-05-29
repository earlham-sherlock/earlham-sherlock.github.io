
### Enrich protein list with internal interactions

Starting from a set of nodes, we can get an initial network by selecting all the interactions between 
these nodes. In the following example we will create this network by selecting links from the IntAct 
database. We will save the results to a new table.

Please note, by the nature of this query, the resulting network can contain multiple connected 
components. Also if there was an initial node fits to no links in the IntAct database, we will
loose the node from the resulting network (as we represent the network with a link list).


```$sql
CREATE TABLE project.mate_my_new_ppi_table WITH (
   format = 'ORC',
) AS

SELECT intact.interactor_a_id, 
       intact.interactor_b_id, 
FROM master.intact_2018_10_04 intact
WHERE intact.interactor_a_id IN ('ensg11867234247', 'ensg11867234247', 'ensg23829324243') 
  AND intact.interactor_b_id IN ('ensg11867234247', 'ensg11867234247', 'ensg23829324243');
```

### Enrich protein list with internal interactions AND first neighbours

If you simply change the `AND` to and `OR` in the query of the previous example, you will get 
not only the interconnections, but also the first neighbours. 


```$sql
CREATE TABLE project.mate_my_new_ppi_table WITH (
   format = 'ORC',
) AS

SELECT intact.interactor_a_id, 
       intact.interactor_b_id, 
FROM master.intact_2018_10_04 intact
WHERE intact.interactor_a_id IN ('ensg11867234247', 'ensg11867234247', 'ensg23829324243') 
   OR intact.interactor_b_id IN ('ensg11867234247', 'ensg11867234247', 'ensg23829324243');
```


---
© 2018, 2019 Earlham Institute ([License](../license.md))
