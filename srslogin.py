from selenium import webdriver
import email
import imaplib

srsUsername = "" # id here
srsPassword = "" # password here

driver = webdriver.Chrome()
driver.get("https://stars.bilkent.edu.tr/srs/")

nameBox = driver.find_element_by_xpath('//*[@id="LoginForm_username"]')
passwordBox = driver.find_element_by_xpath('//*[contains(@id,"LoginForm-p")]')
submitBtn = driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div/div[1]/div[3]/button')

nameBox.send_keys(srsUsername)
passwordBox.send_keys(srsPassword)

submitBtn.click()

# getting the verification code from mail
username = '' # username of mail
password = '' # password of mail

mail = imaplib.IMAP4_SSL("") #imap server as parameter
mail.login(username,password)

mail.select("inbox")

code = None	
while code == None:
	result, data = mail.uid("search", None, 'UNSEEN') # get only unseen codes.

	inbox_item_list = data[0].split()
	most_recent = inbox_item_list[-1] # last item

	res, email_data = mail.uid('fetch', most_recent, '(RFC822)') # res = "OK", its a result.
	 
	raw_email = email_data[0][1].decode("utf-8")

	email_message = email.message_from_string(raw_email)

	subject = email_message['Subject']

	if subject == "Secure Login Gateway E-Mail Verification Code".strip():
		text = email_message.get_payload() # since there is only one text/plain
		index = text.index(':')
		code = text.strip()[index + 2 : index + 7] # verification code
		
codeBox = driver.find_element_by_xpath('//*[@id="EmailVerifyForm_verifyCode"]')
verifyBtn = driver.find_element_by_xpath('//*[@id="verifyEmail-form"]/fieldset/div/div[1]/div[2]/button')

codeBox.send_keys(code)
verifyBtn.click()


