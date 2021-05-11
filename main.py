debugMode = False
debugAdmin = False

import csv
import os
import time
import sys
import json

#Load component list and other essentials
print("Loading...")
companies = {
  "I":"intel",
  "A":"amd",
  "I/A":"both"
}
components = {}
print("Unloading component list")
with open("components.csv") as file:
  csv_reader = csv.reader(file, delimiter=',')
  line = 0
  for row in csv_reader:
    if line != 0:
      try:
        if len(row) == 0: continue
        component = {
          "name":str(row[0]),
          "type":str(row[1]),
          "compatability":str(row[2]),
          "price":int(row[3])
        }
        try:
          components[row[1]].append(component)
        except KeyError:
          components[row[1]] = []
          components[row[1]].append(component)
      except:
        print("Error loading components")
        print(row)
        input("Press enter to continue ")
    line+=1
print("Loaded")
time.sleep(0.05)
os.system("clear")

#Collect & validate user data
adminUser = False
complete = False
if debugMode:
  complete = True
  if debugAdmin:
    name = "tommm"
    email = "w18ttidbury@tringschool.org"
  else:
    name = "David"
    email = "Davidpro@gmail.com"
while not complete:
  name = input("What is your username? ")
  email = input("What is your email? ")
  if name == "" or email == "":
    print("Please fill all fields.")
    continue
  try:
    domain = email.split('@')[1]
    primDomain = domain.split('.')[1]
    secDomain = domain.split('.')[0]
  except:
    print("Please enter a valid email and username.")
    continue
  if len(name) < 5 or len(email) < 5:
    print("Email and username must be longer than 5 characters")
    continue
  if len(domain) < 5 or len(primDomain) < 3 and len(secDomain) < 3:
    print("Please enter a valid email")
    continue
  complete = True
if name == "tommm" and email == "w18ttidbury@tringschool.org": adminUser = True #very secure
selectedComponents = {}
def getComponentbyName(name, type):
  search = components[type]
  for component in search:
    if component["name"] == name:
      return component

def getComponentbyPrice(price, type, maxRange, compatability):
  search = components[type]
  prices = {}
  for component in search:
    diff = price - component["price"]
    if diff < maxRange and diff > -100:
      if diff < 0: diff = diff*-1
      prices[component["name"]] = diff
  dict(sorted(prices.items(), key=lambda item: item[1]))
  for component in prices:
    component = getComponentbyName(component, type)
    if compatability in component["compatability"]:
      return component

def writeCurrent(clear):
  if clear: os.system("clear")
  print("Your currently selected components")
  totalPrice = 0
  for componentsS in selectedComponents:
    format = "None - We don't have any parts at this price point"
    try:
      format = "$" + str(selectedComponents[componentsS]["price"]) + " - " + selectedComponents[componentsS]["name"]
    except:
      format = "None - We don't have any parts at this price point"
    print(componentsS + ": " + format)
    try:
      totalPrice = totalPrice + selectedComponents[componentsS]["price"]
    except:
      totalPrice = totalPrice
  print("\nSubtotal: $" + str(totalPrice))
  return totalPrice

def printComponents(componentType, compatability):
  #os.system("clear")
  print(componentType + ":")
  if components[componentType]:
    componentsS = components[componentType]
    selection = []
    number = 1
    for componentS in componentsS:
      if compatability != None:
        if not compatability in componentS["compatability"]:
          continue
      print("  " + str(number) + ". $" + str(componentS["price"]) + " - " + str(componentS["name"]))
      selection.append(componentS)
      number+=1
    print("  " + str(number) + ". None")
    selection.append(None)
    number+=1
    return selection

def selectComponent(printComponentFunction):
  maxNumber = len(printComponentFunction)
  minNumber = 1
  
  complete = False
  num = 0
  while not complete:
    num = input("")
    try:
      num = int(num)
      if num >= minNumber and num <= maxNumber:
        complete = True
      else:
        print("Please enter a number between " + str(minNumber) + " and " + str(maxNumber))
    except:
      print("Please enter a number between " + str(minNumber) + " and " + str(maxNumber))
  num = num-1
  selectedComponent = printComponentFunction[num]
  return selectedComponent

