# Iteractive-Chart-Web-Scrapping

Python Script for scrapping iteractive web charts. I iteractively scrape data from cryptoquant charts.The scrapping is made by using selenium.py library. 

Run "main()" function to get the data. 

![image](https://user-images.githubusercontent.com/84282116/160249778-650f70b0-41fe-4c00-a0f4-0ee02663c9fa.png)


First stage of the script consists in removing the pop up add and login into Crypto Quant account 
![image](https://user-images.githubusercontent.com/84282116/160249925-db1a6fad-076a-4c74-8f71-9c111fdfac5c.png)

To iteractively scrape the data i use a for loop to move the cursor (caled by the function "move_by_offset") over the coordinates of the graph.
Because each mouse movement does not corresponde to each day movement, under the default structure of the webpage, I zoom in the graph in order to fully capture the daily  datapoints within the graph

Two separate iterations are made in the "main()" function to capture the zoom from the left, and the zoom  for the right, appending the data into a final dataframe.
![image](https://user-images.githubusercontent.com/84282116/160252022-358d7b0c-4a0b-45f5-a70d-11af753aacd8.png)

