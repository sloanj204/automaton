from selenium import webdriver
import time, csv, traceback
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

start_time = time.time()    # used for calculating runtime of program
d = webdriver.Chrome()      # driver for automation  
target_list = []            # array to store eeids
target_date = []            # array to store dates
new_list = []               # storage for errors
is_first = True             # to know which search bar to use
is_prod = False             # flag to identify instance

# URL AND UPLOAD FILE SETTINGS -----------------------------------------
t1_url = "https://hcm4preview.sapsf.com/sf/home?company=C0014376286T1#/login"               # URL of T1
p_url = "https://performancemanager4.successfactors.com/login?company=C0014376286P#/login"  # URL of Prod
target_file = "target.csv"    
error_file = "error_file.csv"     
# ----------------------------------------------------------------------


# loads input records ---------------------------------------------------------------------------------------------------
def load_file():
    with open(target_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            target_list.append(row[0])
            target_date.append(row[1])


# outputs error file ----------------------------------------------------------------------------------------------------
def save_error_file():
    with open(error_file, "w", newline="") as resultFile:
        wr = csv.writer(resultFile, delimiter=',')
        for row in new_list:
                wr.writerows([row])


# login for Production --------------------------------------------------------------------------------------------------
def login_wait(instance_url):
    d.get(instance_url)     # URL of Successfactors Instance
    input("Press any key to continue once you've logged in")


""" =============================================================================================================
    Processes T1 records
    (main function to process records. Pulls from target.csv)

    PARAMETERS:
    arg:    Employee ID
    date:   Date
    ================================================================================================================
"""
def process_me(arg, date):
    global is_first
    wait = WebDriverWait(d, 10)
    
    if is_first == True:
        time.sleep(5)
        is_first = False
        python_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div/div/section/div/div[2]/section/div[2]/div/div/div[1]/div/div/div/div[3]/div[1]/form/input")))  
    else:
        python_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div/div/div[1]/div[3]/div[1]/form/input")))

    python_button.send_keys(arg)
    time.sleep(3)
    python_button.send_keys(Keys.RETURN)
    python_button.send_keys(Keys.RETURN)
    time.sleep(7) # lets profile page load
    
    # job info section
    python_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div/div/div/div/div/div[2]/div/div[2]/div/section[2]/section[2]/div[2]/div[1]/div[2]/div/div/div/div/div/div[1]/div/span/div/button[2]/span[1]/span'))) # clock icon
    python_button.click()
    time.sleep(2) # otherwise clicks the "load more" button with an xpath of /html/body/div[3]/div[2]/section/div/div/div/div[1]/div/footer/div/button[2]/span
    
    python_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/section/div/div/div/div[1]/div/footer/div/button[1]/span'))) # insert record    
    python_button.click()
    # time.sleep(4)

    # pick date
    python_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/section/div/div/div/div/section/div[2]/div[2]/div/div/input')))
    python_button.send_keys(Keys.CONTROL, "a")
    python_button.send_keys(date)
    python_button.send_keys(Keys.ENTER)
    time.sleep(3)

    # event
    python_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/section/div/div/div/div/section/div[4]/div/div/div[2]/div/div/div/div[2]/div/div/input")))     # textbox
    python_button.send_keys("return")
    time.sleep(1)
    python_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[4]/div/div/div/ul/li[12]")))  # return to work event 
    python_button.click()
    time.sleep(3)

    # event reason
    python_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/section/div/div/div/div/section/div[4]/div/div/div[2]/div/div[2]/div/div[2]/div/div/input"))) # return to work event reason
    python_button.send_keys("return")
    time.sleep(1)
    python_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[6]/div/div/div/div/div/ul/li[3]")))    # select event reason
    python_button.click()
    time.sleep(1)

    # save and close
    python_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/section/div/div/div/div/footer/div/button[2]/span[1]/span")))  # save button
    python_button.click()
    time.sleep(4)
    python_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/section/div/div/div/div[2]/div/header/div/div[3]/button")))    # close job info box
    python_button.click()
    time.sleep(4)


""" ==========================================================================================================================
    Processes Production records
    (main function to process records. Pulls from target.csv)

    PARAMETERS:
    arg:    Employee ID
    date:   Date
    ===========================================================================================================================
"""
def process_me_prod(arg, date):
    global is_first # checks if it is the first record in proces. Reason is because there are 2 different search bars. 

    # Main page: go to persons profile
    if is_first == True:
        time.sleep(1)
        is_first = False
        python_button = d.find_elements_by_xpath("/html/body/div[3]/div/div/div/div/section/div/div[2]/section/div[2]/div/div/div[1]/div/div/div/div[3]/div[1]/form/input")[0]
    else:
        python_button = d.find_elements_by_xpath("/html/body/div[2]/div/div/div/div/div[1]/div[3]/div[1]/form/input")[0]
        time.sleep(1)

    python_button.send_keys(arg)
    time.sleep(3)
    python_button.send_keys(Keys.RETURN)
    python_button.send_keys(Keys.RETURN)
    time.sleep(9)

    # job info section
    python_button = d.find_elements_by_xpath("/html/body/div[6]/div/div/div/div/div/div[2]/div/div[2]/div/section[2]/section[2]/div[2]/div[1]/div[2]/div/div/div/div/div/div[1]/div/span/div/button[2]/span/span")[0] # job info section clock icon
    python_button.click()
    time.sleep(4)
    python_button = d.find_elements_by_xpath("/html/body/div[3]/div[2]/section/div/div/div/div[1]/div/footer/div/button[1]/span")[0]      # insert record
    python_button.click()
    time.sleep(4)

    # pick date
    python_button = d.find_elements_by_xpath("/html/body/div[3]/div[2]/section/div/div/div/div/section/div[1]/div[2]/div/div/div[1]/input")[0]  # select date box
    python_button.send_keys(Keys.CONTROL, "a")
    python_button.send_keys(date)
    python_button.send_keys(Keys.ENTER)
    time.sleep(3)

    # event
    python_button = d.find_elements_by_xpath("/html/body/div[3]/div[2]/section/div/div/div/div/section/div[3]/div/div/div[2]/div/div/div/div[2]/div/div/div[1]/input")[0]       # textbox
    python_button.send_keys("Return to Work")
    time.sleep(2)
    python_button = d.find_elements_by_xpath("/html/body/div[3]/div[4]/div/div/div/ul/li[10]")[0]  # return to work event 
    python_button.click()
    time.sleep(3)

    # event reason
    python_button = d.find_elements_by_xpath("/html/body/div[3]/div[2]/section/div/div/div/div/section/div[3]/div/div/div[2]/div/div[2]/div/div[2]/div/div/div[1]/input")[0]  # return to work event reason
    python_button.send_keys("return")
    time.sleep(2)
    python_button = d.find_elements_by_xpath("/html/body/div[3]/div[6]/div/div/div/div/div/ul/li[4]")[0]    # select event reason
    python_button.click()
    time.sleep(2)

    # save and close
    python_button = d.find_elements_by_xpath("/html/body/div[3]/div[2]/section/div/div/div/div/footer/div/button[2]/span")[0]    # save button
    python_button.click()
    time.sleep(12)
    python_button = d.find_elements_by_xpath("/html/body/div[3]/div[2]/section/div/div/div/div[2]/div/header/div/div[3]/button")[0]    # close job info box
    python_button.click()
    time.sleep(5)


# asks user to select instance ===============================================================================================================================
def get_input():
    global is_prod
    print("Which instance?")
    print("[1] Production")
    print("[2] T1")
    instance_id = input()

    if instance_id == "1":      # prod
        is_prod = True
        login_wait(p_url)
    elif instance_id == "2":      # t1
        is_prod = False
        login_wait(t1_url)
    else:
        print("Invalid instance!\n")
        get_input()

    # checks which instance, then processes data
    for i, j in zip(target_list, target_date): 
        print("Processing: ", i, j)
        try:
            if is_prod == True:
                process_me_prod(i, j)   # process prod
            else:
                process_me(i, j)        # process T1
        except Exception as e:
            # print(e)
            traceback.print_exc() # prints error log
            print("ERROR: ", i, j)
            new_list.append([i,j]) # appends to error file
            input("press enter to continue")


# main driver section ============================================================================================================
if __name__ == "__main__":

    load_file()         # loads input data into memory
    get_input()         # asks which instance it is and processes data
    save_error_file()   # saves error file

    # Time to complete process
    time_amount = "%.2f" % ((time.time() - start_time)/60)
    print("Basic --- Time in minutes: ---", time_amount)
