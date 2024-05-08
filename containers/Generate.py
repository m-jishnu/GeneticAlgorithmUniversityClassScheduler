import json
from components import ScenarioComposer, Utilities
from containers import Result
import aiohttp
import asyncio


class Generate:
    def __init__(self):
        self.result = []
        self.event = False

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
            return False

        out_list = list(map(tuple, out.values()))

        if not all(len(t) == 7 for t in out_list):
            return False

        # first_items = [lst[0] for lst in out_list]
        # if any(first_items.count(item) > 2 for item in first_items):
        #     return False

        for lst in out_list:
            if any(lst.count(item) > 2 for item in lst):
                return False

        return True

    async def generate_timetable(self, session, key, text, retry=10):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={key}"
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": text}]}]}
        for _ in range(retry):
            if self.event:
                break
            try:
                async with session.post(
                    url, headers=headers, data=json.dumps(data)
                ) as response:
                    response_json = await response.json()
                    out = json.loads(
                        response_json["candidates"][0]["content"]["parts"][0]["text"]
                    )
                    print(out)
                    if not self.check(out):
                        continue
                    self.result.append(out)
                    self.event.set()
            except Exception:
                continue

    async def get_data(self, text):
        tasks = []
        with open("keys.json") as f:
            keys = json.load(f)["keys"]
        self.event = False
        async with aiohttp.ClientSession() as session:
            for key in keys:
                task = asyncio.create_task(self.generate_timetable(session, key, text))
                tasks.append(task)
                await asyncio.sleep(0.1)
            await asyncio.gather(*tasks)

        if self.result:
            return self.result[0]

        return False

    def generate(self):
        data = ScenarioComposer.ScenarioComposer().getScenarioData()
        final_data = {
            "instructors": self.convert_schedule(data["instructors"]),
            "subjects": self.convert_subject(data["subjects"]),
        }
        with open("training_data.txt") as f:
            add_data = f.read()
        prompt = (
            f"generate a timetable based on the given data\n{final_data}\n{add_data}"
        )
        self.generating = Utilities.Generating()
        worker = Utilities.Worker(lambda: asyncio.run(self.get_data(prompt)))
        worker.finished.connect(self.handle_result)
        worker.start()
        self.generating.show()

    def handle_result(self, result):
        self.generating.close()
        if result:
            Result.Result().fillForm(result)
        else:
            Utilities.show_error("Timetable generation unsuccessful")
