#include <iostream>
#include <string.h>
#include <signal.h>
#include <string>
#include <functional>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <map>
#include <memory>
#include <stdlib.h>
#include <unistd.h>
#define TIMEOUT 300
#define FLAG "/home/ragnarok/flag"
using namespace std;

class Figure{
	public :
		Figure():atk(0),hp(0){
		};
		Figure(const Figure &copyfigure){
			desc = copyfigure.desc;
			weapon = copyfigure.weapon;
			atk = copyfigure.atk;
			def = copyfigure.def;
			hp = copyfigure.hp;
			mp = copyfigure.mp ;
		};
		
		Figure& operator=(const Figure &copyfigure){
			desc = copyfigure.desc;
			weapon = copyfigure.weapon;
			atk = copyfigure.atk;
			def = copyfigure.def ;
			hp = copyfigure.hp;
			mp = copyfigure.mp;
		};



		virtual void add_weapon(string str){
			weapon = str ;
		};

		virtual void cast_spell(shared_ptr<Figure> figure){
		};
		
		virtual void info(){
			cout << "Name : " << name << endl ;
			cout << "Description : " << desc << endl ;
			if(!weapon.empty())
				cout << "Weapon : " << weapon << endl ;
			cout << "Atk : " << atk << endl ;
			cout << "Hp : " << hp << endl ;
			cout << "Mp : " << mp << endl ;
		}

		void damage(shared_ptr<Figure> figure){
			if(atk > figure->def)
				figure->hp -= (atk - figure->def) ;
		}

		void defense(){
			def += 200 ;
			hp += 200 ;
		}

		void change_desc(string str){
			desc = str ;
		}

		void add_atk(int inc_atk){
			atk += inc_atk ;
		}

		void add_def(int inc_def){
			def += inc_def ;
		}

		void add_hp(int inc_hp){
			hp += inc_hp ;
		}
		
		void add_mp(int inc_mp){
			mp += inc_mp ;
		}

		string get_name(){
			return name ;
		}

		long get_hp(){
			return hp ;
		}
		
		long get_mp(){
			return mp ;
		}

		virtual ~Figure(){
			name.clear();
			desc.clear();
			weapon.clear();
			atk = 0 ;
			hp = 0 ;
			mp = 0 ;
			def = 0 ;
		};
				
	protected:
		string name ;
		string desc ;
		string weapon ;
		long atk ;
		long hp ;
		long mp ;
		long def ;

};

shared_ptr<Figure> enemy ;
shared_ptr<Figure> character ;
string name ;
unsigned int money = 0 ;
unsigned int highest = 0 ;
unsigned int rate = 100 ; 

//Character
class Odin: public Figure {
	public :
		Odin(){
			name = "Odin" ;
			desc = "Odin's skill is to increase atk & def" ;
			atk = 1034 ;
			hp = 4561 ;
			mp = 1721 ;
			def = 800 ;

		};
		
		Odin(string figureweapon){
			name = "Odin" ;
			desc = "Odin's skill is to increase atk & def" ;
			atk = 1034 ;
			hp = 4561 ;
			mp = 1721 ;
			def = 800 ;
			add_weapon(figureweapon);	


		};
		
		void cast_spell(shared_ptr<Figure> figure){
			if(mp >= 1600){
				this->add_mp(-1600);			
				figure->add_atk(1034);
				figure->add_def(800);
				cout << "\033[35m" << figure->get_name() << ": (atk+1034,def+800)\033[0m" << endl;

			}else{
				cout << "You have no power !" << endl ;
			}
		}

		virtual void add_weapon(string str){
			if(weapon.empty()){
				weapon = str ;
				if(!weapon.compare("Droupnir")){
					add_atk(800);
				}
				if(!weapon.compare("Gungnir")){
					add_mp(1600);
					cast_spell(shared_ptr<Figure>(this));
				}
				if(!weapon.compare("Sleiphnir")){
					add_hp(300);
				}
				cout << "Done !" << endl ;
			}else{
				cout << "You already have weapons" << endl ;
			}
		}
		
		~Odin(){
		};
};

class Thor: public Figure {
	public :
		Thor(){
			name = "Thor" ;
			desc = "Thor's skill is to damage the enemy" ;
			atk = 2510 ;
			hp = 5891 ;
			mp = 1024 ;
			def = 800 ;
		};
		
		Thor(string figureweapon){
			name = "Thor" ;
			desc = "Thor's skill is to damage the enemy" ;
			atk = 2510 ;
			hp = 5891 ;
			mp = 1024 ;
			def = 800 ;
			add_weapon(figureweapon);	
		};
		
