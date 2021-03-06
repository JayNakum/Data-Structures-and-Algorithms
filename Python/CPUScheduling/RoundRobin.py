# this method gets the Arival Time and Burst Time from user
def getDetails() -> None:
    numberOfProcesses = int(input('Enter number of processes: '))
    for i in range(0, numberOfProcesses):
        # reading data
        arrivalTime = int(input('Enter arrival time for process[%d] : ' %(i + 1)))
        burstTime = int(input('Enter burst time for process[%d] : ' %(i + 1)))
                
        processes.append({'Process ID': i, 'Arrival Time': arrivalTime, 'Burst Time': burstTime}) # putting data in the processes array each process is treated as a dictionary
        # output.append({'Process ID': i, 'Arrival Time': arrivalTime, 'Burst Time': burstTime,'Completion Time':0, 'Turn Around Time': 0, 'Waiting Time': 0})
        
        # sorting by its arrival time
        processes.sort(key=lambda process: process['Arrival Time'])
        # output.sort(key=lambda process: process['Arrival Time'])

# Round Robin
class RoundRobin:
    def __init__(self, processes) -> None:
        self.processes = processes
        self.processCount = len(self.processes)

    # This method does the execution of the the process and generates a Gantt Chart
    def ganttChart(self) -> None: # and returns a ganttChart
        isDone = False
        ganttChart = [] # the main list which will contain the ganttChart 
        time = 0 # initial startTime
        i = 0 # starting with process[0]

        while not isDone:
            if(i >= self.processCount):
                i = 0

            if(self.processes[(self.processCount-1)]['Burst Time'] == 0): # if the remaining burst time of last process is zero
                isDone = True # then gantt chart is formed
            
            # remainingBurstTime is the time left to execute
            remainingBurstTime = self.processes[i]['Burst Time'] # initially the burst time will be the remainingBurstTime
            
            if(remainingBurstTime == 0): # if the remaining time is zero
                i += 1 # then we skip to the next process
                continue
            
            # Check if there is an empty state
            while(self.processes[i]['Arrival Time'] > time):
                time += 1 # keep CPU empty
            
            ganttStart = time # note the start time before execution begins


            # performing the execution of process
            for _ in range(0, QUANTUM): # executing the process for given Time (QUANTUM)
                remainingBurstTime -= 1
                time = time + 1
                if(remainingBurstTime == 0): # if remainingBurstTime is 0
                    break # then the process is fully executed
            
            ganttStop = time # note the stop time after finishing the execution
            
            # add the 'Process ID', 'Start Time' and 'Stop Time' in ganttChart
            ganttChart.append({'Process ID': self.processes[i]['Process ID'], 'Start Time': ganttStart, 'Exit Time': ganttStop})
            # updating the process 'Burst Time' to remainingBurstTime
            self.processes[i]['Burst Time'] = remainingBurstTime

            i += 1 # next process
        print(ganttChart)
        # return ganttChart # returning the final ganttChart list
        
    # this method calculates the completionTime, turnAroundTime, waitingTime and responseTime of each process
    def calculateTimes(self, ganttChart) -> None:
        for process in self.processes:
            for gantt in ganttChart: # it reads the ganttChart
                if(process['Process ID'] == gantt['Process ID']): # and updates the values everytime both the 'Process Id' matches
                    process['Completion Time'] = gantt['Exit Time']
                    
            # Turn Around Time = Completion Time - Arrival Time
            process['Turn Around Time'] = process['Completion Time'] - process['Arrival Time']
            # Waiting Time = Turn Around Time - Burst Time
            process['Waiting Time'] = process['Turn Around Time'] - process['Burst Time']
            # In Round Robin, Response Time = Waiting Time - Arrival Time 
            process['Response Time'] = process['Waiting Time'] - process['Arrival Time']            

    # this method calculates the average of all waitingTimes
    def calculateAverageWaitingTime(self) -> float:
        sum = 0
        for process in self.processes:
            # calculating the sum
            sum = sum + process['Waiting Time']
        # dividing by total processes
        return (sum / self.processCount) # returning the average

    # this method calculates the average of all turnAroundTimes
    def calculateAverageTurnAroundTime(self) -> float:
        sum = 0
        for process in self.processes:
            # calculating the sum
            sum = sum + process['Turn Around Time']
        # dividing by total processes
        return (sum / self.processCount) # returning the average

# this method formats the gantt chart properly
def printGanttChart(list) -> None:
    ganttChartOutput = []
    processID = ''
    startTime = ''
    stopTime = ''
    for process in list:
        processID = str(process['Process ID'])
        startTime = str(process['Start Time'])
        stopTime = str(process['Exit Time'])
        ganttChartOutput.append((processID, startTime, stopTime))
    print(ganttChartOutput)

# this method formats the output properly
def printOutput(list) -> None:
    processID = ''
    arrivalTime = ''
    burstTime = ''
    completionTime = ''
    turnAroundTime = ''
    waitingTime = ''

    print('Process ID | Arrival Time | Burst Time | Completion Time | Turn Around Time | Waiting Time')
    for process in list:
        processID = str(process['Process ID'])
        arrivalTime = str(process['Arrival Time'])
        burstTime = str(process['Burst Time'])
        completionTime = str(process['Completion Time'])
        turnAroundTime = str(process['Turn Around Time'])
        waitingTime = str(process['Waiting Time'])
        
        print(processID+'\t\t'+arrivalTime+'\t\t'+burstTime+'\t\t'+completionTime+'\t\t'+turnAroundTime+'\t\t'+waitingTime)

# DRIVER CODE
if __name__ == "__main__":
    # Running Time Complexity = O(n * QUANTUM)

    QUANTUM = 3  # is the defined time for which any process will be executed
    processes = []  # is the process array in which all processes are stored

    getDetails() # reading the details from user
    
    print(processes)

    algorithm = RoundRobin(processes)

    print('\nGantt Chart: ')
    ganttChart = algorithm.ganttChart() # generate ganttChart
    print(ganttChart)
    printGanttChart(ganttChart) # print ganttChart

    # Calculate 'Completion Time', 'Turn Around Time' and 'Waiting Time' of each process
    algorithm.calculateTimes(ganttChart)
    
    print('\n\nOutput: ')
    print(algorithm.processes)
    printOutput(algorithm.processes) # print details of each process

    # Calculate the average of waiting times
    averageWaitingTime = algorithm.calculateAverageWaitingTime()
    print('\nAverage Waiting Time: ')
    print(averageWaitingTime) # and print averageWaitingTime

    # Calculate the average of turn around times
    averageTurnAroundTime = algorithm.calculateAverageTurnAroundTime()
    print('\nAverage Turn Around Time: ')
    print(averageTurnAroundTime) # and print averageTurnAroundTime