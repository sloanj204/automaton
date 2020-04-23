from selenium import webdriver
import time, csv, traceback, os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
os.system('cls')            # clears up cmd screen
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
t1_components = {
    "first_search_bar" : "/html/body/div[3]/div/div/div/div/section/div/div[2]/section/div[2]/div/div/div[1]/div/div/div/div[3]/div[1]/form/input",
    "typical_search_bar" : "/html/body/div[2]/div/div/div/div/div[1]/div[3]/div[1]/form/input",
    "job_info_clock_icon" : "/html/body/div[6]/div/div/div/div/div/div[2]/div/div[2]/div/section[2]/section[2]/div[2]/div[1]/div[2]/div/div/div/div/div/div[1]/div/span/div/button[2]",
    "job_info_insert_record_icon" : "/html/body/div[3]/div[2]/section/div/div/div/div[1]/div/footer/div/button[1]/span",
    "date_field" : "/html/body/div[3]/div[2]/section/div/div/div/div/section/div[2]/div[2]/div/div/input",
    "event_field" : "/html/body/div[3]/div[2]/section/div/div/div/div/section/div[4]/div/div/div[2]/div/div/div/div[2]/div/div/input",
    "return_to_work_event" : "/html/body/div[3]/div[4]/div/div/div/ul/li[12]",
    "event_reason_field" : "/html/body/div[3]/div[2]/section/div/div/div/div/section/div[4]/div/div/div[2]/div/div[2]/div/div[2]/div/div/input",
    "return_to_work_event_reason" :"/html/body/div[3]/div[6]/div/div/div/div/div/ul/li[3]",
    "save_button" : "/html/body/div[3]/div[2]/section/div/div/div/div/footer/div/button[2]/span[1]/span",
    "close_window" : "/html/body/div[3]/div[2]/section/div/div/div/div[2]/div/header/div/div[3]/button"
}
prod_components = {
    "first_search_bar" : "/html/body/div[3]/div/div/div/div/section/div/div[2]/section/div[2]/div/div/div[1]/div/div/div/div[3]/div[1]/form/input",
    "typical_search_bar" : "/html/body/div[2]/div/div/div/div/div[1]/div[3]/div[1]/form/input",
    "job_info_clock_icon" : "/html/body/div[6]/div/div/div/div/div/div[2]/div/div[2]/div/section[2]/section[2]/div[2]/div[1]/div[2]/div/div/div/div/div/div[1]/div/span/div/button[2]/span/span",
    "job_info_insert_record_icon" : "/html/body/div[3]/div[2]/section/div/div/div/div[1]/div/footer/div/button[1]/span",
    "date_field" : "/html/body/div[3]/div[2]/section/div/div/div/div/section/div[1]/div[2]/div/div/div[1]/input",
    "event_field" : "/html/body/div[3]/div[2]/section/div/div/div/div/section/div[3]/div/div/div[2]/div/div/div/div[2]/div/div/div[1]/input",
    "return_to_work_event" : "/html/body/div[3]/div[4]/div/div/div/ul/li[10]",
    "event_reason_field" : "/html/body/div[3]/div[2]/section/div/div/div/div/section/div[3]/div/div/div[2]/div/div[2]/div/div[2]/div/div/div[1]/input",
    "return_to_work_event_reason" : "/html/body/div[3]/div[6]/div/div/div/div/div/ul/li[4]",
    "save_button" : "/html/body/div[3]/div[2]/section/div/div/div/div/footer/div/button[2]/span",
    "close_window" : "/html/body/div[3]/div[2]/section/div/div/div/div[2]/div/header/div/div[3]/button"
}
# ----------------------------------------------------------------------