def recommendedBuild(use, budget, compatability):
  #Work out good components based on budget and compatability
  if budget == 1:
    budget = 500
    budgetRange = 100
  if budget == 2:
    budget = 1000
    budgetRange = 150
  if budget == 3:
    budget = 2000
    budgetRange = 200
  if budget == 4:
    budget = 4000
    budgetRange = 250
  if budget == 5:
    budget = 8000
    budgetRange = 500
  if use == 1:
    keyboardMousePrice = 30
    cpuPrice = budget*0.30 #30%
    gpuPrice = budget*0.31 #31%
    motherboardPrice = budget*0.18 #18%
    ramPrice = budget*0.08 #8%
    storagePrice = budget*0.13 #13%
  elif use == 2:
    keyboardMousePrice = 30
    cpuPrice = budget*0.45 #45%
    gpuPrice = budget*0 #0%
    motherboardPrice = budget*0.20 #20%
    ramPrice = budget*0.10 #10%
    storagePrice = budget*0.25 #25%
  elif use == 3:
    keyboardMousePrice = 30
    cpuPrice = budget*0.25 #30%
    gpuPrice = budget*0.30 #31%
    motherboardPrice = budget*0.18 #18%
    ramPrice = budget*0.15 #8%
    storagePrice = budget*0.12 #13%
  
  storageType = "HDD"
  if storagePrice > 80: storageType = "SSD"

  print(f"Keyboard & Mouse: ${str(keyboardMousePrice)}")
  print(f"CPU Price: ${str(cpuPrice)}")
  print(f"GPU Price: ${str(gpuPrice)}")
  print(f"mb Price: ${str(motherboardPrice)}")
  print(f"ram Price: ${str(ramPrice)}")
  print(f"Storage Price: ${str(storagePrice)}")

  selectedCPU = getComponentbyPrice(cpuPrice, "CPU", budgetRange, compatability)
  selectedGPU = getComponentbyPrice(gpuPrice, "GPU", budgetRange, compatability)
  selectedMotherboard = getComponentbyPrice(motherboardPrice, "MB", budgetRange, compatability)
  selectedRAM = getComponentbyPrice(ramPrice, "RAM", budgetRange, compatability)
  selectedStorage = getComponentbyPrice(storagePrice, storageType, budgetRange, compatability)

  if selectedCPU == None:
    print("We were unable to select a computer with your budget. Automatically increasing budget")
    selectedCPU = getComponentbyPrice(cpuPrice, "CPU", 500, compatability)
  if selectedGPU == None:
    print("We were unable to select a computer with your budget. Automatically increasing budget")
    selectedGPU = getComponentbyPrice(gpuPrice, "GPU", 500, compatability)
  if selectedMotherboard == None:
    print("We were unable to select a computer with your budget. Automatically increasing budget")
    selectedMotherboard = getComponentbyPrice(motherboardPrice, "MB", 500, compatability)
  if selectedRAM == None:
    print("We were unable to select a computer with your budget. Automatically increasing budget")
    selectedRAM = getComponentbyPrice(ramPrice, "RAM", 500, compatability)
  if selectedStorage == None:
    print("We were unable to select a computer with your budget. Automatically increasing budget")
    selectedStorage = getComponentbyPrice(storagePrice, storageType, 500, compatability)

  selectedComponents["CPU"] = selectedCPU
  selectedComponents["GPU"] = selectedGPU
  selectedComponents["MB"] = selectedMotherboard
  selectedComponents["RAM"] = selectedRAM
  selectedComponents["STORAGE"] = selectedStorage

def purchase():
  os.system("clear")
  writeCurrent(False)
  purchase = input("Would you like to purchase this? ").lower()
  if purchase == "y" or purchase == "yes":
    purchase = True
  else:
    purchase = False
  prebuilt = input("Would you like Bits N' Bytes to build the PC for you ($65)? ").lower()
  if prebuilt == "y" or prebuilt == "yes":
    prebuilt = True
  else:
    prebuilt = False 
  if purchase:
    os.system("clear")
    print("Invoice: ")
    print("==============================")
    totalPrice = writeCurrent(False)
    if prebuilt:
      print("Prebuilt Fee: $65")
      totalPrice = totalPrice + 65
    vat = 0.2*totalPrice
    totalPrice = totalPrice + vat
    print("VAT Fee (20%): $" + str(vat))
    print("Total: $" + str(totalPrice))
    print("==============================")
    print("Totally Secure Payment System")
    print(f"Username: " + name)
    print(f"Email: " + email)
    card = input("Card: ")
    jsonData = None
    with open('orders.txt') as json_file:
      jsonData = json.load(json_file)
    jsonData["orderNumber"] = jsonData["orderNumber"] + 1
    orderNumber = jsonData["orderNumber"]
    print(f"Order Number: {orderNumber}")
    orderData = {
      "orderNumber": orderNumber,
      "cardNumber": card,
      "partsOrdered": selectedComponents,
      "prebuiltFee": 0,
      "VAT": vat
    }
    if prebuilt: orderData["prebuiltFee"] = 65
    orders = jsonData["orders"]
    orders[orderNumber] = orderData

    with open('orders.txt', 'w') as outfile:
      json.dump(jsonData, outfile)
    input("Success!")
  else:
    os.system("clear")
    print("Bye.")
    sys.exit()

