# Power Consumption Estimation Tool Documentation

This program is designed to estimate the power consumption of a running application on a computer by utilizing the Thermal Design Power (TDP) values of the CPU, GPU and memory.

## Rationale behind using TDP values

TDP is a measure of the maximum amount of power that a component, such as a CPU or GPU, can dissipate when running at its base frequency under normal conditions. TDP values are typically provided by the manufacturer and are useful for estimating the amount of power a component will consume when running at its base frequency. 

By utilizing the TDP values of the CPU, GPU, and memory, this program estimates the power consumption of a running application. However, it is important to note that this estimation is not exact and may not account for all factors that contribute to power consumption, such as variable clock speeds, fluctuations in workload, or other factors.

## Difficulties in getting exact values

Obtaining exact power consumption values can be challenging due to the many factors that contribute to power consumption. These factors can include the workload being performed, the clock speed of the CPU and GPU, the efficiency of the power supply, and the temperature of the components. Additionally, many components consume power in a non-linear way, making it difficult to accurately estimate power consumption based on TDP values alone.

## Requirements
- Python 3.x installed on your system.
- The following Python packages installed:
    - psutil
    - GPUtil
    - cpuinfo
    - BeautifulSoup
    - requests

## How to use the program

1. Open a Python environment such as IDLE or a command prompt.
2. Copy and paste the entire code of the program into the Python environment.
3. Install the required Python packages if you haven't already by typing the following commands in the Python environment and pressing Enter:
    ```
    !pip install psutil
    !pip install GPUtil
    !pip install py-cpuinfo
    !pip install beautifulsoup4
    !pip install requests
    ```
4. Run the program by calling the `main()` function. To do this, type `main()` in the Python environment and press Enter.
5. When prompted, enter the name of the process you want to measure the power consumption for. This could be any process that is currently running on your computer.
6. The program will search for the TDP values of your CPU, GPU and memory and estimate the power consumption based on these values.
7. The estimated power consumption values for the CPU, memory and GPU will be displayed.
8. The program will continue to display power consumption values until stopped manually.

## Notes
- If the TDP values for your CPU or GPU cannot be found, the program will display a message stating that it could not find the TDP value for the corresponding component.
- If you do not have a dedicated GPU, the program will display a message stating that it could not detect a GPU.
- The program estimates power consumption based on the TDP values of the components and may not provide exact values. It is important to consider the limitations and potential inaccuracies of this tool when interpreting the results.
- Be aware that excessive or prolonged use of this tool may lead to increased power consumption, so use with caution.
