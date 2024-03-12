from time import sleep
from pyautogui import write,press
from random import uniform

'''
cooldown is 4-5secs
fishy cooldown is <=30secs
'''

def t(msg:str, delay:float=0.5) -> None:
    write(msg)
    sleep(delay+uniform(0,0.5))
    press('enter')
    return

def test():
    sleep(5)
    write('test')
    sleep(1)
    press('enter')

def main(_type:str='train', start_fatigue:int=0, max_fatigue:int=500, end_fatigue:int=500) -> None:

    cooldown:int = 4

    if _type=='train':
        # how much fatigue we get to work with at the start
        fat_diff = max(max_fatigue, end_fatigue) - start_fatigue
        # convert to number of times we can call the command
        commands = fat_diff // 3 # takes 3 fatigue per command
        # take into account how much fatigue has gone down after completing
        # initial round of commands. Assume it takes 2secs to complete command
        # and fatigue goes down by 250/hr
        # Doesn't look like fatigue goes down when actively using commands
        extras = 0 # int(commands*5/24) # same as commands*3/3600*250
        total = commands+extras
        command_time_constant = 0.5 # average time variance dictated by random.uniform
        total_time_constant = command_time_constant + cooldown
        total_time = total*total_time_constant
        
        print(f'Commands to run: {commands}, Extras: {extras}, Total: {total}')
        sleep(10)
        
        for _ in range(total):
            print(f'''{_}/{total}, {round(_/total*100,1)}%
Estimated time remaining: {int((total_time-_*total_time_constant)//60)}m {round((total_time-_*total_time_constant)%60,1)}s''')
            t('t!tg train')
            sleep(cooldown+uniform(0,0.5))
            
    elif _type=='walk':
        # see explanations for calcs above ^
        fat_diff = max(max_fatigue, end_fatigue) - start_fatigue
        commands = fat_diff // 20 # 20 not 10 to account for feeding in between
        # Assume it takes 6secs per feeding command
        # Doesn't look like fatigue goes down when actively using commands
        extras = 0 # int(commands*5/12) # same as commands*6/3600*250
        total = commands+extras
        command_time_constant = 1.25 # average time variance dictated by random.uniform
        total_time_constant = command_time_constant + cooldown*3 # 3 commands per command cycle
        total_time = total*total_time_constant
        
        print(f'Commands to run: {commands}, Extras: {extras}, Total: {total}')
        sleep(10)
        
        t('t!tg feed')
        sleep(cooldown+uniform(0,0.5))
        for _ in range(total):
            print(f'''{_}/{total}, {round(_/total*100,1)}%
Estimated time remaining: {(total_time-_*total_time_constant)//60}m{(total_time-_*total_time_constant)%60}s''')
            # for every 2 walks, feed once
            for __ in range(2):
                t('t!tg walk')
                sleep(cooldown+uniform(0,0.5))
            t('t!tg feed')
            sleep(cooldown+uniform(0,0.5))
            
    else:
        print(f'Unknown command: {_type}')
    return

if __name__ == "__main__":
    arg0 = input('Input tg interaction (train/walk): ')
    print('\nType t!tg info to see your tg\'s related info including fatigue')
    arg1 = int(input('Input starting fatigue (0-497): '))
    arg2 = int(input('Input maximum fatigue (500-525): '))
    print('Will begin typing in 10secs. Tab to discord and click on the text box where commands will be pasted')
    main(_type=arg0, start_fatigue=arg1, max_fatigue=arg2)
            
