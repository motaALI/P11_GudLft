import json
from locust import HttpUser, task, between

class LocustTestServer(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        self.login()
    
    def login(self):
        self.client.post("/showSummary", data={"email": "example@example.com"})

    @task
    def index(self):
        self.client.get("/")
    
    @task
    def show_summary(self):
        self.client.post("/showSummary", data={"email": "example@example.com"})
    
    @task
    def book(self):
        self.client.get("/book/competition_name/club_name")
    
    @task
    def purchase_places(self):
        data = {
            "competition": "competition_name",
            "club": "club_name",
            "places": "5"
        }
        self.client.post("/purchasePlaces", data=data)
    
    @task
    def clubs_points(self):
        self.client.get("/clubsPoints")
    
    @task
    def logout(self):
        self.client.get("/logout")
