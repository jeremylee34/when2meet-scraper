#! /usr/bin/env python3

# import subprocess


# url="https://www.when2meet.com/?16376106-q61We&fbclid=IwAR1lv2GJ-dipIfHLjb4dnQ1UHwPbDoJ-3CHskcjMVbA_hYJPLrk60Bg8yow"

# # subprocess.run(["curl", url, ">", "curl.txt"])
# subprocess.run(f"curl {url} > curl.txt", shell=True, check=True)

import pycurl
from io import BytesIO
import re

def curl_to_txt(url):
    b_obj = BytesIO()
    crl = pycurl.Curl()
    crl.setopt(crl.URL, url)
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.perform()
    crl.close()
    get_body = b_obj.getvalue().decode('utf8')
    f = open("curl.txt", "w")
    f.write(get_body)

    return get_body.split('\n')

def p_id_to_person(p_id, names):
    return list(names.keys())[list(names.values()).index(p_id)]

def available_times(curl, names):
    times = {}
    for line in curl:
        if re.match(r"AvailableAtSlot.*.push.*", line):
            pair = re.findall(r'\d+', line)
            time = int(pair[0])
            person = int(pair[1])
            person = p_id_to_person(person, names)
            if time not in times:
                times.update({
                    time : {
                        'time_id' : '',
                        'time': '',
                        'date': '',
                        'day': '',
                        'people' : [person]
                    }
                })
            else:
                times[time]["people"].append(person)

    for line in curl:
        if re.match(r"^TimeOfSlot.*;$", line):
            pair = re.findall(r'\d+', line)
            no = int(pair[0])
            time_id = int(pair[1])
            if no in times:
                times[no]['time_id'] = time_id
                time_entry = times[no]
                times.pop(no)
                times.update({
                    time_id: time_entry
                })


    # for entry in sorted(times):
    #     print(entry, times[entry])
    return times
    
def find_people(curl):
    for line in curl:
        if re.match(r"PeopleNames.*;PeopleIDs", line):
            name_string = line
    name_string = name_string.split(';')
    name_dict = {}
    for name in name_string:
        if re.match("AvailableAtSlot", name):
            break
        nums = re.findall(r'\d+', name)

        # name
        if len(nums) == 1:
            person = name.split(' ')[2][1:-1]
            name_dict.update({person:0})
            last_name = person

        # person_id
        elif len(nums) == 2:
            person_id = int(name.split(' ')[2])
            name_dict[last_name] = person_id

    # print(name_dict)

    return name_dict

def populate_times(curl, times):
    # for line in curl:
    #     if re.match()
    print("hi")

    for line in curl:
        # if re.search(r"AEST", line):
        #     if re.search(r"<div style=", line):
        #         print('long')
        #     else:
        #         print("normal")
        #         time_id = int(line.split('"')[5])
        #         date_time = line.split('"')[7]
        #         print(time_id, date_time)

        time_regex = re.compile(r'(ShowSlot.*,)(".*\d\d\d\d).*(\d\d:\d\d:\d\d) (..) (AEST)')
        time_info = time_regex.search(line)
   

        if time_info:
            time_info = list(time_info.groups())
            time_info[0] = int(time_info[0].split('(')[-1][0:-1])
            time_id = time_info[0]
            date = time_info[1][1:].split(' ')
            day = date[0]
            date = (' ').join(date[1:])
            time = time_info[2]
            am_pm = time_info[3]
            # print(time_id, date, time, am_pm)


            if time_info[0] in times:
                # print(time_info)
                times[time_id]['time'] = time
                times[time_id]['date'] = date
                times[time_id]['day'] = day
                # times[time_id]['']


    return times


if __name__ == "__main__":
    url="https://www.when2meet.com/?16376106-q61We&fbclid=IwAR1lv2GJ-dipIfHLjb4dnQ1UHwPbDoJ-3CHskcjMVbA_hYJPLrk60Bg8yow"

    get_body = curl_to_txt(url)
    name_dict = find_people(get_body)
    times = available_times(get_body, name_dict)
    print(name_dict)
    times = populate_times(get_body, times)
    for time in times:
        print(time, times[time])