# Social Media API

Description

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies into a virtual environment.

```bash
pip install -r requirements.txt
```

PostgreSQL server and pgAdmin 4 can be to be downloaded [here](https://pip.pypa.io/en/stable/), which will be needed to manage database objects. A [Heroku](https://www.heroku.com/) account will be required to deploy the application from the CI/CD pipeline. [Postman](https://www.postman.com/) or any similiar API client is recommended to test HTTP requests. 

## Usage

Create a `.env` file in project directory to provide the following credentials and variables. The file path will need to be set in `config.py`. Also add the project directory path to each file via 
``` sys.path.append('path/to/directory')```. 

```python
  database_hostname: str
  database_port: str
  database_password: str
  database_name: str
  database_username: str
  secret_key: str
  algorithm: str
  access_token_expire_minutes: int
```

For the CI/CD pipeline to operate, two GitHub environments will needed to be made: testing and production. Refer to the `build-deploy.yml` file to determine which secrets will need to be added for each environment via GitHub Actions. 

Create two PostgreSQL databases in pgAdmin 4, one for testing and the other for main production. In the `database.py` file, select which `SQLALCHEMY_DATABASE_URL` will passed into the SQLAlchemy engine object. 

Once the above is complete, run the following in terminal under the app directory to start the server.

```bash
uvicorn main:app --reload
```

## Tests

Run the following command in terminal to test the API is functioning properly.
```bash
pytest -v -s 
```

## Acknowledgements
This API was made possible by the Python API Development course taught from [Sanjeev Thiyagarajan](https://www.youtube.com/watch?v=0sOvCWFmrtA).  

## License
This repository is released under the [MIT](https://opensource.org/licenses/MIT) License.
