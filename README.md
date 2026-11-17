\# Real-Time Performance Monitoring and Analysis of Cloud Computing System



A web-based application designed to monitor and analyze the performance of connected computer systems in real time. The system collects resource usage information and presents it through a centralized dashboard for easy monitoring and analysis.



\## Project Overview



This project provides a centralized platform to monitor multiple client computers using their IP addresses. It helps administrators observe system performance, identify resource usage issues, and generate reports.



\## Key Features



\- Real-time system performance monitoring

\- Monitoring multiple client computers using IP addresses

\- CPU usage monitoring

\- Memory usage monitoring

\- Network data sent and received monitoring

\- Disk usage monitoring

\- Interactive dashboard with graphical reports

\- User and administrator login

\- Performance reports and system information

\- Email and SMS notification functionality (optional configuration)



\## Technologies Used



| Component | Technology |

|---|---|

| Backend | Python, Flask |

| Frontend | HTML, CSS, JavaScript, Bootstrap |

| Database / Cloud | Firebase |

| Data Visualization | CanvasJS |

| System Monitoring | Python system monitoring libraries |

| Notifications | Email and Twilio SMS integration |

| Version Control | Git and GitHub |



\## Project Structure



```text

cloud-performance-monitoring/

│

├── app.py

├── main.py

├── MailSent.py

├── requirements.txt

├── .gitignore

│

├── templates/

│   ├── index.html

│   ├── userlogin.html

│   ├── adminlogin.html

│   └── ...

│

├── static/

│   ├── assets/

│   │   ├── css/

│   │   ├── js/

│   │   ├── img/

│   │   └── vendor/

│   ├── forms/

│   └── uploads/

│

└── README.md

```



\## Installation and Setup



\### 1. Clone the repository



```bash

git clone https://github.com/bskiranmala/cloud-performance-monitoring.git

cd cloud-performance-monitoring

```



\### 2. Create a virtual environment



```bash

python -m venv venv

```



\### 3. Activate the virtual environment



Windows:



```bash

venv\\Scripts\\activate

```



\### 4. Install dependencies



```bash

pip install -r requirements.txt

```



\### 5. Configure the application



Configure the required Firebase credentials and other environment-specific settings locally.



Do not upload private keys, API tokens, passwords, or service account files to GitHub.



\### 6. Run the application



Check the application entry point and run the appropriate Python file. For example:



```bash

python app.py

```



Open the local URL displayed in your terminal in a web browser.



\## Project Objectives



\- Monitor the performance of connected computer systems.

\- Provide centralized access to system resource information.

\- Visualize performance metrics through graphical dashboards.

\- Help identify performance bottlenecks.

\- Support efficient system administration and analysis.



\## Future Enhancements



\- Advanced performance analytics

\- Customizable resource usage thresholds

\- Automated performance alerts

\- Historical performance comparison

\- Improved cloud integration

\- More detailed monitoring reports



\## Security



Private configuration files and credentials are intentionally excluded from this public repository. Configure your own credentials before running the application.



\## Author



\*\*Kiran Kumar B S\*\*



Computer Science and Engineering Graduate



GitHub: \[@bskiranmala](https://github.com/bskiranmala)



