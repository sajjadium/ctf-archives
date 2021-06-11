#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

//gcc -O0 -Wl,-z,relro,-z,now -fno-stack-protector-all -o ../ressources/kikoo_4_ever kikoo_4_ever.c

#define REGLE_BUF_SIZE 512
#define LIEUX_BUF_SIZE 48
#define ARRAY_SIZE 100
#define TINY_ARRAY_SIZE 5

typedef struct regle{
  char regle[REGLE_BUF_SIZE];
  int locked;
}Regle;

typedef struct lieux{
  char nom[LIEUX_BUF_SIZE];
  int visite;
  char initiale;
}Lieux;

typedef struct kikoos_observe{
  char pseudos[10][32];
  char observations[10][128];
  int n_observation;
}Kikoos_observe;

Regle *les_regles_du_kikoo[ARRAY_SIZE];
Lieux les_lieux_du_kikoo[TINY_ARRAY_SIZE];
Kikoos_observe kikoos_observe;

int read_user_int(){
	char buf[9];
	int i;

	fgets(buf, 8, stdin);
	i = atoi(buf);

	return i;
}

void read_user_str(char* s, int size){
	char *ptr = NULL;
	read(0, s, size);
	ptr = strchr(s, '\n');
	if(ptr != NULL)
		*ptr = 0;
  //Si il y a pas de \n c'est qu'il a rempli le buffer au max du max, enfin j'crois
  else
    s[size] = 0;
}


int get_free_index(void **tab){
  for(int i = 0 ; i < ARRAY_SIZE ; i++){
    if(tab[i] == NULL)
      return i;
  }
  return -1;
}

void ajouter_observation(char *pseudo, char *observation){
  strncpy(kikoos_observe.pseudos[kikoos_observe.n_observation], pseudo, 32);
  strncpy(kikoos_observe.observations[kikoos_observe.n_observation], observation, 128);
  kikoos_observe.n_observation++;
}

void lire_observations(){
  if(kikoos_observe.n_observation <= 0){
    puts("No interesting observations at this time.");
    return;
  }


  for(int i = 0 ; i < kikoos_observe.n_observation ; i++){
    printf("Observation n°%d:\n\tNickname: %s\n\tNote: %s\n", (i+1), kikoos_observe.pseudos[i], kikoos_observe.observations[i]);

  }
}

void creer_lieux(int i, char *nom, int visite, char initiale){
  Lieux *lieux;

  lieux = &les_lieux_du_kikoo[i];

  memcpy(lieux->nom, nom, LIEUX_BUF_SIZE);
  lieux->visite = visite;
  lieux->initiale = initiale;
}

Regle* creer_regle(char *str_regle, int locked){
  Regle *regle = NULL;
  int i = -1;

  i = get_free_index((void**)les_regles_du_kikoo);
  if(i == -1){
    puts("The list of rules is full.");
    return NULL;
  }

  regle = malloc(sizeof(Regle));
  if(regle == NULL){
    return NULL;
  }

  memcpy(regle->regle, str_regle, REGLE_BUF_SIZE);
  regle->locked = locked;

  les_regles_du_kikoo[i] = regle;
  return regle;
}

void ecrire_regle(){
  char buf[REGLE_BUF_SIZE];
  int i;
  char go_on[8] = "n";
  Regle *regle = NULL;

  if(kikoos_observe.n_observation == 0){
    puts("What are you going to write? We haven't found anything interesting yet.");
    puts("Let's go find some kikoo.");
    return;
  }

  i = get_free_index((void**)les_regles_du_kikoo);
  if(i == -1){
    puts("The list of rules is full.");
    return;
  }

  puts("\nMake me dream, what's that rule?");
  do{
    printf("Rule n°%d: ", (i+1));
    read_user_str(buf, REGLE_BUF_SIZE+0x10);
    printf("Read back what you just wrote:\n%s\n", buf);
    printf("Is it ok? Shall we move on? (y/n)");
    read_user_str(go_on, 4);
  }while(go_on[0] != 'y');

  regle = creer_regle(buf, 1);
  les_regles_du_kikoo[i] = regle;
}

