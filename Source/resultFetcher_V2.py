#REWRITING FUNTION For readability
#IMPORTING DEPENDENCIES
import sys #for command line arguments (used in script note in ipynb)
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select #for selecting option
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions #for checking alert
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
#from selenium.webdriver.support import expected_conditions as EC


site_bput = 'http://www.bputexam.in/StudentSection/ResultPublished/StudentResult.aspx'

driver = webdriver.Chrome()
site_bput ='http://www.bputexam.in/StudentSection/ResultPublished/StudentResult.aspx'
driver.get(site_bput)

filename = 'results_5th_sem.txt'
if(len(sys.argv)>=4):
	filename = sys.argv[3]

result_store = open(filename,'a')

#REWRITING FUNTION For readability
def secondClick():#clicking 2ND view result BUTTON
    try:
        view_result2 = driver.find_elements_by_id("gvResultSummary_ctl02_lnkViewResult")
        #if results not found
        if len(view_result2)==0:
            return False
        #BOOLEAN-flag for desired result there may be multiple result(back,2nd sem,4th sem) we have to select one
        desired_result=False
        for i in range(1,6):
            view_result_subject_code = driver.find_elements_by_id("gvResultSummary_ctl0"+str(i)+"_lblSubCode")
            #finding subject of 5th semester so that respective button can be clicked
            for result in view_result_subject_code:
                if str(result.text).find('5TH')!=-1:
                    #A
                    #Clicking on any white space to come out of text box
                    action = webdriver.common.action_chains.ActionChains(driver)
                    action.move_by_offset(150,0) #move 150 pixels to the right to access Help link
                    action.click()
                    action.perform()
                    result_view_button = driver.find_element_by_id("gvResultSummary_ctl0"+str(i)+"_lnkViewResult")
                    #result_view_button.click()
                    driver.execute_script("arguments[0].click();", result_view_button)
                    #print("SECOND CLICK DONE\n")
                    desired_result=True
                    break
            if desired_result:
                return True
        return False
    except Exception:
        return False
def findGrade(regno):
    #Exam session option
    exam_option = Select(driver.find_element_by_name('ddlSession'))
    #registration Number field
    registerationNo_text = driver.find_element_by_id('txtRegNo');
    #date of Birth field
    birth_date_text = driver.find_element_by_id('dpStudentdob_dateInput');

    ###########FORM FILL
    #Exam session::
    exam_option.select_by_visible_text("Odd(2017-18)")
    #Registration no value::
    registerationNo_text.clear()
    registerationNo_text.send_keys(regno)
    #date of Birth value:refilling dob is not required though
    birth_date_text.clear()
    birth_date_text.send_keys("10/10/1996")

    #########VIEW RESULT
    #clicking view Result Button
    #Firstly
    #Clicking on any white space to come out of text box
    try:
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_by_offset(150,0) #move 150 pixels to the right to access Help link
        action.click()
        action.perform()
        #Click on View Result Button
        view_result = driver.find_element_by_id("btnView")
        driver.execute_script("arguments[0].click();", view_result)
    except Exception:
        return "No result Found(404E)",""

    #if click produces exception or gives alert
    do_nothing = True
    try:
        WebDriverWait(driver,3).until(expected_conditions.alert_is_present())
        driver.switch_to_alert().accept()
        driver.get(site_bput)
        return "no result found(SiteErrorE)",""
    except TimeoutException:
        do_nothing = False

    #clicking 2ND view result BUTTON
    if not secondClick():
        return "No result Found",""

    #########FETCH RESULT
    #fetch result_table
    result_table = driver.find_elements_by_xpath('//form[1]//div[@id="tblBasicDetail"]//table[@class="pure-table pure-table-striped pure-table-bordered"]//tbody//tr')
    #Student NAME fetch
    student_name_row = driver.find_element_by_xpath('//form[1]//div[@id="tblBasicDetail"]//table[@class="pure-table pure-table-striped pure-table-bordered"]//tbody//tr//td//span[@id="lblName"]')
    student_name = str(student_name_row.text)
    #student SGPA
    #selecting data table inside BIGGER RESULT TABLE
    #sgpa row is in a table inside a result_table's 7th row
    all_elements_of_data_table = result_table[5].find_elements_by_xpath('.//td')

    #sgpa is the second last element of the table if we see(SGPA: X:YZ format )
    second_last_index = len(all_elements_of_data_table)-2
    sgpa_val = "N/A"
    #sgpa_val is in format(SGPA: X:YZ)
    if all_elements_of_data_table[second_last_index]:
        sgpa_val = all_elements_of_data_table[second_last_index]
        sgpa_val = float(sgpa_val.text.split(" ")[1])

    return student_name,sgpa_val

regnoStart = 1501202001
regnoEnd = 1501202900

if(len(sys.argv)>=2):
	regnoStart = int(sys.argv[1])
if(len(sys.argv)>=3):
	regnoEnd = int(sys.argv[2])

starting_time = time.time()

result_store.write("Script::resultFetcher.py Author::livingstonegcs@gmail.com,NIST-Berhampur\n")
result_store.write("Range_Regno, From:"+str(regnoStart)+" to "+ str(regnoEnd)+"\n")
while regnoStart<=regnoEnd:
    ###result_store = open(filename,'a')
    #Extracting information 30-students-set-wise
    for i in range(1,30):
        result_store = open(filename,'a')
        driver.get('http://www.bputexam.in/StudentSection/ResultPublished/StudentResult.aspx')
        name,cgpa = findGrade(regnoStart)
        if len(str(cgpa))==0:
            driver.get('http://www.bputexam.in/StudentSection/ResultPublished/StudentResult.aspx')
            name,cgpa = findGrade(regnoStart)
        #Writing in the console
        print(str(regnoStart) + "    " + name + "   " + str(cgpa))
        #writing in FILE
        result_store.write(str(regnoStart) + "    " + name + "   " + str(cgpa) + "\n" )
        result_store.close()
        regnoStart = regnoStart + 1
        if regnoStart>regnoEnd:
        	break
###result_store.close()

ending_time = time.time()

driver.close()
#Writing time taken
result_store = open(filename,'a')
result_store.write("Time taken: "+str(int((ending_time-starting_time)//60))+" Mins "+ str(int((ending_time-starting_time)%60))+" Secs\n")
result_store.close()

print("Time taken: "+str(int((ending_time-starting_time)//60))+" Mins "+ str(int((ending_time-starting_time)%60))+" Secs")