		void cast_spell(shared_ptr<Figure> figure){
			if(mp >= 800){
				this->add_mp(-800);
				figure->add_hp(-3000);
				cout << "\033[35m" << figure->get_name() << ": (hp-3000)\033[0m" << endl;
			}else{
				cout << "You have no power !" << endl ;
			}
		}

		virtual void add_weapon(string str){
			if(weapon.empty()){
				weapon = str ;
				if(!weapon.compare("Mjollnir")){
					add_atk(800);
				}
				if(!weapon.compare("Larngreiper")){
					add_hp(800);
					add_def(200);
				}
				if(!weapon.compare("Megingjord")){
					add_mp(2170);
				}
				cout << "Done !" << endl ;
			}else{
				cout << "You already have weapons" << endl ;
			}
		}

		~Thor(){
		};
};

class Freyr: public Figure {
	public :
		Freyr(){
			name = "Freyr" ;
			desc = "Freyr's skill is to decrease hp & increase atk" ;
			atk = 217 ;
			hp = 8888 ;
			mp = 2017 ;
			def = 1200 ;
		};
		
		Freyr(string figureweapon){
			name = "Freyr" ;
			desc = "Freyr's skill is to decrease hp & increase atk" ;
			atk = 217 ;
			hp = 8888 ;
			mp = 2017 ;
			def = 1200 ;
			add_weapon(figureweapon);	
		};
		
		void cast_spell(shared_ptr<Figure> figure){
			if(mp >= 1000){
				add_mp(-1000);
				figure->add_hp(-5000);
				figure->add_atk(4000);
				cout << "\033[35m" << figure->get_name() << ": (hp-5000,atk+4000)\033[0m" << endl;
			}else{
				cout << "You have no power !" << endl ;
			}
		}

		virtual void add_weapon(string str){
			if(weapon.empty()){
				weapon = str ;
				if(!weapon.compare("Skidbladnir")){
					add_hp(4000);
					add_atk(-200);
				}
				if(!weapon.compare("Gullinbursti")){
					rate *= 4  ;
				}
				if(!weapon.compare("Laevateinn")){
					add_atk(1000);
					add_hp(-1500);
				}
				if(!weapon.compare("Bllodyhoof")){
					add_hp(2170);
					add_def(400);
				}
				cout << "Done !" << endl ;
			}else{
				cout << "You already have weapons" << endl ;
			}
		}

		~Freyr(){
			if(!weapon.empty()){
				if(!weapon.compare("Gullinbursti")){
					rate /= 4  ;
				}
				
			}
		};
};
//Enemy
class Fenrir : public Figure {
	public :
		Fenrir(){
			name = "Fenrir" ;
			desc = "Fenrir's skill is to damage the enemy" ;
			atk = 1024 ;
			hp = 8192 ; 
			mp = 4212 ;
			def = 700 ;
		};
		
		Fenrir(string figureweapon){
			name = "Fenrir" ;
			desc = "Fenrir's skill is to damage the enemy" ;
			atk = 1024 ;
			hp = 8192 ;
			mp = 4212 ;
			def = 700 ;
			add_weapon(figureweapon);	
		};
		
		void cast_spell(shared_ptr<Figure> figure){
			if(mp >= 1500){
				add_mp(-1500);
				figure->add_hp(-6000);
				cout << "\033[35m" << figure->get_name() << ": (hp-6000)\033[0m" << endl;
			}else{
				cout << "You have no power !" << endl;
			}
		}

		virtual void add_weapon(string str){
			if(weapon.empty()){
				weapon = str ;
				if(!weapon.compare("Spike")){
					add_atk(1024);
					add_def(300);
				}
			}else{
				cout << "You already have weapons" << endl ;
			
			}
		}

		~Fenrir(){
		};
	
};

class Loki : public Figure {
	public :
		Loki(){
			name = "Loki" ;
			desc = "Loki's skill is to increase atk & def" ;
			atk = 2024 ;
			hp = 55660 ;
			mp = 5566 ;
			def = 666 ;
		};
		
		Loki(string figureweapon){
			name = "Loki" ;
			desc = "Loki's skill is to increase atk & def" ;
			atk = 2024 ;
			hp = 5566 ;
			mp = 5566 ;
			def = 666 ;
			add_weapon(figureweapon);	
		};
		