void init_buffering(){
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
}



void scenario_j(){
  puts("\nOkay, I think I got what we need.");
  puts("Topic: [Recherche] Pseudo stylé :D *clic*");
  puts("\nWell, let's see..");
  sleep(3);

  puts("\n------------------------------------------------");
  puts("x_Skipix_x\n29 septembre 2011 à 11:09:54");
  puts("HELP ME FAITES MOI DON D 1 NOM PR JE VIVE :)");
  puts("------------------------------------------------");

  puts("\n------------------------------------------------");
  puts("x_Skipix_x\n29 septembre 2011 à 11:11:24");
  puts("j'ai trouvé Qabutox mais je trouve sa fait un peu trop pokemon ^.^");
  puts("------------------------------------------------");

  puts("\n------------------------------------------------");
  puts("Buffd0ver_flow\n29 septembre 2011 à 11:13:07");
  puts("Shape, trouver en 2.4 sec Pseudo style :sunglasses: Swyfter sinan");
  puts("------------------------------------------------");

  puts("\n------------------------------------------------");
  puts("jer75emy\n29 septembre 2011 à 11:16:48");
  puts("Qabutox je trouve c'est un peu gamin. Mais Swyfter ça me plait.");
  puts("------------------------------------------------");


  puts("\nThat's interesting, but it's not enough.");
  ajouter_observation("jer75emy", "Mature Kikoo");
  puts("\n [+] A new observation has been added to your notebook.");
  puts("\nLet's look for a juicier topic.");
  puts("\nOn the Minecraft forum... Topic: [Serveur Minecraft] Pvp - faction *clic*");
  puts("\nSo what does it say on this topic...");
  sleep(3);

  puts("\n------------------------------------------------");
  puts("Kankan776\n25 septembre 2012 à 15:35:41");
  puts("Slt tout le monde ! Jvous presente mon serveur Minecraft pvp-faction ! Cest un serveur 6 slots ...");
  puts("------------------------------------------------");

  puts("\n------------------------------------------------");
  puts("Kankan776\n2 octobre 2012 à 11:05:59");
  puts("Le serv viens de passer à 15 slots ! Le nouvel ip: onsefousurlagueule.turboserv.eu");
  puts("------------------------------------------------");


  puts("\nI like that. I don't know why, but his nickname sounds familiar... :thinking:");

  ajouter_observation("Kankan776", "High level Kikoo, owner of a minecraft pvp faction server.");
  puts("\n [+] A new observation has been added to your notebook.");
  sleep(3);
}

void scenario_y(){
  int time_usleep = 300000;

  puts("\nAll right, let's see what we can find interesting.");
  puts("Here, this looks like fun. *clic*\n");
  sleep(3);

  puts("*video sound*");
  puts("- Bonjour Michel.");
  puts("- Bonjour Michel ça va ?");
  puts("- Vous m'avez oublié.");
  puts("- J'suis désolé j'étais en pleine partie de \"Qui est ce ?\".");
  puts("Vous savez le jeu où on doit trouver le visage de..");
  puts("- Je sais c'que c'est Michel.. Mais vous jouez avec qui ?");
  puts("- Tout seul. Bon je gagne à chaque fois mais ça m'occupe..");
  puts("*...*");

  puts("\nTwo minutes later...");
  sleep(3);
  puts("\n*...*");
  puts("- Regardez bien..");
  puts("Cette armoire à étagères lui tombe dessus. À première vu on dirait que ..?");
  puts("- Bah que c'est l'armoire d'une marque suédoise très connue, le genre de truc qu'on met 7 heures à monter mais qui se déboite au moindre choc.");
  puts("- Vous vouliez pas citer Ikea c'est ça ?");
  puts("- Oui c'était l'idée heum en effet.");
  puts("- Sauf que celle-ci d'armoire, c'est pas eux, parce que...");
  puts("*...*");

  puts("\nWhat the hell am I doing? We're supposed to be looking for kikoo, let's go look over here...");

  printf("\nSearch Bar: ");
  printf("C"); usleep(time_usleep);
  printf("h"); usleep(time_usleep);
  printf("o"); usleep(time_usleep);
  printf("u"); usleep(time_usleep);
  printf("m"); usleep(time_usleep);
  printf("i"); usleep(time_usleep*2);
  puts(" *Enter*");

  puts("Maybe this video will help us... *clic*");
  sleep(3);
  puts("\n*video sound*");
  puts("- Oh c'est dégeu !");
  puts("HMM! HMMM!");
  puts("*BOUM*");
  puts("*...*");

  puts("\nYeah, well, let's go see the comments.");

  puts("\"Comments are disabled\"");

  puts("\nWell, great..");

  puts("Okay, fuck choumi, I've got a better idea.");

  printf("\nSearch Bar: ");

  printf("T"); usleep(time_usleep);
  printf("k"); usleep(time_usleep);
  printf("7"); usleep(time_usleep);
  printf("7"); usleep(time_usleep*2);
  puts(" *Enter*");

  puts("Let's get the first video. *clic*");
  sleep(3);
  puts("\n*video sound*");
  puts("- Salam les khey, petite vidéo, avant d'entamer le sujet en ce qui concerne jean permanof, JP");
  puts("en ce qui concerne le ddos, j'tenais tout simplement à faire passer un petit message à tous les streamhackers.");
  puts("Allez tous vous faire enculer !");
  puts("*...*");

  puts("\n*Pause*\nShut up. That's the feedback we want.");

  puts("\n\"Force à jp...\", All right..");

  puts("\"Tk tu un grand homme...\", Yeah, okay.\nYoutube may not be the best place to make good observations.");

  puts("\nLet's go somewhere else.");
  sleep(3);
}

