# Alemeno-task

## 1. Post Request to register a new Customer
![register](https://github.com/Grg-Sid/Alemeno-task/assets/106266279/8f7d62c2-32a8-420d-b79c-80c962787c96)

## 2. Post Request to check eligiblity for Loan
![check](https://github.com/Grg-Sid/Alemeno-task/assets/106266279/bea98119-d7c0-46b6-bc4b-2fc7b226d919)

## 3. Post Request to create Loan
![create](https://github.com/Grg-Sid/Alemeno-task/assets/106266279/6a82e4bc-4471-4771-8015-d93224f581ae)

## 4. Get Request to view a particular Loan Details
![loan-det](https://github.com/Grg-Sid/Alemeno-task/assets/106266279/fde700c3-64af-4957-a82d-f3b9c4ff1b0c)

## 5. Get Requestt to view all the Loans of a given Customer
![loans](https://github.com/Grg-Sid/Alemeno-task/assets/106266279/806c8cd3-d1cb-4d36-9220-9d756019cd81)

# SETUP

1. Clone the repository:

```CMD
git clone https://github.com/Grg-Sid/Alemeno-task.git
```

2. Install, Create and activate a virtual environment:

```CMD
python3 -m venv .venv
```

Activate the virtual environment

```CMD
source .venv/bin/activate
```

3. Install the dependencies:

```CMD
pip install -r requirements.txt
```

5.Run the migrate command

```CMD
python manage.py migrate
```

6. Run the backend server on localhost:

```CMD
python manage.py runserver
```

You can access the endpoints from your web browser following this url

```url
http://127.0.0.1:8000
```
