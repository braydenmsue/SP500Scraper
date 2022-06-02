import csv
file = open("stock_data.csv")
csvreader = csv.reader(file)
header = next(csvreader)

# Initiate value-holding variables
highValue = 0
highIndex = 0
lowValue = 99.9
lowIndex = 0
currentIndex = 0

companyName = []
percentChanges = []

for row in csvreader:
    companyName.append(row[1])
    # Add percent change to list without the percent sign, so it can be converted to float and compared
    percentChanges.append(float(row[2].strip("%")))

    # Compare current percent change value to highest so far, replace if current is higher
    if percentChanges[currentIndex] > highValue:
        highValue = percentChanges[currentIndex]
        highIndex = currentIndex

    # Compare current percent change value to lowest so far
    if percentChanges[currentIndex] < lowValue:
        lowValue = percentChanges[currentIndex]
        lowIndex = currentIndex

    currentIndex += 1


print("Strongest performer of the day is " + companyName[highIndex] + " with a stock value increase of " + str(highValue) + "%.")
print("Weakest performer of the day is " + companyName[lowIndex] + " with a stock value decrease of " + str(lowValue) + "%.")

file.close()