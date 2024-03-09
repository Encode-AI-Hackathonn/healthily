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
    def search_headers():
        return {
            "accept": "application/json",
            "authorization": f"Bearer {getenv('HEALTHILY_ACCESS')}",
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
            # print(response.text)
            try:
                conversation = response_json["conversation"]
                question = response_json["question"]
                user = response_json["user"]
                # continue conversation
                self.conversation_id = conversation["id"]
                if 'report' in response_json.keys():
                    self.cause = response_json['report']['summary']["articles_v3"][0]['name']
                    self.cause_prob =response_json['report']['summary']["articles_v3"][0]['condition']['probalility']
                    print('Possible Cause:', self.cause)
                    print('Probability', self.cause_prob)
                    chatting = False

                response = self.respond_question(question)
            
            except:
                'An Error Occurred'

            
        
        
    def base_resp(self):
        return {
            "answer": {
                
            },
            "conversation": {
                "id": self.conversation_id
            }
        }

    def find_symptom(self, symptom):
        response = requests.get(
            'https://portal.your.md/v4/search/symptoms'+'?text='+symptom, 
            headers=HealthilyManager.search_headers()
        )
        for s in response.json()['autocomplete']:
            selected = []
            print(s['user_facing_name'])
            selection = input()
            if selection == 'YES':
                selected.append(s['id'])
        if len(selected) <= 3:
            return selected
        else: print('Too many symptoms selected, max is 3')


    def respond_question(self, question):
        question_type = question["type"]
        # base payload
        payload = self.base_resp()
        # response matches question
        payload["answer"]["type"] = question_type

        def selection(label):
            selected = []
            for choice in question['choices']:
                print(choice[label])
                selection = input()
                if selection == 'YES':
                    selected.append(choice['id'])
            payload['answer']['selection'] = selected
            return payload

        # prompts as per
        for msg in question["messages"]:
            print(msg["value"] if "value" in msg else msg["text"])
    
        if question_type == "name":
            name = input()
            payload["answer"]["value"] = name.upper()
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
                if selection.upper() == 'YES':
                    included.append(str(choice['id']))
                    if question['multiple'] == 'false': break
            payload["answer"]["input"] = {}
            payload["answer"]["input"]['include'] = included
        
        elif question_type == "health_background": payload = selection('long_name')
        elif question_type in ["factor", "symptom", 'symptoms']: payload = selection('text')

        elif question_type == "autocomplete":
            symptom = input()
            payload = self.find_symptom(symptom)
            
        else:
            raise NotImplementedError()

        response = requests.post(
            self.chat_url, 
            headers=HealthilyManager.session_headers(), 
            json=payload
        )

        # print(response.status_code)
        # print(response.text)
        # print(response.json().keys())
        return response



    def get_NHS_header():
        return {
        'Content-Type': 'application/json',
        "subscription-key": f"{getenv('NHS_PK')}"
    }

    def search_service(self, loc_or_code):
        location = requests.post(
            'https://api.nhs.uk/service-search/search-postcode-or-place?api-version=1&search='+loc_or_code,
            headers=get_NHS_header())
        
        cause = requests.get(
            'https://api.nhs.uk/service-search?api-version=2&search='+self.cause,
            headers=get_NHS_header())
        
        print('Location',location)
        print('Cause',cause)





if __name__ == "__main__":
    dotenv_file = find_dotenv()
    load_dotenv(dotenv_file)
    hm = HealthilyManager(dotenv_file)
    hm.ensure_login()
    hm.chat()
    hm.search_service('Birmingham')
    