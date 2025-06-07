# Place for the brainrot

class HP:

    bars = 20
    remaining_health_symbol = "█"
    lost_health_symbol = "░"

    color_green = "\033[92m"
    color_yellow = "\33[33m"
    color_red = "\033[91m"
    color_default = "\033[0m"


    def __init__(self, max_health, current_health, name, health_color):
        self.max_health = max_health
        self.current_health = current_health
        self.remaining_health_bars = round(self.current_health / self.max_health * HP.bars)
        self.lost_health_bars = HP.bars - self.remaining_health_bars
        self.health_color = health_color
        self.name = name

    def update(self, current):
        self.current_health = current
        self.remaining_health_bars = round(self.current_health / self.max_health * HP.bars)
        self.lost_health_bars = HP.bars - self.remaining_health_bars
    
    def check(self, move):
        move_cost_dict = {"get_encrypted_flag": 50, "perform_deadcoin" : 0, "call_the_signer" : 20, "level_restart" : 0, "level_quit" : 0}
        if (self.current_health - move_cost_dict[move]) <= 0 :
            return False
        return True
    
    def __repr__(self):
        return f"Your HP : ❤ {'\33[0;101m'}{self.current_health}{'\33[0m'}"f"{self.health_color}{self.remaining_health_bars * self.remaining_health_symbol}"f"{self.lost_health_bars * self.lost_health_symbol}{HP.color_default}"
    

def title_drop():
        from time import sleep
        title_drop = f'''{"\33[1;91m"}
██╗   ██╗██╗ ██████╗ ██╗     ███████╗███╗   ██╗ ██████╗███████╗        ██╗    ██╗    ███████╗███╗   ██╗ ██████╗ ██████╗ ██████╗ ███████╗                                
██║   ██║██║██╔═══██╗██║     ██╔════╝████╗  ██║██╔════╝██╔════╝       ██╔╝   ██╔╝    ██╔════╝████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔════╝                                
██║   ██║██║██║   ██║██║     █████╗  ██╔██╗ ██║██║     █████╗        ██╔╝   ██╔╝     █████╗  ██╔██╗ ██║██║     ██║   ██║██████╔╝█████╗                                  
╚██╗ ██╔╝██║██║   ██║██║     ██╔══╝  ██║╚██╗██║██║     ██╔══╝       ██╔╝   ██╔╝      ██╔══╝  ██║╚██╗██║██║     ██║   ██║██╔══██╗██╔══╝                                  
 ╚████╔╝ ██║╚██████╔╝███████╗███████╗██║ ╚████║╚██████╗███████╗    ██╔╝   ██╔╝       ███████╗██║ ╚████║╚██████╗╚██████╔╝██║  ██║███████╗                                
  ╚═══╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═══╝ ╚═════╝╚══════╝    ╚═╝    ╚═╝        ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝                                
                                                                                                                                                                        
         ██╗     ██╗██╗  ██╗███████╗    ██████╗ ██████╗ ███╗   ██╗ ██████╗ ███████╗    ████████╗ ██████╗     ██╗  ██╗███████╗ █████╗ ██╗   ██╗███████╗███╗   ██╗        
         ██║     ██║██║ ██╔╝██╔════╝    ██╔══██╗██╔══██╗████╗  ██║██╔════╝ ██╔════╝    ╚══██╔══╝██╔═══██╗    ██║  ██║██╔════╝██╔══██╗██║   ██║██╔════╝████╗  ██║        
         ██║     ██║█████╔╝ █████╗      ██████╔╝██████╔╝██╔██╗ ██║██║  ███╗███████╗       ██║   ██║   ██║    ███████║█████╗  ███████║██║   ██║█████╗  ██╔██╗ ██║        
         ██║     ██║██╔═██╗ ██╔══╝      ██╔═══╝ ██╔══██╗██║╚██╗██║██║   ██║╚════██║       ██║   ██║   ██║    ██╔══██║██╔══╝  ██╔══██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║        
██╗██╗██╗███████╗██║██║  ██╗███████╗    ██║     ██║  ██║██║ ╚████║╚██████╔╝███████║       ██║   ╚██████╔╝    ██║  ██║███████╗██║  ██║ ╚████╔╝ ███████╗██║ ╚████║        
╚═╝╚═╝╚═╝╚══════╝╚═╝╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝       ╚═╝    ╚═════╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
{"\33[0m"}'''
        print(title_drop)
        sleep(1.25)
        print("S T A R T I N G  R O U T I N E . . .\n")
        sleep(1)
        print(f'{"\33[1;91m"}WARNING: INTRUDER DETECTED')
        sleep(0.25)
        print(f'-- LIFESTEAL ENABLED --{"\33[0m"}')
        sleep(1)
        