void scenario_t(){
  puts("\nSo, what's up with Twitch today?");
  puts("A little Minecraft stream with 11 viewers? Sounds pretty good to me.. *clic*");


  puts("\n*stream sound*");
  puts("- Fais toi une maison en caca on se retrouve demain quand il fera jour.");
  puts("- Aïe ! Y a un archer qui me tape !");
  puts("*...*");
  sleep(3);

  puts("\nSo what's the chatter on this fabulous stream?");

  puts("\n*stream chat*");

  puts("Palagrosdindon: plop la guilde");

  puts("zguegenbronze: psg max");

  puts("Palagrosdindon: si tu bute ton pote j'me sub");

  puts("Kankan776: Omg mais t un trizo");
  puts("*...*");


  puts("\nOkay, now we're getting some good ones. Stay alerted, take note.");
  sleep(3);
  puts("\n*stream sound*");
  puts("- Putin y a un zombie ! AH MAIS NON C'EST TOI !");

  puts("*ourge*");
  puts("*Ding dinG Ding dinG Ding*"); //c'est le bruit de l'xp si tu l'avais pas
  puts("*...*");

  puts("\n\n*stream chat*");
  puts("zguegenbronze: Jme lave le pénis à l'eau bénite");

  puts("Kankan776: T'es qu'un noob de toute facon @Palagrosdindon");

  puts("Kankan776: Ptdrrr comment il est mort");
  puts("Palagrosdindon: ahahahah aller salut");
  puts("*...*");


  puts("\nWe're dealing with a hell of a team. They seem to play by the rules we wrote down..");
  sleep(3);
  ajouter_observation("Kankan776", "This kikoo seems to me to respect several rules of the notebook, to be analyzed in depth.");
  ajouter_observation("zguegenbronze", "High quality Kikoo, not to be approached, very high risk of contamination.");
  ajouter_observation("Palagrosdindon", "Excellent Kikoo troller, beware.");
  puts("\n [+] Three new observations have been added to your notebook.");

}

Lieux* get_lieux(char initiale){
  for(int i = 0 ; i < TINY_ARRAY_SIZE ; i++){
    if(les_lieux_du_kikoo[i].initiale == initiale)
      return &les_lieux_du_kikoo[i];
  }
  return NULL;
}

void lister_les_lieux(){
  for(int i = 0 ; i < TINY_ARRAY_SIZE ; i++){
    if(les_lieux_du_kikoo[i].visite == 1)
      printf("\t#%c : %s\n", les_lieux_du_kikoo[i].initiale, les_lieux_du_kikoo[i].nom);
  }
}

