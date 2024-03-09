import requests
from os import getenv, environ
from dotenv import find_dotenv, load_dotenv, set_key

# Bearer

class HealthilyManager:
    base_url = "https://portal.your.md/v4"
    chat_url = base_url + "/chat"

    @staticmethod
    def auth_headers(auth, auth_prefix=""):
        return {
            "accept": "*/*",
            "content-type": "application/json",
            "Authorization": f"{auth_prefix}{auth}",
            "x-api-key": f"{getenv('HEALTHILY_KEY')}"
        }

    @staticmethod
    def session_headers():
        return HealthilyManager.auth_headers(getenv('HEALTHILY_ACCESS'), "Bearer ")

    @staticmethod
    def account_headers():
        return HealthilyManager.auth_headers(getenv('HEALTHILY_TOKEN'))

    def __init__(self, dotenv_file):
        self.dotenv_file = dotenv_file
        self.access_token = getenv("HEALTHILY_ACCESS")
        self.conversation_id = None

    def ensure_login(self):
        if self.access_token is None:
            print("No cached access token...")
            # can't login if there is already an active session
            if not self.try_login():
                self.logout()
                self.try_login()
        else:
            print("Cached access token...")

    def logout(self):
        response = requests.post(
            self.base_url + "/logout", 
            headers=HealthilyManager.account_headers()
        )
        
        assert response.status_code == 204

    def try_login(self):
        response = requests.post(
            self.base_url + "/login", 
            headers=HealthilyManager.account_headers(), 
            json={
                "delete_at": 1899250155,
                "email": "anon@anon.com",
                "email_verified": True,
                "id": "0",
                "name": "Anon"
            }
        )

        if response.status_code == 200:
            response_json = response.json()
            set_key(self.dotenv_file, "HEALTHILY_ACCESS", response_json["access_token"])
            environ["HEALTHILY_ACCESS"] = response_json["access_token"]
            print("Success: Logged in with new access token")
            return True
        else:
            print("Error: Active access token already exists")
            return False

    def chat(self):
        response = requests.post(
            self.chat_url, 
            headers=HealthilyManager.session_headers(), 
            json={}
        )

        chatting = True


        while (chatting):
            response_json = response.json()
            print(response.text)
            conversation = response_json["conversation"]
            question = response_json["question"]
            user = response_json["user"]
            # continue conversation
            self.conversation_id = conversation["id"]
        
            response = self.respond_question(question)
        
        
    def base_resp(self):
        return {
            "answer": {
                
            },
            "conversation": {
                "id": self.conversation_id
            }
        }

    def find_synthom(self, symptom):
        response = requests.post(
            'https://portal.your.md/v4/search/symptoms', 
            headers=HealthilyManager.session_headers(), 
            json={'text': symptom}
        )

    def respond_question(self, question):
        question_type = question["type"]
        # base payload
        payload = self.base_resp()
        # response matches question
        payload["answer"]["type"] = question_type
        # prompts as per
        for msg in question["messages"]:
            print(msg["value"] if "value" in msg else msg["text"])
    
        if question_type == "name":
            name = input()
            payload["answer"]["value"] = name
        elif question_type == "sex":
            print("choose betweeen MALE and FEMALE")
            gender = input()
            payload["answer"]["selection"] = [gender]
        elif question_type == "year_of_birth":
            # "MALE" or "FEMALE"
            yob = int(input())
            payload["answer"]["value"] = yob
        elif question_type == "initial_symptom":
            # "MALE" or "FEMALE"
            initial_symptoms_freetext = input()
            payload["answer"]["value"] = initial_symptoms_freetext
        elif question_type == "generic":
            included = []
            for choice in question['choices']:
                print(choice['label'])
                selection = input()
                if selection == 'YES':
                    included.append(str(choice['id']))
            payload["answer"]["input"] = {}
            payload["answer"]["input"]['include'] = included
            print(payload)

        # elif question_type == "autocomplete":
        #     pass
            
        else:
            raise NotImplementedError()

        response = requests.post(
            self.chat_url, 
            headers=HealthilyManager.session_headers(), 
            json=payload
        )

        print(response.status_code)
        print(response.text)
        print(response.json().keys())
        return response



if __name__ == "__main__":
    dotenv_file = find_dotenv()
    load_dotenv(dotenv_file)
    hm = HealthilyManager(dotenv_file)
    hm.ensure_login()
    hm.chat()
    