		void cast_spell(shared_ptr<Figure> figure){
			if(mp >= 1500){
				add_mp(-1500);
				add_atk(3000);
				add_def(300);
				cout << "\033[35m" << get_name() << ": (atk+3000,def+300)\033[0m" << endl;
			}else{
				cout << "You have no power !" << endl ;
			}
		}

		virtual void add_weapon(string str){
			if(weapon.empty()){
				weapon = str ;
				if(!weapon.compare("Sif's hair")){
					add_hp(1024);
					add_def(300);
				}
				if(!weapon.compare("Gungnir")){
					cast_spell(shared_ptr<Loki>(this));
				}
			}else{
				cout << "You already have weapons" << endl ;
			
			}
		}

		~Loki(){
		};


};

class Jormungandr : public Figure {
	public :
		Jormungandr(){
			name = "Jormungandr" ;
			desc = "Jormungandr's skill is to increase hp" ;
			atk = 4024 ;
			hp = 6566 ;
			mp = 4123 ;
			def = 777 ;
		};
		
		Jormungandr(string figureweapon){
			name = "Jormungandr" ;
			desc = "Jormungandr's skill is to increase hp" ;
			atk = 4024 ;
			hp = 6445 ;
			mp = 4123 ;
			def = 777 ;
			add_weapon(figureweapon);	
		};
		
		void cast_spell(shared_ptr<Figure> figure){
			if(mp >= 800){
				add_mp(-800);
				add_hp(3000);
				cout << "\033[35m" << get_name() << ": (hp+3000)\033[0m" << endl;
			}else{
				cout << "You have no power !" << endl ;
			}
		}

		virtual void add_weapon(string str){
			if(weapon.empty()){
				weapon = str ;
				if(!weapon.compare("Tooth")){
					add_atk(1024);
					add_hp(1024);
				}
			}else{
				cout << "You already have weapons" << endl ;
			
			}
		}

		~Jormungandr(){
		};


};



void sig_alarm_handler(int signum){
    cout << "Timeout" << endl ;
    exit(1);
}

void init(){
    setvbuf(stdin,0,_IONBF,0);
    setvbuf(stdout,0,_IONBF,0);
    setvbuf(stderr,0,_IONBF,0);
    srand(time(NULL));
    signal(SIGALRM,sig_alarm_handler);
    alarm(TIMEOUT);
}

void create_enemy(){
	switch(rand() % 3+1){
		case 1 :
			enemy = shared_ptr<Fenrir>(new Fenrir("Spike"));
			break ;
		case 2 :
			enemy = shared_ptr<Loki>(new Loki("Sif's hair"));
			break ;
		case 3 :
			enemy = shared_ptr<Jormungandr>(new Jormungandr("Tooth"));
			break ;
	}
}

void figure_list(){
	cout << "*****************" << endl ;
	cout << " 1.Odin          " << endl ;
	cout << " 2.Thor          " << endl ;
	cout << " 3.Freyr         " << endl ;
	cout << "*****************" << endl ;
}

int select_figure(){
	unsigned int choice ;
	if(!character){
		figure_list();
		cout << "Choose your figure :" ;
		cin >> choice ;
		if(!cin.good()){
			cout << "format error !" << endl ;
			_exit(-1);
		}
		switch(choice){
			case 1 :
				character = shared_ptr<Odin>(new Odin());
				break ;
			case 2 :
				character = shared_ptr<Thor>(new Thor());
				break ;
			case 3 :
				character = shared_ptr<Freyr>(new Freyr());
				break ;
			default :
				cout << "\033[31mInvaild choice\033[0m" << endl ;
				return 0 ;
		}
		cout << "Done !" << endl ;
	}else{
		cout << "You have selected a figure !" << endl;
	}
	return 1 ;
}

void show_figure(){
	if(!name.empty()){
		cout << "------------- The highest record -------------" << endl ;
		cout << " Name : " << name << endl ;
		cout << " Money : " << highest << endl ;
		cout << "----------------------------------------------" << endl ;
	}
	cout << "Current money : " << money << endl ;
	if(character){
		character->info();
	}else{
		cout << "You need to select a character first !" << endl ;
	}
}

void change_descript(){
	string desc ;
	if(character){
		cout << "Description : " ;
		cin >> desc ;
		character->change_desc(desc);
	}else{
		cout << "You need to select a character first !" << endl ;
	}
}

void make_weapon(){
	string weapon ;
	if(character){
		if(money >= 133700){
			cout << "Name of your weapon :" ;
			cin.ignore();
			getline(cin,weapon);
			character->add_weapon(weapon);
			money -= 133700 ;
		}else {
			cout << "You need to get more money !" << endl;
		}
	}else{	
		cout << "You need to select a character first !" << endl ;
	}
}

