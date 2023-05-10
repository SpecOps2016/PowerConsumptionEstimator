import time
import psutil
import GPUtil
import psutil
from bs4 import BeautifulSoup
import requests
import cpuinfo
import time
import re

def get_text_before_substring(text):
    pattern = re.compile(r"(.+)\s+\d+-Core")
    match = pattern.search(text)
    if match:
        return match.group(1).strip()  # Return text before the "<integer>-Core"
    return None

def get_text_after_substring_2(text):
    pattern = re.compile(r"(AMD|NVIDIA)\s+(.*)")
    match = pattern.search(text)
    if match:
        return match.group(2).strip()  # Return text after "AMD" or "NVIDIA"
    return None


def get_cpu_tdp(cpu_name):
    url = "https://www.techpowerup.com/cpu-specs/?ajaxsrch=" + cpu_name
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find("table", {"class": "processors"})

        if table:
           for a_tag in table.find_all('a'):
                for a_tag in table.find_all('a'):
                # check if the text of the <a> tag matches the CPU name
                    if a_tag.get_text().lower() in cpu_name.lower():
                        # get the TDP from the seventh subsequent <td> tag
                        tdp_tag = a_tag.find_next('td')
                        for i in range(6):
                            tdp_tag = tdp_tag.find_next('td')
                        return tdp_tag.get_text()

    return None


def get_gpu_tdp(gpu_name):
    search_url = "https://www.techpowerup.com/gpu-specs/"
    response = requests.get(search_url, params={"name": gpu_name})

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)
        search_results = soup.find_all("a")

        if search_results:
            for result in search_results:
                if gpu_name.lower() in result.get_text().lower():
                    print(result)
                    gpu_url = "https://www.techpowerup.com" + result["href"]
                    gpu_response = requests.get(gpu_url)


                    if gpu_response.status_code == 200:
                        gpu_soup = BeautifulSoup(gpu_response.text, 'html.parser')
                        tdp_tag = gpu_soup.find('dt', string='TDP')
                        if tdp_tag:
                            tdp_value = tdp_tag.find_next('dd').text.strip()
                            return tdp_value

    return None

def get_cpu_model():
    print(cpuinfo.get_cpu_info()['brand_raw'])
    return cpuinfo.get_cpu_info()['brand_raw']



def get_gpu_model():
    gpus = GPUtil.getGPUs()
    if gpus:
        return gpus[0].name
    return None


def get_memory_max_power(memory_amount):
    max_power = 3 * memory_amount/8
    return max_power


def get_process_pid(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return proc.info['pid']
    return None

def measure_usage(pid, cpu_max_power, memory_max_power, gpu_max_power):
    process = psutil.Process(pid)
    while True:
        cpu_usage = process.cpu_percent(interval=1) / 100
        memory_usage = process.memory_info().rss / psutil.virtual_memory().total
        cpu_power = cpu_max_power * cpu_usage
        memory_power = memory_max_power * memory_usage

        gpus = GPUtil.getGPUs()
        gpu_power = 0
        for gpu in gpus:
            gpu_load = gpu.load
            gpu_power += gpu_max_power * gpu_load
        
        print(f'Estimated CPU Power Consumption: {cpu_power}W')
        print(f'Estimated Memory Power Consumption: {memory_power}W')
        print(f'Estimated GPU Power Consumption: {gpu_power}W')
        print(f'Total Estimated Power Consumption: {cpu_power + memory_power + gpu_power}W')

        time.sleep(5)

def main():
    process_name = input("Enter the process name: ")  # Prompt the user to enter the process name
    pid = get_process_pid(process_name)
    if pid is not None:
        cpu_max_power = None
        memory_max_power = None
        gpu_max_power = None
        cpu_model = get_cpu_model()
        print(f"Your CPU model is: {cpu_model}")
        tdp = get_cpu_tdp(get_text_before_substring(cpu_model))
        if tdp:
            cpu_max_power = tdp  
        else:
            print(f"Could not find the TDP of your CPU.")
        gpu_model = get_gpu_model()
        if gpu_model:
            print(f"Your GPU model is: {gpu_model}")
            print(get_text_after_substring_2(gpu_model))
            gpu_max_power = get_gpu_tdp(get_text_after_substring_2(gpu_model))
            if gpu_max_power:
                print(f"The max power of your GPU is: {gpu_max_power}")
            else:
                print(f"Could not find the max power of your GPU.")
        else:
            print("GPU not detected.")
        memory_type = " "
    
        while True:
            memory_type = input("Please enter how much memory you have: ")
            if memory_type.isdigit():
                if int(memory_type) % 8 == 0:
                    break
            else:
                print("Please enter memory in multiples of 8\n")
        memory_max_power = get_memory_max_power(int(memory_type))
        if memory_max_power:
            print(f"The max power of memory is: {memory_max_power}")
        else:
            print(f"Could not find the max power of memory.")
        measure_usage(pid, float(cpu_max_power.split("W")[0].strip()), float(memory_max_power), float(gpu_max_power.split("W")[0].strip()))
    else:
        print(f'No process found with name {process_name}')

if __name__ == "__main__":
    main()