while True:
  os.system("clear")
  print("Welcome,", name)

  print("-------------------------------------")
  print("1. Select your own components")
  print("2. Choose from our recommended builds")
  if adminUser:
    print("3. View orders")
    print("4. View order by ID")
  print("-------------------------------------")
  complete = False
  s = 0
  while not complete:
    s = input("")
    try:
      s = int(s)
      complete = True
    except:
      print("Please enter a number")
  
  if s == 1:
    print("AMD or Intel?")
    print("-------------------------------------")
    print("1. AMD (Good for gaming)")
    print("2. Intel")
    print("-------------------------------------")
    complete = False
    c = 0
    while not complete:
      c = input("")
      try:
        c = int(c)
        complete = True
      except:
        print("Please enter a number")

    if c == 1: c = "A"
    if c == 2: c = "I"
    if c == 3: c = "A"

    os.system("clear")
    writeCurrent(False)
    print("")
    selectedComponents["CPU"] = selectComponent(printComponents("CPU", c))
    os.system("clear")
    writeCurrent(False)
    print("")
    selectedComponents["GPU"] = selectComponent(printComponents("GPU", c))
    os.system("clear")
    writeCurrent(False)
    print("")
    selectedComponents["MB"] = selectComponent(printComponents("MB", c))
    os.system("clear")
    writeCurrent(False)
    print("")
    selectedComponents["RAM1"] = selectComponent(printComponents("RAM", c))
    os.system("clear")
    writeCurrent(False)
    print("")
    selectedComponents["RAM2"] = selectComponent(printComponents("RAM", c))

    purchase()
  elif s == 2:
    os.system("clear")
    print("What will you be using your computer for?")
    print("-------------------------------------")
    print("1. Gaming")
    print("2. Work (Editing documents, PDFs, etc)")
    print("3. Graphic design")
    print("-------------------------------------")
    complete = False
    s = 0
    while not complete:
      s = input("")
      try:
        s = int(s)
        complete = True
      except:
        print("Please enter a number")
    

    print("What is your computer budget?")
    print("-------------------------------------")
    print("1. $500")
    print("2. $1000")
    print("3. $2000")
    print("4. $4000")
    print("5. $8000")
    print("-------------------------------------")
    complete = False
    budget = 0
    while not complete:
      budget = input("")
      try:
        budget = int(budget)
        complete = True
      except:
        print("Please enter a number")

    print("AMD or Intel?")
    print("-------------------------------------")
    print("1. AMD (Good for gaming)")
    print("2. Intel")
    print("3. No preference - Let us choose!")
    print("-------------------------------------")
    complete = False
    c = 0
    while not complete:
      c = input("")
      try:
        c = int(c)
        complete = True
      except:
        print("Please enter a number")

    if c == 1: c = "A"
    if c == 2: c = "I"
    if c == 3: c = "A"

    os.system("clear")

    print("Compatability: " + companies[c])
    print("")

    recommendedBuild(s, budget, c)
    input("\nPress enter to continue")
    purchase()
  else:
    if adminUser:
      if s == 3:
        print("...")
        jsonData = None
        with open('orders.txt') as json_file:
          jsonData = json.load(json_file)
        currentOrder = 1
        totalOrders = jsonData["orderNumber"]
        while currentOrder <= totalOrders:
          order = jsonData["orders"][str(currentOrder)]
          print(f"Order number: " + str(order["orderNumber"]))
          print(f"Card number: " + str(order["cardNumber"]))
          print("Parts ordered:")
          parts = order["partsOrdered"]
          totalPrice = 0
          for part in parts:
            part = parts[part]
            print("$" + str(part["price"]) + " - " + part["name"])
            totalPrice = totalPrice + part["price"]
          print("\nSubtotal: $" + str(totalPrice))
          print("Prebuilt Fee: $" + str(order["prebuiltFee"]))
          totalPrice = totalPrice + order["prebuiltFee"]
          vat = 0.2*totalPrice
          totalPrice = totalPrice + vat
          print("VAT Fee (20%): $" + str(vat))
          print("Total: $" + str(totalPrice))
          print("\n\n")
          currentOrder = currentOrder + 1
          input("View next order? ")
      elif s == 4:
        jsonData = None
        with open('orders.txt') as json_file:
          jsonData = json.load(json_file)
        while True:
          print("There are " + str(jsonData["orderNumber"]) + " many orders currently")
          selectedOrderNumber = input("Which order do you want to look at? ")
          try:
            selectedOrderNumber = int(selectedOrderNumber)
          except:
            print("Error")
            continue
          order = jsonData["orders"][str(selectedOrderNumber)]
          print(f"Order number: " + str(order["orderNumber"]))
          print(f"Card number: " + str(order["cardNumber"]))
          print("Parts ordered:")
          parts = order["partsOrdered"]
          totalPrice = 0
          for part in parts:
            part = parts[part]
            print("$" + str(part["price"]) + " - " + part["name"])
            totalPrice = totalPrice + part["price"]
          print("\nSubtotal: $" + str(totalPrice))
          print("Prebuilt Fee: $" + str(order["prebuiltFee"]))
          totalPrice = totalPrice + order["prebuiltFee"]
          vat = 0.2*totalPrice
          totalPrice = totalPrice + vat
          print("VAT Fee (20%): $" + str(vat))
          print("Total: $" + str(totalPrice))
          print("\n\n")
      else:
        continue
    else:
      continue