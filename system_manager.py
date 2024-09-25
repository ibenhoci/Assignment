import json

def load_environment(fn: str):
    servers = []
    with open(fn, "r") as fl:
        content = json.load(fl)
    for server in content["servers"]:
        servers.append({
            "name": list(server.keys())[0],
            "cpu": server[list(server.keys())[0]]["cpu"],
            "memory": server[list(server.keys())[0]]["memory"]
        })
    return servers


class InvalidValue(Exception):
    """Exception for invalid value input"""
    pass



def convert_memory(mem_str: str) -> int:
    """This function converts our memory from G to M"""
    if mem_str.endswith('G'):
        return int(mem_str[:-1]) * 1024
    elif mem_str.endswith('M'):
        return int(mem_str[:-1])
    else:
        raise ValueError(f"Invalid memory: {mem_str}")



# This is the adding function
def add_function(server_list, tasks):
    cpu_value = int(input ('Cpu value: '))
    if cpu_value <= 0:
        raise InvalidValue("Cpu value cannot be negative!")
    
    mem_value = input('Memory value in MB or G: ')
    memory_value = convert_memory(mem_value)
    
    timespan = int(input('Timespan value: '))
    if timespan <= 0:
        raise InvalidValue("Timespan value cannot be negative!")

    for server in server_list:
        server_name = server['name']
        
        tasks_on_server = tasks.get(server_name, [])

        used_cpu = sum(task['cpu'] for task in tasks_on_server)
        used_memory = sum(task['memory'] for task in tasks_on_server)

        available_memory = convert_memory(server['memory']) - used_memory
        available_cpu = server['cpu'] - used_cpu

        if available_cpu >= cpu_value and available_memory >= memory_value:
            added_task = {
                'cpu': cpu_value,
                'memory': memory_value,
                'timespan': timespan,
                'remaining_time': timespan
            }
            tasks_on_server.append(added_task)
            tasks[server_name] = tasks_on_server

            print(f"Task assigned to {server_name} with {cpu_value} CPU and {memory_value}M")
            return 
        
    raise InvalidValue ("No server available has enough resources for this task")

def status_function(server_list, tasks):
    print('Running!')

def run():
    command = ""
    cmds = ['exit', 'add', 'status']
    print(f"Available commands are: {cmds}")

    server_list = load_environment('environment_3.json')
    tasks = {}

    while command != "exit":
        command = input("> ")
        
        
        if command == 'add':
            try:
                add_function(server_list, tasks)
            except InvalidValue as e:
                print(f'Caught an error: {e}') 
            except ValueError as e:
                print(f'Caught an error: {e}')
        
        elif command == 'status':
            print('Not implemented for now')
        
        elif command == 'exit':
            print('Exit...')
        else:
            print('Invalid cmd, available cmds are :{cmds}')
    return


if __name__ == '__main__':
    run()