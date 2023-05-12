# EM_Book_Recommender

bert model google drive link: https://drive.google.com/drive/folders/1aTFCM9tRdmGPq1hxpJYTiq4iIabXQllW?usp=sharing \
hosted website url: http://66.42.113.98/ 

## Environment Configuration

If you want to run the website locally, here are some instructions.

### Backend

We are using python3.10 and all the required packages are included in requirement.txt. \
To start the backend server, navigate to the backend folder and use this following command:

``uvicorn api_server:app --reload``

The server will be running on http://127.0.0.1:8000/ by default.

### Frontend

We are using node version 18.16.0 for our react project. Ensure you have npm and react on your machine to install all the required packages. \
To start the frontend server, use the corresponding npm starting code in package.json or simply use: \

``react-scripts start``

### Database

We have already open our database to all IPs with read only access. The MongoDB link is included in the corresponding python files. \
If you have any connection issues or other issues about setup when running this project locally, please contact Peter:shuhaok2@illinois.edu