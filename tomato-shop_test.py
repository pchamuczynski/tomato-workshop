#!/usr/bin/env python3

from playwright.sync_api import sync_playwright, expect
import sys

def select_option_with_validation(page, selector, value):
    """Select an option and validate its availability."""
    options = page.locator(f"{selector} option").all_text_contents()
    if value not in options:
        error = f"Error: Option '{value}' is not available in {selector}. Available options: {options}"
        return False, error # Continue execution without selecting the option
    page.select_option(selector, value)
    return True, "OK"

def test_select_product(page, data):
        
        if 'product' in data:
            result, error = select_option_with_validation(page, "#product", data['product'])
            if not result:
                print(f"❌: {data}: {error}")
        if 'color' in data:
            result, error = select_option_with_validation(page, "#color", data['color'])
            if not result:
                print(f"❌: {data}: {error}")
        if 'size' in data:
            result, error = select_option_with_validation(page, "#size", data['size'])
            if not result:
                print(f"❌: {data}: {error}")
        if 'quantity' in data:
            page.fill("#quantity", str(data['quantity']))
        if 'country' in data:
            result, error = select_option_with_validation(page, "#country", data['country'])
            if not result:
                print(f"❌: {data}: {error}")
        if 'name' in data:
            page.fill("#name", data['name'])
        if 'address' in data:
            page.fill("#address", data['address'])
        if 'phone' in data:  
            page.fill("#phone", data['phone'])
        if 'email' in data:
            page.fill("#email", data['email'])
        if 'payment' in data:
            result, error = select_option_with_validation(page, "#payment", data['payment'])
            if not result:
                print(f"❌: {data}: {error}")
        if 'delivery' in data:
            result, error = select_option_with_validation(page, "#delivery", data['delivery'])
            if not result:
                print(f"❌: {data}: {error}")

        page.click("#submit")

        # Wait for the status element to contain the expected value
        status_element = page.locator("#status")
        status_value = status_element.input_value()
        response = page.locator("#response")
        response_value = response.input_value()

        if 'status' in data:
            expected_status = data['status'].strip()
            if not status_value.strip() == expected_status:
                print(f"❌: {data}\nUnexpected status: {status_value}, expecting {expected_status}. Response: {response_value}")
            else:
                print(f"✅: {data}\nStatus: {status_value}, Response: {response_value}")
        else:
            print(f"✅: {data}\nStatus: {status_value}, Response: {response_value}")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Launch browser
        context = browser.new_context()
        page = context.new_page()
        
        # Open the webpage
        page.goto("http://tomatoworkshopwebpage.s3-website-us-east-1.amazonaws.com/")

        csv_rows = []
        if len(sys.argv) > 1:
            # Read from file if a CLI argument is provided
            file_path = sys.argv[1]
            print(f"Reading from file: {file_path}")
            with open(file_path, "r") as file:
                for line in file:
                    csv_rows.append(line.strip())
        else:
            # Read from stdin if no CLI argument is provided
            print("Reading from stdin. Type input and press Enter:")
            for line in sys.stdin:
                csv_rows.append(line.strip())

        # first row is header. It contains the names of the fields
        header = csv_rows[0].split(",")
        mapping = {}
        for i, field in enumerate(header):
            mapping[field] = i
        # the rest of the rows are data
        for row in csv_rows[1:]:
            values = row.split(",")
            data = {}
            for field, i in mapping.items():
                data[field] = values[i]
            test_select_product(page, data)

if __name__ == "__main__":
    main()