void cast(){
	unsigned int choice ;
	cout << "===========================" << endl ;
	cout << " 1. Enemy                  " << endl ;
	cout << " 2. Self                   " << endl ;
	cout << "===========================" << endl ;
	cout << "Target :" ;
	cin >> choice ;
	switch(choice){
		case 1 :
			for(int i = 0 ; i < 10 ; i++){
				usleep(100000);
				cout << "!!!" ;
			}
			cout << endl ;
			character->cast_spell(enemy);
			break ;
		case 2 :
			for(int i = 0 ; i < 10 ; i++){
				usleep(100000);
				cout << "!!!" ;
			}
			cout << endl ;
			character->cast_spell(character);
			break ;
		default : 
			cout << "Invalid choice ! " << endl ;
			return ;
	}

}

void set_name(){
	if(name.empty()){
		cout << "Name :" ;
		cin >> name ;
	}else{
		cout << "Your name is " << name << endl; 
	}
}

void fight_menu(){
	cout << "###########################" << endl ;
	cout << "          Action           " << endl ;
	cout << "###########################" << endl ;
	cout << "  1. Attack                " << endl ;
	cout << "  2. Defense               " << endl ;
	cout << "  3. Cast Spell            " << endl ;
	cout << "  4. Run                   " << endl ;
	cout << "###########################" << endl ;

}

void fight_enemy(){	
	unsigned int status ;
	int fd ;
	int choice ;
	if(character){
		while(1){
			cout << "============================================" << endl ;
			cout << "Enemy Info : " << endl ;
			enemy->info();
			cout << "============================================" << endl ;
			cout << "Your Info : " << endl ;
			character->info();
			cout << "============================================" << endl ;
			fight_menu();
			cout << "Your choice : ";
			cin >> choice ;
			if(!cin.good()){
				cout << "format error !" << endl;
				_exit(0);
			}
			// Your round
			switch(choice){
				case 1 :
					cout << "\033[33mYou damage enemy !\033[0m" << endl ;
					character->damage(enemy);
					break ;
				case 2 :
					cout << "\033[33mIncrese your hp and def\033[0m" << endl ;
					character->defense();
					break ;
				case 3 :
					cast();
					break ;
				case 4 :
					return ;
					break ;
				default :
					cout << "Invalid choice !" << endl ;
					break ;
			}
			// enemy round
			status = rand() % 3 ;
			switch(status){
				case 0 :
					cout << "\033[33mEnemy attack you !\033[0m" << endl ;
					enemy->damage(character);
					break ;
				case 1 :
					cout << "\033[33mEnemy defense !\033[0m" << endl;
					enemy->defense();
					break ;
				case 2 :
					cout << "\033[33mEnemy cast spell !\033[0m" << endl;
					enemy->cast_spell(character);
					break ;
			}
			if(character->get_hp() < 0){
				cout << "\033[31mYou died !\033[0m" << endl ;
				character = NULL ;
				cout << "\033[33mDo you want to continue ? (0:No/1:Yes)\033[0m :"  ;
				cin >> choice ;
				if(!cin.good()){
					cout << "format error !" << endl;
					_exit(0);
				}
				if(choice == 1){
					if(money >= 217){
						money -= 217 ;
						return ;
					}else{
						cout << "You do not have enough money !" << endl ;
					}
				}
				cout << "\033[31m = = = = = = Game Over = = = = = = \033[0m" << endl ;
				exit(0);
				
			}
			if(enemy->get_hp() < 0){
				cout << "\033[33m You win !\033[0m" << endl ;
				enemy = NULL ;
				cout << "Something for you :)" << endl ;

				money += 133700 ;
				if(money > highest){
					cout << "Record your score ~" << endl ;
					set_name();
					highest = money ;
				}
				if(money > 0x55555555){
					fd = open(FLAG,0);
					char *buf = new char[100] ;
					read(fd,buf,80);
					free(buf);
					close(fd);
				}

				create_enemy();
				cout << "New enemy has borned ! " << endl ;
				return ;
			}
		}
	}else{
		cout << "You need to select a character first !" << endl ;
	}
}




void read_input(char *buf,unsigned int size){
    int ret ;
    ret = read(0,buf,size);
    if(ret <= 0){
        puts("read error");
        _exit(1);
    }
}

