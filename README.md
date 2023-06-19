# Postlook

![Postlook](https://github.com/dhanjo/Postlook/assets/24205535/fca49a0d-7ee5-480c-b647-67ded86f0dda)

The Postlook Scanner is a powerful tool designed to scan the Postman website and identify publicly exposed critical company information. It leverages techniques to search for sensitive data that may have been unintentionally made public on the Postman platform.
# Features of Postlook:
1. Automated Scanning: The tool performs automated scans of the Postman site, systematically examining various endpoints, APIs, and public collections to discover potentially sensitive information.
2. Notification and Reporting: Upon completion of the scan, the tool generates a comprehensive report that highlights any publicly exposed critical company information found.
3. User-Friendly Interface: The tool offers an intuitive and user-friendly interface, making it accessible to security professionals, developers, and other stakeholders. The scan results are presented in a structured and easy-to-understand format, enabling efficient analysis and remediation.
 
# Working of Postlook
The Postlook tool is written in Python and scans the Postman website for finding publicly available data related to the keyword.

# Installation

`pip install -r requirment.txt`

# Usage 

`python postlook.py [-h] [-q <Organization Name>] [-o <Output File Name>]`














