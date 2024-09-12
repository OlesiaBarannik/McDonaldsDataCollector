
# McDonalds Data Collector

This project is a data collection tool for extracting product information from McDonald's website.

## Files

- **app.py**: The main application script for running the data collection.
- **mcdonalds_parser.py**: Contains the parsing logic for collecting product details.
- **products.json**: A sample output file containing collected product data.
- **requirements.txt**: List of required Python libraries for the project.
- **chromedriver.exe**: Chrome WebDriver executable for automated browsing.

## Setup

1. Clone the repository or download the project files.
2. Install the required dependencies by running:

    ```bash
    pip install -r requirements.txt
    ```

3. Ensure that you have Google Chrome installed and place the appropriate version of `chromedriver.exe` in the project folder.

4. First, run the parser to collect data:

    ```bash
    python mcdonalds_parser.py
    ```
This will extract product details from McDonald's website and save them into `products.json`.

5. Run the main script to collect data:

    ```bash
    python app.py
    ```

## Output

Once the server is running, you can access the following endpoints:

Get all products:

URL: /all_products/
Method: GET
Description: Returns all information about all products.

Get information about a specific product:

URL: /products/{product_name}
Method: GET
Description: Returns information about the exact product where {product_name} is the name of the product.

Get a specific field of a product:

URL: /products/{product_name}/{product_field}
Method: GET
Description: Returns information about a specific field of a product where {product_name} is the name of the product and {product_field} is the field of the product (e.g., calories, fats).
