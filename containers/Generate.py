import json
import requests
from components import ScenarioComposer, Utilities
from containers import Result
from threading import Event
import time


class Generate:
    def __init__(self):
        self.result = []
        self.event = Event()

    @staticmethod
    def convert_schedule(dic, inc=2):
        with open("timeslots.json") as f:
            t = json.load(f)["timeslots"]

        final = {}
        for data in dic.values():
            add = []
            name = data[0]
            for i in range(1, inc):
                add.append(data[i])
            availability = []
            for week in data[inc]:
                lst = []
                for day in range(len(week)):
                    if week[day] == "Available":
                        if day == 0:
                            lst.append("Monday")
                        elif day == 1:
                            lst.append("Tuesday")
                        elif day == 2:
                            lst.append("Wednesday")
                        elif day == 3:
                            lst.append("Thursday")
                        elif day == 4:
                            lst.append("Friday")
                availability.append(lst)

            schedule = dict(zip(t, availability))
            final[name] = [*add, schedule]
        return final

    @staticmethod
    def convert_subject(dic):
        final = {}
        for data in dic.values():
            name = data[0]
            instructors = [value for value in json.loads(data[1]).values()]
            hours = data[2]
            code = data[3]
            _type = data[5]
            final[name] = [hours, code, _type, instructors]
        return final

    @staticmethod
    def check(out):
        if len(out) != 5:
            # print("length of the dict is not 5.")
            return False

        out_list = list(map(tuple, out.values()))

        if not all(len(t) == 7 for t in out_list):
            # print("Not all lists have a length of 7.")
            return False

        if len(out_list) != len(set(out_list)):
            # print("Repeating lists detected.")
            return False

        if any(len(set(t)) == 1 for t in out_list):
            # print("A list with all values the same was found.")
            return False

        return True

    def generate_timetable(self, key, text, retry=10):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={key}"
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": text}]}]}
        for _ in range(retry):
            print("generating...")
            if self.event.is_set():
                break
            try:
                response = requests.post(url, headers=headers, data=json.dumps(data))
                out = json.loads(
                    response.json()["candidates"][0]["content"]["parts"][0]["text"]
                )
                if not self.check(out):
                    continue
                self.result.append(out)
                self.event.set()
            except Exception:
                continue

    def get_data(self, text):
        workers = []
        with open("keys.json") as f:
            keys = json.load(f)["keys"]
        self.event.clear()
        for key in keys:
            worker = Utilities.Worker(self.generate_timetable, key, text)
            worker.start()
            workers.append(worker)
            time.sleep(0.1)

        for worker in workers:
            worker.wait()

        if self.result:
            return self.result[0]

        return False

    def generate(self):
        data = ScenarioComposer.ScenarioComposer().getScenarioData()
        final_data = {
            "instructors": self.convert_schedule(data["instructors"]),
            "subjects": self.convert_subject(data["subjects"]),
            "sections": self.convert_schedule(data["sections"], 1),
        }
        with open("training_data.txt") as f:
            add_data = f.read()
        prompt = (
            f"generate a timetable based on the given data\n{final_data}\n{add_data}"
        )
        self.generating = Utilities.Generating()
        worker = Utilities.Worker(self.get_data, prompt)
        worker.finished.connect(self.handle_result)
        worker.start()
        self.generating.show()

    def handle_result(self, result):
        self.generating.close()
        if result:
            Result.Result().fillForm(result)
        else:
            Utilities.show_error("Timetable generation unsuccessful")
