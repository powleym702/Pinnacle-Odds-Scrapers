from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import re

driver_path = r'C:\Users\matth\OneDrive\Documents\chromedriver-win32\chromedriver.exe'
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

urls = []

try:
    # Base URL for the page
    url = "https://www.pinnacle.com/en/hockey/nhl/matchups/#period:1"
    driver.get(url)

    # Table XPath
    table_xpath = '//*[@id="root"]/div[1]/div[2]/main'
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, table_xpath)))

    print("Page loaded successfully, starting to retrieve links.")

    g = 3  # Start row index
    consecutive_failures = 0  # Track failed row attempts

    while True:
        row_found = False  # Flag to track if a valid row was found in this iteration

        for i in range(0, 4):  # Check up to the next 3 rows (g, g+1, g+2, g+3)
            current_row = g + i
            try:
                # Dynamic XPath for the link in the current row
                link_xpath = f'//*[@id="root"]/div[1]/div[2]/main/div/div[4]/div[2]/div/div[{current_row}]/div[3]/a'

                # Wait for the element and extract the link
                WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, link_xpath)))
                game_link = driver.find_element(By.XPATH, link_xpath)
                game_url = game_link.get_attribute("href")
                urls.append(game_url)

                print(f"Link found at row {current_row}: {game_url}")

                # Update `g` to the next row and reset failure count
                g = current_row + 1
                consecutive_failures = 0
                row_found = True
                break  # Break out of the inner loop to continue from the new row

            except (NoSuchElementException, TimeoutException):
                continue  # Move to the next index (g+1, g+2, etc.)

        if not row_found:
            consecutive_failures += 1
            g += 4  # Skip forward to avoid infinite loops

        if consecutive_failures >= 1:  # Stop after 2 consecutive failure checks
            break

finally:
    print("Retrieved URLs")

lines = []
oddss = []
names = []
stats = []


try:
    for url in urls:
        prop_url = f"{url}#player-props"
        driver.get(prop_url)
        
        # Ensure the page/table is loaded
        table_xpath = '//*[@id="root"]/div[1]/div[2]/main/div[3]/div'
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, table_xpath)))
        
        print(f"Processing URL: {prop_url}")  # Debugging output

        g = 1  # Start with the first row
        while True:
            try:
                # Build dynamic XPath for the current row's elements
                over_line_xpath = f'//*[@id="root"]/div[1]/div[2]/main/div[3]/div/div[{g}]/div[2]/div/div/div[1]/button/span[1]'
                odds1_xpath = f'//*[@id="root"]/div[1]/div[2]/main/div[3]/div/div[{g}]/div[2]/div/div/div[1]/button/span[2]'
                odds2_xpath = f'//*[@id="root"]/div[1]/div[2]/main/div[3]/div/div[{g}]/div[2]/div/div/div[2]/button/span[2]'
                player_xpath = f'//*[@id="root"]/div[1]/div[2]/main/div[3]/div/div[{g}]/div[1]/span[1]'
                under_line_xpath = f'//*[@id="root"]/div[1]/div[2]/main/div[3]/div/div[{g}]/div[2]/div/div/div[2]/button/span[1]'

                # Wait for the line element to appear
                WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, over_line_xpath)))
                
                player_name = driver.find_element(By.XPATH, player_xpath).text
                name = player_name.split(" (")[0]
                stat = player_name[player_name.find("(") + 1 : player_name.find(")")]
                # Extract the line string
                over_line_string = driver.find_element(By.XPATH, over_line_xpath).text
                # Only proceed if the line contains a dot
                if "." in over_line_string:
#                    print(f"Row {g} - Line string: {line_string} for {name}")  # Debugging output
                    # Extract and compare odds
                    odds1 = float(driver.find_element(By.XPATH, odds1_xpath).text)
                    odds2 = float(driver.find_element(By.XPATH, odds2_xpath).text)
                    decimal_odds = min(odds1, odds2)

                    # Convert to American odds
                    if decimal_odds >= 2:
                        odds = round((decimal_odds - 1) * 100, 0)
                    else:
                        odds = round(-100 / (decimal_odds - 1), 0)

                    # Extract the line number
                    if odds1 > odds2:
                        under_line_string = driver.find_element(By.XPATH, under_line_xpath).text
                        line = re.search(r'.*?\d+(\.\d+)?', under_line_string).group()
                    else:
                        line = re.search(r'.*?\d+(\.\d+)?', over_line_string).group()
                    if odds >= -150 and odds <= -134:
                        stats.append(stat)
                        names.append(name)
                        oddss.append(odds)
                        lines.append(line)
#                    print(f"Appended: Line {line}, Odds {odds}")  # Debugging output
 #               else:
 #                   print(f"Row {g} - Line string does not contain valid data.")  # Debugging output

            except (NoSuchElementException, TimeoutException):
                print(f"Row {g} - Missing element(s), skipping to the next row.")
            
            # Increment row index `g` to move to the next row
            g += 1

            # Break condition: Exit if we exceed the rows in the table
            try:
                next_row_xpath = f'//*[@id="root"]/div[1]/div[2]/main/div[3]/div/div[{g}]'
                driver.find_element(By.XPATH, next_row_xpath)  # Check if the row exists
            except NoSuchElementException:
                print(f"No more rows found at index {g}. Moving to the next URL.")
                break

finally:
    driver.quit()
'''
print("Shots On Goal:")

for name in names:
    print(name)
for line in lines:
    print(line)
for odds in oddss:
    print(odds)

print("Shots On Goal")
for name, line, odds in zip(sog_names, sog_lines, sog_oddss):
    print(f"{name}  {line}  {odds}")
print("Points")
for name, line, odds in zip(points_names, points_lines, points_oddss):
    print(f"{name}  {line}  {odds}")
print("Assists")
for name, line, odds in zip(assists_names, assists_lines, assists_oddss):
    print(f"{name}  {line}  {odds}")
print("Saves")
for name, line, odds in zip(saves_names, saves_lines, saves_oddss):
    print(f"{name}  {line}  {odds}")
    '''
# Combine the lists into a single list of tuples
data = list(zip(names, lines, stats, oddss))

# Sort by stat first (index 2) and then by name (index 0)
sorted_data = sorted(data, key=lambda x: (x[2], x[0]))

# Print the sorted data
for name, line, stat, odds in sorted_data:
    print(f"{name},{line},{stat},{odds}")