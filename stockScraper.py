from bs4 import BeautifulSoup
import requests

# Design path: We need a way to keep track of the urls of the stocks we wish to track. Either we can keep atext file of urls or just hard code them in.
# them the algorithm can be as follows: 1). read in the urls, 2). scrape, format, and create a new object with the stock data. 3). formst the ints more 
# 4). print the data for each stock to a text file.

# also might need to check into data base stuff so we can keep track of past data. or we can store data in a textfile and append to it.

# One big problem here is the probelm of storing data. since the stock data is changing everyday we need to be able to update the information. the only way I can think of doing that now, is to keep this program running for ever.
# maybe talk to a professor about it.

#TO DO:
    # 1). Implement error handling for url access.
    # 2) Set up a database :)))))))))))))))) (sql and linux on old laptop as a sever)
    # 4) start making the algorithm to access stock technically (500 long day avergae or whatever.)
    # 5) Mayve we should make the 500 average thing a sepreate method its going to take a lot of calculating I think.
    # 6) database shit.



#-----Classes-----#

class Stock:

    # We are going to need a method that formats the values further. The M and T identifiers are not removed. need to somehow conver to a int so 
    # we can use it in calculations. Or maybe just do this in the format method we already made.... might be hard to distiguish which value has m or t.

    # Stock constructor. 
    def __init__(self, ticker, url, openVal=None, dayRange=None, weekRange=None, marketCap=None, sharesOutstanding=None, publicFloat=None, beta=None, 
    revPerEmployee=None, peRatio=None, eps=None, yieldPercent=None, dividend=None, divDate=None, shortInt=None, shortFloat=None, avgVol=None, closePrice=None):
        self.url = url
        self.ticker = ticker
        self.openVal = openVal
        self.dayRange = dayRange
        self.weekRange = weekRange
        self.marketCap = marketCap
        self.sharesOutstanding = sharesOutstanding
        self.publicFloat = publicFloat
        self.beta = beta
        self.revPerEmployee = revPerEmployee
        self.peRatio = peRatio
        self.eps = eps
        self.yieldPercent = yieldPercent
        self.dividend = dividend
        self.divDate = divDate
        self.shortInt = shortInt
        self.shortFloat = shortFloat
        self.avgVol = avgVol
        self.closePrice = closePrice
    
    # This is the objects tostring method. Prints basic information. Might need to augment later for more information.
    def __str__(self):
        return f"-------------------------\nTicker: {self.ticker}\nPrevious Close: {self.closePrice}\nOpen Price: {self.openVal}\n-------------------------"


#-----Functions-----#
 
#-----Debug-----#
def printStockInfo(releventHtml):

    for code in releventHtml:
        print(code.text.replace(' ', ''))

def printStockDict(stockDict):

    for stock in stockDict:
        print(stockDict[stock])




# This method reads all the urls in the urls.txt file and creates stock objects based on their related html page. Returns a dictionary of stock objects whos keys are their ticker.
def initDict():

    # Create the dictionary for all the stocks.
    stockDict = {}

    try:

        # Open the url file for reading.
        with open("urls.txt", "r") as urlFile:
        
            for line in urlFile: 

                # Get the url address.
                urlAddr = line.strip()

                # Create the stock object for the current url.
                newStock = createStockObject(urlAddr)

                # Add the new stock object to the dictionary using its ticker as the key.
                stockDict[newStock.ticker] = newStock

                print("done")

    except FileNotFoundError:
        print("File not found :(")
    except IOError:
        print("I/O error :(")

    return stockDict

# This method gets passed a url and returns a stock object. NEED TO ADD ERROR HANDLING HERE INCASE SOMETHING GOES WRONG!!! (if: error condition, then: return none)
def createStockObject(stockUrl): 

    print(stockUrl)

    # Gain access to the market watch page for apple. 
    stockPage = requests.get(stockUrl).text

    # Assign the beautiful soup variable.
    soup = BeautifulSoup(stockPage, 'lxml')

    # Get the ticker of the stock.
    stockTicker = soup.find("span", class_ = "company__ticker").text

    # Get the price information from the page.
    htmlData = soup.find('ul', class_ = "list list--kv list--col50")
    stockPrices = htmlData.find_all("span", class_ = "primary")

    # Get the closing price of the stock.
    closingPrice = soup.find("td", class_ = "table__cell u-semi").text

    # Format the data so that we can create the object.
    values = formatHtmlData(stockTicker, stockUrl, stockPrices, closingPrice)

    # Create the new stock object.
    newStock = Stock(*values)

    # Return the new object.
    return newStock

# Formats the html data values of a stock. Removes extra symbols. Returns a list.
def formatHtmlData(stockTicker, stockUrl, baseValues, baseClose):

    # List of formatted values to return.
    values = []

    # Append the ticker for the stock to the list.
    values.append(stockTicker)

    # Append the url for the stock.
    values.append(stockUrl)

    # Format the values and append them to the list.
    for value in baseValues:
        values.append(value.text.replace("$", "").replace("%", ""))

    # Add the formatted closing price.
    values.append(baseClose.replace("$", ""))

    # Return the list.
    return values


#-----Main-----#

#Initialize all the stocks from the urls text document.
stockDict = initDict()

printStockDict(stockDict)

#-------------------------------------------#

