void print_h(char c){
    printf("    %c     %c      \n",c,c);
    printf("     %c     %c     \n",c,c);
    printf("     %c%c%c%c%c%c%c     \n",c,c,c,c,c,c,c);
    printf("     %c     %c     \n",c,c);
    printf("      %c     %c    \n",c,c);
}

void print_i(char c){
    printf("     %c%c%c     \n",c,c,c);
    printf("      %c     \n",c);
    printf("      %c     \n",c);
    printf("      %c     \n",c);
    printf("     %c%c%c     \n",c,c,c);
}
void print_t(char c){
    printf("   %c%c%c%c%c%c%c    \n",c,c,c,c,c,c,c);
    printf("      %c     \n",c);
    printf("      %c     \n",c);
    printf("      %c     \n",c);
    printf("      %c     \n",c);

}
void print_c(char c){
    printf("     %c%c%c%c     \n",c,c,c,c);
    printf("    %c     \n",c);
    printf("   %c     \n",c);
    printf("    %c     \n",c);
    printf("     %c%c%c%c     \n",c,c,c,c);
}

void print_o(char c){
    printf("    %c%c%c%c     \n",c,c,c,c);
    printf("    %c    %c \n",c,c);
    printf("   %c      %c\n",c,c);
    printf("    %c    %c \n",c,c);
    printf("      %c%c%c%c     \n",c,c,c,c);

}
void print_n(char c){
    printf("   %c    %c    \n",c,c);
    printf("    %c   %c%c    \n",c,c,c);
    printf("    %c %c  %c    \n",c,c,c);
    printf("    %c%c   %c    \n",c,c,c);
    printf("     %c    %c    \n",c,c);
}




void money_gen(){
    char *charset = "hitcon";
    char buf[8];
    char c;
    int idx ;
    int padding ;
	map<int,function<void (char)>> fptr = {
		{0,print_h},
		{1,print_i},
		{2,print_t},
		{3,print_c},
		{4,print_o},
		{5,print_n}
	};
	if(money > 0x50000000){
		cout << "Your money is too much !" << endl;
		return ;
	}
    cout << "You need to input a charactor which is same as the asciiart to get the power" << endl ;
    cout << "Enter \"q\" to leave the station" << endl ;
    while(true){
		usleep(100000);
        idx = rand() % 6 ;
        c = rand() % 0x5e + 0x21;
        padding = rand() % 0x42 ;
        cout << "***************************" << endl;
        fptr[idx](c);
		cout << "***************************" << endl ;
        cout << "Magic : " ;
        read_input(buf,2);
        if(buf[0] == 'q')
            break;
        if(buf[0] == charset[idx]){
            money += rate ;
            cout << "Get money !" << endl ;
        	cout << "Your money : " << money << endl;
		}else{
            cout << "Boom !!!" << endl ;
			if(money > 1000){
            	money -= 1000 ;
			}else{
				money = 0 ;
			}
			return ;
        }
    }
}




void main_menu(){
	cout << endl ;
	cout << "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" << endl ;
	cout << "                    RAGNAROK                    " << endl ;
	cout << "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" << endl ;
	cout << "@                                              @" << endl ;
	cout << "@ 1. Choose your figure                        @" << endl ;
	cout << "@ 2. Show your info                            @" << endl ;
	cout << "@ 3. Earn money                                @" << endl ;
	cout << "@ 4. Make & Equip weapon                       @" << endl ;
	cout << "@ 5. Fight against the enemy                   @" << endl ;
	cout << "@ 6. Change your description                   @" << endl ;
	cout << "@ 7. Give up                                   @" << endl ;
	cout << "@                                              @" << endl ;
	cout << "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" << endl ;
}

int main(){
    unsigned int choice ;
    init();
	create_enemy();
    while(1){
		main_menu();
        cout << "Your choice :" ;
        cin >> choice ;
        cout << endl ;
        if(!cin.good()){
            cout << "format error !" << endl;
            _exit(0);
        }
		switch(choice){
			case 1 :
				select_figure();
				break ;				
			case 2 :
				show_figure();
				break ;
			case 3 :
				money_gen();
				break ;
			case 4 :
				make_weapon();
				break ;
			case 5 :
				fight_enemy();
				break ;
			case 6 :
				change_descript();
				break ;
			case 7 :
				cout << "\033[34mGoodbye\033[0m" << endl ;
				_exit(0);
			default :
				cout << "\033[31mInvaild choice\033[0m" << endl ;
				break ;
		}
	}
	return 0 ; 
}