void choisir_lieux(){

  int go_on = 1;
  char choix[8];
  Lieux *lieux = NULL;

  puts("");
  lister_les_lieux();
  puts("Type Q to exit.");
  do{
    printf("> ");
    read_user_str(choix, 4);

    lieux = get_lieux(choix[0]);

    if(choix[0] == 'J' && lieux != NULL && lieux->visite == 1){
      go_on = 0;
      scenario_j();
      lieux->visite = 2;
    }
    else if(choix[0] == 'Y' && lieux != NULL && lieux->visite == 1){
      go_on = 0;
      scenario_y();
      lieux->visite = 2;
    }
    else if(choix[0] == 'T' && lieux != NULL && lieux->visite == 1){
      go_on = 0;
      scenario_t();
      lieux->visite = 2;
    }
    else if(choix[0] == 'Q'){
      go_on = 0;
    }
    else{
      puts("Choice not available.");
    }

  }while(go_on);
}

void lire_les_regles(){

  puts("\nThe Rules of the Holy Kikoo:");
  for(int i = 0 ; i < ARRAY_SIZE && les_regles_du_kikoo[i] != NULL ; i++){
    printf("Rule n°%d: %s\n", (i+1), les_regles_du_kikoo[i]->regle);
  }
}

void introduction(){

  printf(
      "\n\t+---------------------------------------------------------------+\n" \
      "\t| /!\\Warning/!\\                                                 |\n" \
      "\t| The scenarios are based on real facts.                        |\n" \
      "\t| The pseudonyms of the observed kikoos have been modified in   |\n" \
      "\t| order to preserve their anonymity and protect their privacy.  |\n" \
      "\t+---------------------------------------------------------------+\n\t#subtlety\n\n" \
    );
  sleep(3);
  puts("First of all, kikoos are like pokemons. You have to look for them in their natural habitat.\n" \
        "That is, not in the tall grass, but on the internet.");

  lire_les_regles();

  puts("\nThey'll help us identify our first kikoo. I'm not a rocket scientist, so maybe we'll have to add a few rules.\n" \
  "I'm counting on your creativity to help me flesh out my notebook, \"The Rules of the Holy Kikoo.\"");

  puts("I've got a little list of places we could find good kikoo...\n\nWhich one do we start with?");
}

void initialisation(){
  init_buffering();
  creer_regle("A kikoo who has never played Minecraft in his life is not a kikoo.", 1);
  creer_regle("A kikoo has necessarily maintained at least one discussion on the forum jeuxvideo.com.", 1);
  creer_regle("Every self-respecting kikoo has already been banned from an online video game for the reason: Cheat.", 1);
  creer_regle("A kikoo could find his login credentials in database leaks.", 1);
  creer_regle("A kikoo enjoys the annoyance of his friends.", 1);
  creer_lieux(0, "Long-standing topics on jeuxvideo.com.", 1, 'J');
  creer_lieux(1, "Stupid YouTube channels.", 1, 'Y');
  creer_lieux(2, "Minecraft streams on Twitch.", 1, 'T');
  kikoos_observe.n_observation = 0;
}

void choix(){
  printf("\n==What do we do?==\n" \
				 " 1 -> Rereading the rules\n" \
				 " 2 -> Write a rule\n" \
				 " 3 -> We're going hunting\n" \
         " 4 -> View comments\n" \
				 " 9 -> I'm out of here.\n" \
				 "==================\n\n"
	);
}


int main(void){

  char tmp[64];
  int choice;
  int go_on = 1;

  initialisation();
  introduction();
  choisir_lieux();

	while(go_on){
    choix();
		printf("> ");
		choice = read_user_int();

		switch (choice) {
			case 1:
        lire_les_regles();
				break;
			case 2:
        ecrire_regle();
				break;
			case 3:
        choisir_lieux();
				break;
      case 4:
        lire_observations();
  			break;
			case 9:
        go_on = 0;
				break;
			default:
				printf("\nDon't get what you're trying to do, buddy.\n\n");
				break;
		}
	}


  return 0;
}
