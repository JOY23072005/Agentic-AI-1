from memory import memory

def add(a,b) -> float:
    return a+b
def multiply(a,b) -> float:
    return a*b
def divide(a,b) -> float:
    return a/b
def current_time():
    from datetime import datetime
    return datetime.now().strftime('%d-%m-%Y %H:%M:%S')
def remember(key,value):
    memory[key]=value
    return "remembered"
def recall(key):
    try:
        return memory[key]
    except:
        return f"available keys : {memory.keys()}"

tool_map = {
    'add':add,
    'multiply':multiply,
    'divide':divide,
    'current_time':current_time,
    'remember':remember,
    'recall':recall
}
