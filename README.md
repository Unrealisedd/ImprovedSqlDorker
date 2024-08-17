# SQLDorker

**SQLDorker** is a Python-based tool designed for discovering SQL injection vulnerabilities using Google dorking and payload-based testing. It combines the power of Tor for anonymity, Wappalyzer for technology detection, and a set of SQL injection payloads to help security professionals and researchers identify vulnerabilities in web applications.

## Features

- **Google Dorking**: Automatically fetches URLs using customizable Google search queries.
- **Tor Integration**: Uses Tor for IP rotation to minimize detection and rate limiting.
- **Technology Detection**: Identifies technologies used on target websites with Wappalyzer.
- **SQL Injection Testing**: Tests URLs for SQL injection vulnerabilities using a variety of payloads.
- **Customizable Payloads**: Loads payloads specific to detected technologies and generic payloads for broader coverage.
- **Error Handling**: Gracefully handles various errors, including rate limiting and timeout issues.

## Installation

To use SQLDorker, you'll need Python 3.6 or higher. Follow these steps to set up the tool:

1. **Clone the Repository**

    ```
    git clone https://github.com/yourusername/sqldorker.git
    cd sqldorker
    ```

2. **Install Dependencies**

    Create a virtual environment and install the required packages:

    ```
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. **Install Tor and TorNet**

    - **Tor**: Install Tor from [the official Tor website](https://www.torproject.org/download/).
    - **TorNet**: Install `tornet` using pip:

    ```
    pip install tornet
    ```

4. **Download Payloads**

    Create a directory named `payloads` in the root of the repository and place your SQL injection payload files (`mssql.txt`, `mysql.txt`, etc.) inside it.

## Usage

1. **Run the Tool**

    Execute the script to start the tool:

    ```
    python sqldorker.py
    ```

2. **Provide Input**

    - **Google Dorking Parameter**: Enter a Google search dork (e.g., `inurl:"?id="`).
    - **Number of Requests**: Specify how many URLs to fetch.

3. **Review Results**

    The tool will display the fetched URLs and indicate any detected SQL injection vulnerabilities. Errors such as rate limiting or timeouts will be handled gracefully.

## Example

```
Enter the Google dorking parameter (e.g., inurl:"?id="): inurl:"?id="
Enter the number of requests to make: 10
```

The tool will fetch URLs based on the dork, test them for SQL injection vulnerabilities, and provide feedback on each URL.

## Error Handling

- **403 Errors**: Indicates that access to the URL is not allowed.
- **429 Errors**: Too Many Requests - the tool will pause and retry after a delay.
- **Redirects**: Redirects to different domains are skipped.
- **Connection Errors**: Includes handling for timeouts and other connection issues.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork the Repository**

2. **Create a Branch**

    ```bash
    git checkout -b feature/your-feature
    ```

3. **Make Changes and Commit**

    ```bash
    git add .
    git commit -m "Add your feature"
    ```

4. **Push to Your Fork**

    ```bash
    git push origin feature/your-feature
    ```

5. **Create a Pull Request**

    Go to the original repository and create a pull request from your branch.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Wappalyzer**: For technology detection.
- **Tor Project**: For providing anonymity through Tor.
- **Google**: For search capabilities.