# loads input records ---------------------------------------------------------------------------------------------------
def load_file():
    try:
        with open(target_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                target_list.append(row[0])
                target_date.append(row[1])
    except:
        print("ERROR: input file not found. Please use", target_file)
        input("Press Enter to try again.")
        load_file()

# outputs error file ----------------------------------------------------------------------------------------------------
def save_error_file():
    with open(error_file, "w", newline="") as resultFile:
        wr = csv.writer(resultFile, delimiter=',')
        for row in new_list:
                wr.writerows([row])

# login for Production --------------------------------------------------------------------------------------------------
def login_wait(instance_url):
    d.get(instance_url)     # URL of Successfactors Instance
    input("Press Enter key to continue once you've logged in and EC has finished loading.")

""" =============================================================================================================
    Processes records
    (main function to process records. Pulls from target.csv)

    PARAMETERS:
    arg:            Employee ID
    date:           Date
    my_instance:    flag to specify which instance
    ================================================================================================================
"""
def process_me(arg, date, my_instance):
    global is_first
    wait = WebDriverWait(d, 10)
    
    if is_first == True:
        time.sleep(5)
        python_button = wait.until(EC.element_to_be_clickable((By.XPATH, my_instance["first_search_bar"])))  
    else:
        python_button = wait.until(EC.element_to_be_clickable((By.XPATH, my_instance["typical_search_bar"])))

    python_button.send_keys(arg)
    time.sleep(3)
    python_button.send_keys(Keys.RETURN)
    python_button.send_keys(Keys.RETURN)
    time.sleep(9) # lets profile page load
    
    # job info section
    python_button = wait.until(EC.element_to_be_clickable((By.XPATH, my_instance["job_info_clock_icon"])))
    is_first = False
    python_button.click()
    time.sleep(4) # otherwise clicks the "load more" button 
    
    python_button = wait.until(EC.element_to_be_clickable((By.XPATH, my_instance["job_info_insert_record_icon"])))   
    python_button.click()
    time.sleep(4)

    # pick date
    python_button = wait.until(EC.element_to_be_clickable((By.XPATH, my_instance["date_field"])))
    python_button.send_keys(Keys.CONTROL, "a")
    python_button.send_keys(date)
    python_button.send_keys(Keys.ENTER)
    time.sleep(3)

    # event
    python_button = wait.until(EC.element_to_be_clickable((By.XPATH, my_instance["event_field"]))) 
    python_button.send_keys("return")
    time.sleep(2)
    python_button = wait.until(EC.element_to_be_clickable((By.XPATH, my_instance["return_to_work_event"])))  
    python_button.click()
    time.sleep(3)

    # event reason
    python_button = wait.until(EC.element_to_be_clickable((By.XPATH, my_instance["event_reason_field"]))) 
    python_button.send_keys("return")
    time.sleep(2)
    python_button = wait.until(EC.element_to_be_clickable((By.XPATH, my_instance["return_to_work_event_reason"]))) 
    python_button.click()
    time.sleep(2)

    # save and close
    python_button = wait.until(EC.element_to_be_clickable((By.XPATH, my_instance["save_button"])))  # save button
    python_button.click()
    time.sleep(12) # 4 in T1
    python_button = wait.until(EC.element_to_be_clickable((By.XPATH, my_instance["close_window"])))    # close job info box
    python_button.click()
    time.sleep(5) # 4 in T1


# asks user to select instance ===============================================================================================================================
def get_input():
    global is_prod
    global t1_components
    global prod_components
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
                process_me(i, j, prod_components)   # process prod
            else:
                # process_t1(i, j)        # process T1
                process_me(i, j, t1_components)
        except Exception as e:
            # print(e)
            traceback.print_exc() # prints error log
            print("ERROR: ", i, j)
            new_list.append([i,j]) # appends to error file
            input("press enter to continue with next record after you have closed the job info box.")


# main driver section ============================================================================================================
if __name__ == "__main__":

    load_file()         # loads input data into memory
    get_input()         # asks which instance it is and processes data
    save_error_file()   # saves error file

    # Time to complete process
    time_amount = "%.2f" % ((time.time() - start_time)/60)
    print("Basic --- Time in minutes: ---", time_amount)
