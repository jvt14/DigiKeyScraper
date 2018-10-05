import requests
from bs4 import BeautifulSoup

print("DigiKey Web Scraping")

# Base URL that will be used to get item data
baseURL = "https://www.digikey.com/product-detail/en/"

#partList = [("silicon-labs","C8051F320-GQ","336-1259-ND"), ("silicon-labs","C8051F380-GQ","336-2021-ND")]

# Open parts text file to get part numbers for lookup
readFile = open("parts.txt", "r")

# Read the lines from the file
lines = readFile.readlines()

# Create an array of tuples from each line from the file
partFileList = [tuple(line.strip().split(',')) for line in lines] 
#print(partFileList)

# Open a new file to write results into
writeFile = open("quantities.txt","w")

writeFile.write("\t\t%16s \t %20s \t %20s\n" % ("Mfg Part #","DigiKey Part #","Quantity"))
writeFile.write("-------------------------")
writeFile.write("-------------------------")
writeFile.write("-------------------------\n")

print("\t%16s \t %20s \t %20s" % ("Mfg Part #","DigiKey Part #","Quantity"))

count = 0

for part in partFileList:
    count += 1
    #print(part)
    # Parse the fields for each array entry
    manufacturer = part[0] #"silicon-labs"
    partNumber = part[1] #"C8051F380-GQ" #"C8051F320-GQ"
    dkNumber = part[2] #"336-2021-ND" #336-1259-ND"
    #print(manufacturer)

    # Create the specific URL for this part
    combinedURL = baseURL+manufacturer+"/"+partNumber+"/"+dkNumber
    #print(combinedURL)

    data = requests.get(combinedURL)
    soup = BeautifulSoup(data.text, 'html.parser')

    # Look for the 'Product Overview' table
    productOverview = soup.find('table', { 'id' : 'product-overview'})
    #print(productOverview)

    # Find the quantity field in the table
    qty = productOverview.find_all('td')[2].find('span', {'id' : 'dkQty'}).text

    # Print out the data to the screen
    #print(partNumber+" "+dkNumber+" "+qty)
    print("%d | %20s \t %20s \t %20s" % (count,partNumber,dkNumber,qty))

    # Print out the data to the file
    writeFile.write("%d | %20s \t %20s \t %20s\n" % (count,partNumber,dkNumber,qty))

# Cleanup files at the end of the program
readFile.close()
writeFile.close()