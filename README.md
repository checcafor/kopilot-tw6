
# ProgettoTW6
<a name="readme-top"></a>
<!-- PROJECT SHIELDS -->
[![Apache][license-shield]][license-url]
[![GitHub][GitHub.com]][GitHub-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/checcafor/kopilot-tw6">
    <img src="static/img/readme/logo.png" alt="Logo" width="200" height="80">
  </a>

  <!-- <h3 align="center">Ko-pilot</h3> -->
  <br>

  <p align="center">
    An awesome way to move green!
    <br />
    <a href="#explore"><strong>Explore the docs »</strong></a>
    <br>
    <br>
    <a href="#">View Online Demo</a>

  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

<a name="explore"></a>
<div align="center" style="margin-top: 30px">
    <img src="static/img/readme/preview.png" alt="Logo">
</div>

This project was conceived with the goal of optimizing short-distance transportation. The concept is straightforward: it involves two key roles— the "driver" (i.e. the individual offering the ride) and the "kopilot" (i.e. the person seeking the ride). Eligibility for providing a ride is limited to drivers located within one kilometer of the kopilot making the request.
By implementing this proximity-based system, individuals heading towards the same destination, whether for better or worse, can share a ride in the same vehicle. This approach not only diminishes the number of cars on the road but also contributes significantly to the reduction of CO2 emissions. Given that carbon emissions pose a considerable contemporary challenge, this initiative plays a crucial role in addressing and mitigating this environmental concern.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- BUILD WITH -->
## Built With

A combination of the latest technologies was used for this project. In particular, front-end frameworks such as bootstrap for some features and Jinja which is part of Flask were used.
As regards the back-end, the only framework for implementing the server used is Flask, with the modules necessary to implement the PWA. As regards the use of APIs, the only ones used are those of Google Maps, regarding the geographical position and coordinate conversion.

### Front-end:

![CSS3]
![HTML5]
![JavaScript]
[![JQuery][JQuery.com]][JQuery-url]
[![Jinja][Jinja.com]][Jinja-url]
[![Bootstrap][Bootstrap.com]][Bootstrap-url]

### Back-end:

[![Python][Python.com]][Python-url]
[![SQLite][SQLite.com]][SQLite-url]
[![Flask][Flask.com]][Flask-url]

### API's:

[![Google][Google.com]][Google-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- SYSTEM REQUIREMENTS -->
## System Requirements

> [!IMPORTANT]
> To correctly execute the behavior of this PWA you must have the following prerequisites pre-installed on your system:
> - Python 3.x
> - pip (Python Package Installer) - latest version

If you think you cannot meet these requirements, or at least not the recommended version, we recommend you check the installation of them by following this tutorial [here](https://github.com/r3aprz/Python-installation-tutorial).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- SETTING UP VENV -->
## Setting Up the Virtual Environment

1. Ensure you have Python correctly installed (and at the latest version) on your system.

2. Open the terminal:
    - On Windows: Use Command Prompt.
    - On macOS and Linux: Use the system terminal.
    
3. Navigate to your project directory if necessary.

4. Create a virtual environment by running the following command:
    ```bash
    python -m venv venv
    ```
5. Then enter in the virtual environment
    - For MacOS or Linux systems:
        ```bash
        source venv/bin/activate
        ```
    - For Windows:
        ```bash
        venv\Scripts\activate
        ```
		> **Warning**  
		> Some versions of Windows may restrict the execution of scripts such as `.bat` from the terminal for security reasons. Make sure you have this option ***disabled***. You may find this option under the name *UAC* (User Access Control).
6. Install dependencies:
    ```bash
    pip install --upgrade -r requirements.txt
    ```
    Then, to update any modules:
    ```bash
    pip install --upgrade Flask Werkzeug click itsdangerous Jinja2 MarkupSafe Flask-WTF WTForms email_validator websocket_server
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- STARTING THE PWA -->
## Starting the PWA

1. Run the application by typing:
    ```bash
    python app.py
    ```
    The application should now be accessible at [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your web-browser.


<!-- LICENSE -->
## License
> [!WARNING] 
> Distributed under the Apache `2.0 License`. See <a href="https://github.com/checcafor/kopilot-tw6/blob/main/LICENSE">LICENSE</a> for more information.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact
> [!NOTE] 
> De Micco Francesco - [linkedin](https://www.linkedin.com/in/francesco-de-micco-b55034210/) - francesco.demicco001@studenti.uniparthenope.it <br>
> Formisano Francesca - [linkedin](https://www.linkedin.com/in/francesca-formisano-056460263/) - francesca.formisano001@studenti.uniparthenope.it <br>
> Fusco Giuseppe - [linkedin](???) - giuseppe.fusco001@studenti.uniparthenope.it
> 
> Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[license-shield]: https://img.shields.io/badge/apache-%23D42029.svg?style=for-the-badge&logo=apache&logoColor=white
[license-url]: https://github.com/checcafor/kopilot-tw6/blob/main/LICENSE

[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[CSS3]: https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white
[HTML5]: https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white
[JAVASCRIPT]: https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E
[Python.com]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[SQLite.com]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white
[SQLite-url]: https://www.sqlite.org/index.html
[Jinja.com]: https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black
[Jinja-url]: https://jinja.palletsprojects.com/en/3.1.x/
[GitHub.com]: https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white
[GitHub-url]: https://github.com/
[Flask.com]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/en/3.0.x/
[Google.com]: https://img.shields.io/badge/google-4285F4?style=for-the-badge&logo=google&logoColor=white
[Google-url]: https://developers.google.com/maps/documentation/javascript/get-api-key?hl=it
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 