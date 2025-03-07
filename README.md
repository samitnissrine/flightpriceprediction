# Flight Price Prediction

This project focuses on predicting flight prices using machine learning models, which are integrated into a Flask web application using distinct pipelines for training and prediction. The project began with sourcing data from Kayak and supplementing it through web scraping using Beautiful Soup and Selenium.

To streamline model development and deployment, we adopted modular coding practices. This allowed us to create separate pipelines for training machine learning models and predicting flight prices. These pipelines were then seamlessly integrated into a Flask web application, providing an intuitive interface for users to interact with and obtain predictions.

In parallel, to enhance model accuracy and keep predictions up-to-date with new data, we implemented some basic MLOps principles. This involved the introduction of continuous training workflows orchestrated by Airflow. Airflow automates tasks such as data extraction, preprocessing, model training, evaluation, and deployment in a scheduled and reproducible manner. Concurrently, DVC was employed for efficient data and model versioning, ensuring that each iteration of the model could be tracked and reproduced as necessary. MLflow was utilized to log experiments and metrics, providing insights into model performance over time.

The entire project is containerized using Docker, facilitating easy deployment and scalability of both the Flask application and the MLOps workflows.



## Tools Used

- Machine Learning Models: scikit-learn
- code version control: git
- Vscode
- Web Scraping: Beautiful Soup, Selenium
- Flask: Web framework for developing the application
- Airflow: Orchestration of continuous training pipelines
- DVC (Data Version Control): Management of data and model versioning
- MLflow: Tracking experiments and metrics
- Docker: Containerization for deployment and scalability
