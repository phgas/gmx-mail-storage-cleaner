# GMX Mail Storage Cleaner

The GMX Mail Storage Cleaner script automates the deletion of emails in your GMX mailbox. Instead of manually deleting a maximum of 50 emails per request, this script retrieves the total number of emails in a specified folder, fetches their URIs, and deletes them in bulk. This is particularly useful for cleaning up large volumes of emails efficiently.
## Prerequisites

- Python 3.11
- pip

## Installation

1. Clone this repository:
    ```
    git clone https://github.com/phgas/gmx-mail-storage-cleaner.git
    ```
    
2. Change directory:
    ```
    cd gmx-mail-storage-cleaner
    ```
    
3. Install the required Python packages:
    ```
    pip install -r requirements.txt
    ```

## Configuration

1. Login to your Gmx-Account and press F12 to open Chrome DevTools (if you are using another web browser do self dilligence).

2. Change to the Network tab, activate `Preserve Log` and filter for `Fetch/XHR`.

3. Clear the network log, click on "Posteingang" and in the logs look for `folders?` -> from Requests Headers copy Bearer Token (BEARER_TOKEN_TO_RETRIEVE)
   
5. Clear the network log, delete a mail and in the logs look for `MailBatchDelete?` -> from Requests Headers copy Bearer Token (BEARER_TOKEN_TO_DELETE)
6. Create a `.env` file in the project directory and add your two Bearer Tokens:
    ```
    BEARER_TOKEN_TO_RETRIEVE = "Bearer ..."
    BEARER_TOKEN_TO_DELETE = "Bearer ..."
    ```

## Usage

Run the Python script:

```
python main.py
```

## Additional Information
- Make sure your `.env` file is correctly set up with your GMX API tokens.
- The script handles both `INBOX` and `TRASH` folders by default, but you can modify the folder types as needed.