def menu_box():
        rainbow_colors = ["\33[91m", "\33[33m", "\33[92m","\33[34m", "\33[36m", "\33[95m"]
        text = "[+ FISTFUL OF DOLLAR]"
        italy = '\x1B[3m'
        r_c = "\33[0m"

        colored_text = ''.join(f"{rainbow_colors[i % len(rainbow_colors)]}{italy}{char}{r_c}" for i, char in enumerate(text))

        l_pre = "║ 2 - perform_deadcoin << "
        l_suf = "║"
        width = 54 
        text_width = width - len(l_pre) - len(l_suf)
        padd = text_width - len(text)
        res = colored_text + ' ' * padd

        box = f"""
╔════════════════════════════════════════════════════╗
║ 1 - get_encrypted_flag                             ║
{l_pre}{res}{l_suf}
║ 3 - call_the_signer                                ║
║ 4 - level_restart                                  ║
║ 5 - level_quit                                     ║
╚════════════════════════════════════════════════════╝
        """

        print(box)



def death_message():
        print('''

▗▖  ▗▖▗▄▖ ▗▖ ▗▖     ▗▄▖ ▗▄▄▖ ▗▄▄▄▖    ▗▄▄▄  ▗▄▄▄▖ ▗▄▖ ▗▄▄▄  
 ▝▚▞▘▐▌ ▐▌▐▌ ▐▌    ▐▌ ▐▌▐▌ ▐▌▐▌       ▐▌  █ ▐▌   ▐▌ ▐▌▐▌  █ 
  ▐▌ ▐▌ ▐▌▐▌ ▐▌    ▐▛▀▜▌▐▛▀▚▖▐▛▀▀▘    ▐▌  █ ▐▛▀▀▘▐▛▀▜▌▐▌  █ 
  ▐▌ ▝▚▄▞▘▝▚▄▞▘    ▐▌ ▐▌▐▌ ▐▌▐▙▄▄▖    ▐▙▄▄▀ ▐▙▄▄▖▐▌ ▐▌▐▙▄▄▀ 
                                                            

          ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⠴⠶⠶⠶⠶⠶⠶⠶⠶⢤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
          ⠀⠀⠀⠀⢀⣤⠶⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠶⣤⡀⠀⠀⠀⠀⠀
          ⠀⠀⢀⡴⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢷⡄⠀⠀⠀
          ⠀⣰⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣦⠀⠀
          ⢰⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣧⠀
          ⣿⠀⠀⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡄⠀⢹⡄
          ⡏⠀⢰⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⢸⡇
          ⣿⠀⠘⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡟⠀⢸⡇
          ⢹⡆⠀⢹⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⣾⠀
          ⠈⢷⡀⢸⡇⠀⢀⣠⣤⣶⣶⣶⣤⡀⠀⠀⠀⠀⠀⢀⣠⣶⣶⣶⣶⣤⣄⠀⠀⣿⠀⣼⠃⠀
          ⠀⠈⢷⣼⠃⠀⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⡇⠀⢸⡾⠃⠀⠀
          ⠀⠀⠈⣿⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⠃⠀⢸⡇⠀⠀⠀
          ⠀⠀⠀⣿⠀⠀⠘⢿⣿⣿⣿⣿⡿⠃⠀⢠⠀⣄⠀⠀⠙⢿⣿⣿⣿⡿⠏⠀⠀⢘⡇⠀⠀⠀
          ⠀⠀⠀⢻⡄⠀⠀⠀⠈⠉⠉⠀⠀⠀⣴⣿⠀⣿⣷⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀⢸⡇⠀⠀⠀
          ⠀⠀⠀⠈⠻⣄⡀⠀⠀⠀⠀⠀⠀⢠⣿⣿⠀⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⠀⠀⠀⠀
          ⠀⠀⠀⠀⠀⠘⣟⠳⣦⡀⠀⠀⠀⠸⣿⡿⠀⢻⣿⡟⠀⠀⠀⠀⣤⡾⢻⡏⠁⠀⠀⠀⠀⠀
          ⠀⠀⠀⠀⠀⠀⢻⡄⢻⠻⣆⠀⠀⠀⠈⠀⠀⠀⠈⠀⠀⠀⢀⡾⢻⠁⢸⠁⠀⠀⠀⠀⠀⠀
          ⠀⠀⠀⠀⠀⠀⢸⡇⠀⡆⢹⠒⡦⢤⠤⡤⢤⢤⡤⣤⠤⡔⡿⢁⡇⠀⡿⠀⠀⠀⠀⠀⠀⠀
          ⠀⠀⠀⠀⠀⠀⠘⡇⠀⢣⢸⠦⣧⣼⣀⡇⢸⢀⣇⣸⣠⡷⢇⢸⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀
          ⠀⠀⠀⠀⠀⠀⠀⣷⠀⠈⠺⣄⣇⢸⠉⡏⢹⠉⡏⢹⢀⣧⠾⠋⠀⢠⡇⠀⠀⠀⠀⠀⠀⠀
          ⠀⠀⠀⠀⠀⠀⠀⠻⣆⠀⠀⠀⠈⠉⠙⠓⠚⠚⠋⠉⠁⠀⠀⠀⢀⡾⠁⠀⠀⠀⠀⠀⠀⠀
          ⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡴⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀
          ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠳⠶⠦⣤⣤⣤⡤⠶⠞⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
''')
        
        
