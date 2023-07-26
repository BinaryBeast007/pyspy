<a name="readme-top"></a>

<p  align="center"><img width="600px" src="https://github.com/BinaryBeast007/pyspy/blob/main/assets/pyspy.gif"></p>


<h2 align="center">PySpy</h2>
<p align="center">
    A System Monitoring and Logging Tool
    <br />
    <strong>Explore the docs »</strong>
    <br />
    <a href="https://github.com/BinaryBeast007/pyspy/issues">Report Bug</a>
    ·
    <a href="https://github.com/BinaryBeast007/pyspy/issues">Request Feature</a></p>

<!-- TABLE OF CONTENTS -->
<details open>
  <summary><b>Table of Contents</b></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#dependencies">Dependencies</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#usage">Usage</a></li>
      </ul>
    </li>
    <li><a href="#features">Features</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#disclaimer">Disclaimer</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project
PySpy is a Python-based system monitoring and logging tool designed to gather various system information, capture screenshots, record audio, and retrieve network information, including Wi-Fi profiles, passwords and extracts Google Chrome's saved passwords. It provides a convenient way to package this information into a zip file and send it via email for remote monitoring or troubleshooting purposes. Please note that this tool should only be used for educational and ethical purposes, and any unauthorized use may violate privacy laws and regulations.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

Getting started with [Python](https://www.python.org/about/gettingstarted/)
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Dependencies

Before running PySpy, make sure you have Python 3.x installed on your system. Additionally, you need to install the required Python modules listed in the `requirements.txt` file. You can install them using the following command:

```bash
pip install -r requirements.txt
```

or

```bash
pip install psutil pyaudio wave Pillow requests pycryptodomex pywin32
```

If you prefer to install the modules manually, here's the list of required Python modules:
```bash
psutil
pyaudio
wave
Pillow
requests
pycryptodomex 
pywin32 

```
<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Installation

- Clone the repo
   ```bash
   git clone https://github.com/BinaryBeast007/pyspy
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Usage

To use PySpy for email notifications, you will need to set up a Mailtrap account with temporary mail. Follow the steps below to configure PySpy with your Mailtrap credentials:

1.  **Create a Mailtrap Account**
    
    -   Go to [https://mailtrap.io/](https://mailtrap.io/) and sign up for an account with temporary mail.
2.  **Access SMTP Settings**
    
    -   After signing in, navigate to "Email Testing" and select "Inboxes" from the dropdown menu.
3.  **Obtain Mailtrap Credentials**
    
    -   In the Inboxes page, select "SMTP Settings" for the desired inbox.
    -   Locate the "Show Credentials" button and click on it. This will reveal the SMTP username and password specific to your Mailtrap inbox.
4.  **Configure PySpy Class**
    
    -   In the Python script, find the class constructor where you initialize the PySpy object.
    -   Inside the constructor, look for the lines where `self.EMAIL_ADDRESS` and `self.EMAIL_PASSWORD` are defined.
    -   Copy the previously obtained Mailtrap SMTP username and password.
    -   Replace `self.EMAIL_ADDRESS` with the Mailtrap SMTP username and `self.EMAIL_PASSWORD` with the Mailtrap SMTP password.
5.  **Save and Run**
    
    -   Save your changes to the Python script after configuring the email credentials.
    -   Now, PySpy is set up to send email notifications using the provided Mailtrap account.

To use PySpy, simply run the script:

```bash
python src/pyspy.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Features

- Gather essential system information such as OS details, CPU usage, memory usage, disk space, network interfaces, etc.
- Capture screenshots and save them for further analysis.
- Record audio and save it as a WAV file.
- Retrieve geolocation data (IP-based) using the `ipinfo.io` API.
- Retrieve Wi-Fi profiles and their corresponding passwords for connected networks.
- Extracts passwords from Google Chrome (Chrome version >= 80).
- Package all collected information into a zip file for easy sharing.
- Send the zip file as an email attachment to a specified recipient.
- Deletes the zip file and temporary folder



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the repository on GitHub.
    
2.  Create a new branch with a descriptive name:
    
    ```bash
    git checkout -b feature/your-feature-name
    ``` 
    
3.  Make your changes and commit them:
    
    ```bash
    git commit -m "Add your commit message here"
    ``` 
    
4.  Push your changes to your forked repository:
    
    ```bash
    git push origin feature/your-feature-name
    ``` 
    
5.  Open a pull request on the original repository, explaining your changes.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Disclaimer

This project and its associated source code, tools, and files are provided for educational and research purposes only. The author(s) of this project take NO responsibility and/or liability for any consequences that may arise from how you choose to use any of the provided tools, source code, or files.

**USE AT YOUR OWN RISK.**

Please ensure that you have the necessary permissions and consent before using this tool on any system or network. Unauthorized use or any malicious activities are strictly prohibited.

By using PySpy, you agree to comply with all applicable laws and regulations. The authors are not responsible for any misuse, damage, or any other potential harm caused by the use of this project.

Always use this tool responsibly and respect the privacy and security of others. If you are uncertain about the legality or ethical implications of using this tool, seek advice from legal and ethical experts before proceeding.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/BinaryBeast007/pyspy/blob/main/LICENSE) file for details.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

