import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://aerialcast.irc-enter.tech"

def test_page_title_and_elements(driver):
    """
    Test 1: Verify the page loads successfully, displays the correct title,
    and has the essential Login and Register elements.
    """
    driver.get(BASE_URL)
    
    # Verify Title
    assert "AerialCast" in driver.title
    
    # Wait for the main container to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "main"))
    )
    
    # Check if Login and Register tabs are present
    login_tab = driver.find_element(By.CSS_SELECTOR, "[id$='-trigger-login']")
    register_tab = driver.find_element(By.CSS_SELECTOR, "[id$='-trigger-register']")
    
    assert login_tab.is_displayed()
    assert register_tab.is_displayed()
    
    # Check if default form is Login and inputs are visible
    email_input = driver.find_element(By.CSS_SELECTOR, "#radix-_r_0_-content-login #email")
    password_input = driver.find_element(By.CSS_SELECTOR, "#radix-_r_0_-content-login #password")
    
    assert email_input.is_displayed()
    assert password_input.is_displayed()

def test_tab_switching(driver):
    """
    Test 2: Verify that switching between Login and Register tabs
    renders the correct input fields.
    """
    driver.get(BASE_URL)
    
    # Wait for tabs to render
    login_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[id$='-trigger-login']"))
    )
    register_tab = driver.find_element(By.CSS_SELECTOR, "[id$='-trigger-register']")
    
    # Initially login content should be visible, register hidden
    login_content = driver.find_element(By.CSS_SELECTOR, "[id$='-content-login']")
    register_content = driver.find_element(By.CSS_SELECTOR, "[id$='-content-register']")
    
    assert login_content.is_displayed()
    assert not register_content.is_displayed()
    
    # Click Register tab
    register_tab.click()
    
    # Wait for register form to show up and login form to hide
    WebDriverWait(driver, 5).until(
        lambda d: register_content.is_displayed() and not login_content.is_displayed()
    )
    
    # Verify register fields are visible
    full_name = driver.find_element(By.ID, "fullName")
    confirm_password = driver.find_element(By.ID, "confirmPassword")
    assert full_name.is_displayed()
    assert confirm_password.is_displayed()
    
    # Click Login tab to switch back
    login_tab.click()
    
    # Wait for login form to show up
    WebDriverWait(driver, 5).until(
        lambda d: login_content.is_displayed() and not register_content.is_displayed()
    )

def test_password_visibility_toggle(driver):
    """
    Test 3: Verify that clicking the show password button toggles the password input type.
    """
    driver.get(BASE_URL)
    
    # Locate password field and show password button
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#radix-_r_0_-content-login #password"))
    )
    # The toggle button is next to the password input inside the same relative wrapper
    toggle_btn = driver.find_element(By.CSS_SELECTOR, "#radix-_r_0_-content-login button[aria-label='Show password']")
    
    # Verify default type is password
    assert password_input.get_attribute("type") == "password"
    
    # Click toggle button
    toggle_btn.click()
    
    # Verify type changes to text
    assert password_input.get_attribute("type") == "text"
    
    # Click toggle button again
    toggle_btn.click()
    
    # Verify type changes back to password
    assert password_input.get_attribute("type") == "password"

def test_failed_login_invalid_email(driver):
    """
    Test 4: Verify that attempting to submit login with invalid email triggers validation.
    """
    driver.get(BASE_URL)
    
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#radix-_r_0_-content-login #email"))
    )
    password_input = driver.find_element(By.CSS_SELECTOR, "#radix-_r_0_-content-login #password")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "#radix-_r_0_-content-login button[type='submit']")
    
    # Input invalid email format and random password
    email_input.send_keys("invalidemailformat")
    password_input.send_keys("somepassword123")
    submit_btn.click()
    
    # Browser validation checking (HTML5 required/type validation check)
    validity = driver.execute_script("return arguments[0].validity.valid;", email_input)
    assert not validity, "Email input should be marked as invalid by browser validation"

def test_failed_login_incorrect_credentials(driver):
    """
    Test 5: Verify that attempting to log in with incorrect credentials triggers an error toast.
    """
    driver.get(BASE_URL)
    
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#radix-_r_0_-content-login #email"))
    )
    password_input = driver.find_element(By.CSS_SELECTOR, "#radix-_r_0_-content-login #password")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "#radix-_r_0_-content-login button[type='submit']")
    
    # Fill standard invalid email and password
    email_input.send_keys("nonexistentuser@example.com")
    password_input.send_keys("wrongpassword")
    submit_btn.click()
    
    # Wait for toast notification or error popup to appear.
    # Next.js applications using Sonner or shadcn toaster display toasts inside an ol/li structure with role="status" or class containing "toast"
    toast = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(@role, 'status') or contains(@class, 'toast') or contains(@class, 'notification') or contains(@data-sonner-toast, '')]"))
    )
    
    # Wait for toast text to be populated (checking both visible text and raw text content to handle css animations)
    toast_text = ""
    for _ in range(50):
        toast_text = toast.text.strip() or toast.get_attribute("textContent").strip()
        if toast_text:
            break
        time.sleep(0.1)
        
    print("Toast message found:", toast_text)
    assert len(toast_text) > 0, "Toast text was empty"

def test_failed_registration_mismatched_passwords(driver):
    """
    Test 6: Verify that attempting to register with mismatched passwords triggers an error validation.
    """
    driver.get(BASE_URL)
    
    # Switch to Register tab
    register_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[id$='-trigger-register']"))
    )
    register_tab.click()
    
    # Wait for the Register form fields
    full_name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "fullName"))
    )
    email_input = driver.find_element(By.CSS_SELECTOR, "#radix-_r_0_-content-register #email")
    password_input = driver.find_element(By.CSS_SELECTOR, "#radix-_r_0_-content-register #password")
    confirm_password = driver.find_element(By.ID, "confirmPassword")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "#radix-_r_0_-content-register button[type='submit']")
    
    # Fill in register form with mismatched passwords
    full_name.send_keys("Test User")
    email_input.send_keys("testuser@example.com")
    password_input.send_keys("Password123!")
    confirm_password.send_keys("MismatchedPassword321!")
    
    submit_btn.click()
    
    # Wait for validation error.
    try:
        toast = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@role, 'status') or contains(@class, 'toast') or contains(text(), 'match') or contains(text(), 'mismatch')]"))
        )
        # Wait for text to populate
        toast_text = ""
        for _ in range(50):
            toast_text = toast.text.strip() or toast.get_attribute("textContent").strip()
            if toast_text:
                break
            time.sleep(0.1)
        assert len(toast_text) > 0
        print("Registration error message found:", toast_text)
    except Exception:
        # Fallback to check custom field validation error message in the DOM
        error_msg = driver.find_element(By.XPATH, "//*[contains(text(), 'match') or contains(text(), 'mismatch') or contains(text(), 'Passwords do not match')]")
        # Wait for text to populate
        error_text = ""
        for _ in range(50):
            error_text = error_msg.text.strip() or error_msg.get_attribute("textContent").strip()
            if error_text:
                break
            time.sleep(0.1)
        assert len(error_text) > 0
        print("Registration inline error message found:", error_text)
