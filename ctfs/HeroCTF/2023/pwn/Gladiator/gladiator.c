// gcc -no-pie -Wl,-z,norelro -o gladiator gladiator.c -lpthread

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <stdarg.h>
#include <pthread.h>
#include <string.h>

/*********** STRUCTURES ***********/

typedef struct
{
    int64_t hp;
    void (*spell)(int64_t *, int64_t);
    void **object;
    void (*exit)(int64_t *);
} gladiator_t;

typedef struct
{
    int64_t hp;
    void (*spell)(int64_t *, int64_t);
    void (*object)(void *);
} npc_t;

typedef struct
{
    int64_t hp;
    pthread_mutex_t mutex;
    pthread_cond_t cond;
    void (*spell)(int64_t *);
} character_t;

typedef struct
{
    int64_t hp;
    void (*spell)(gladiator_t *);
} god_t;

typedef struct
{
    int64_t bags_nb;
    size_t grams;
    void (*magic)(void *);
} perlimpinpin_t;

typedef struct thread_arg
{
    gladiator_t *gladiator;
    npc_t *npc;
    character_t *witch;
    character_t *night_king;
    god_t *god;
} thread_arg;

typedef struct
{
    int64_t zombified_gladiator_nb;
    void **army;
} thread_army_t;

typedef struct
{
    pthread_mutex_t mutex_fight;
    pthread_cond_t cond_fight_level_1;
    pthread_cond_t cond_fight_level_2;
    pthread_cond_t cond_fight_level_3;
    pthread_cond_t cond_fight_level_4;
} arena_fight_t;

static arena_fight_t arena_fight =
    {
        .mutex_fight = PTHREAD_MUTEX_INITIALIZER,
        .cond_fight_level_1 = PTHREAD_COND_INITIALIZER,
        .cond_fight_level_2 = PTHREAD_COND_INITIALIZER,
        .cond_fight_level_3 = PTHREAD_COND_INITIALIZER,
        .cond_fight_level_4 = PTHREAD_COND_INITIALIZER};

/*********** UTILS ***********/
int fflushed_printf(const char *format, ...)
{
    va_list args;
    int ret;

    va_start(args, format);
    ret = vprintf(format, args);

    va_end(args);
    fflush(stdout);

    return ret;
}

/*********** ACTIONS ***********/
void hit(int64_t *hp)
{
    *hp -= 1;
}

void flurry_of_blows(int64_t *hp, int64_t k)
{
    for (int i = 0; i < k; i++)
    {
        hit(hp);
    }
}

void feigning_death(int64_t *hp)
{
    fflushed_printf("\n[+] You fake death...\n");
    fflushed_printf("[-] But your opponent kills you.\n");
    *hp = 0;
    pthread_exit(NULL);
}

void uno_reverse_card(void *reverse_card)
{
    fflushed_printf("\n[+] UNO Reverse !\n");
    pthread_cond_signal(reverse_card);
}

void sharp_blade(int64_t *hp, int64_t damage)
{
    *hp -= damage;
}

void avada_kedavra(int64_t *hp)
{
    *hp = (-1337);
}

void god_power(gladiator_t *gladiator)
{
    gladiator->hp = 0;
    free(gladiator);
}

/*********** CREATIONS ***********/

gladiator_t *create_gladiator(int64_t hp, void (*spell)(int64_t *, int64_t))
{
    gladiator_t *gladiator = (gladiator_t *)malloc(sizeof(gladiator_t));
    gladiator->hp = hp;
    gladiator->spell = spell;
    gladiator->exit = feigning_death;
    return gladiator;
}

npc_t *create_npc(int64_t hp, void (*spell)(int64_t *, int64_t))
{
    npc_t *random_npc = (npc_t *)malloc(sizeof(npc_t));
    random_npc->hp = hp;
    random_npc->spell = spell;
    random_npc->object = uno_reverse_card;
    return random_npc;
}

character_t *create_character(int64_t hp, void (*spell)(int64_t *))
{
    character_t *character = (character_t *)malloc(sizeof(character_t));
    character->hp = hp;
    character->spell = spell;
    return character;
}

god_t *create_god(int64_t hp, void (*spell)(gladiator_t *))
{
    god_t *god = (god_t *)malloc(sizeof(god_t));
    god->hp = hp;
    god->spell = spell;
    return god;
}

void menu()
{
    fflushed_printf("\n========= ACTIONS =========\n");
    fflushed_printf("1) Hit\n");
    fflushed_printf("2) Fluuuuurrry of bloooows!\n");
    fflushed_printf("3) Exit\n");
    fflushed_printf("\n>>> Your choice: ");
}

void menu2()
{
    fflushed_printf("\n========= ACTIONS =========\n");
    fflushed_printf("1) Hit\n");
    fflushed_printf("2) Fluuuuurrry of bloooows!\n");
    fflushed_printf("3) Use your object\n");
    fflushed_printf("4) Exit\n");
    fflushed_printf("\n>>> Your choice: ");
}

void menu3()
{
    fflushed_printf("\n========= ENCHANT YOUR OBJECT =========\n");
    fflushed_printf("1) Add an enchantment\n");
    fflushed_printf("2) Remove an enchantment\n");
    fflushed_printf("3) Check enchantments\n");
    fflushed_printf("4) End of enchantments \n");
    fflushed_printf("\n>>> Your choice: ");
}

void menu4()
{
    fflushed_printf("\n========= COMMANDMENTS =========\n");
    fflushed_printf("1) Take a page for a commandment \n");
    fflushed_printf("2) Rewrite a commandment \n");
    fflushed_printf("3) Delete what I wrote \n");
    fflushed_printf("4) Check what I wrote before \n");
    fflushed_printf("\n>>> Your choice: ");
}

void menu_object_level2()
{
    fflushed_printf("\n===== Objects =====\n");
    fflushed_printf("1) HP potion\n");
    fflushed_printf("2) Sharp blade\n");
    fflushed_printf("3) Perlimpinpin bags\n");
    fflushed_printf("\n>>> Your choice: ");
}

void menu_object_level3()
{
    fflushed_printf("\n======= Objects =======\n");
    fflushed_printf("1) Magic wand\n");
    fflushed_printf("2) Book of spells\n");
    fflushed_printf("3) Potion of invisibility\n");
    fflushed_printf("\n>>> Your choice: ");
}

void check_death(gladiator_t *gladiator)
{
    if (gladiator->hp <= 0)
    {
        fflushed_printf("\n[-] You died...\n");
        exit(0);
    }
}

int choose_object_level2(gladiator_t *gladiator)
{
    int64_t nb_bags = 0;

    while (1)
    {
        int choice;
        menu_object_level2();
        scanf("%d", &choice);
        getchar();

        if (choice > 0 && choice <= 3)
        {

            switch (choice)
            {
            case 1:
                gladiator->hp = 1337;
                break;
            case 2:
                gladiator->spell = sharp_blade;
                break;
            case 3:
                int64_t nb;
                size_t grams;
                void **bag_of_bags;

                while (1)
                {

                    fflushed_printf(">>> You can take up to 10 bags, how many do you want? ");
                    scanf("%ld", &nb);
                    getchar();

                    if (nb > 0 && nb <= 10)
                    {
                        bag_of_bags = malloc(nb * sizeof(void *));

                        for (int64_t i = 0; i < nb; i++)
                        {

                            while (1)
                            {
                                fflushed_printf(">>> How many grams do you want in the bag %ld ? ", i);
                                scanf("%zu", &grams);
                                getchar();

                                if (grams >= 1 && grams <= 100)
                                {
                                    bag_of_bags[i] = malloc(grams);

                                    perlimpinpin_t *bag = (perlimpinpin_t *)bag_of_bags[i];
                                    bag->bags_nb = i;
                                    bag->grams = grams;

                                    break;
                                }
                                else
                                {
                                    fflushed_printf("[!] A bag can only contain between 1 and 100 grams\n");
                                }
                            }
                        }

                        nb_bags = nb;

                        break;
                    }
                    else
                    {
                        fflushed_printf("[-] You should take at least 1 bag (max is 10)\n");
                    }
                }

                gladiator->object = bag_of_bags;

                break;

            default:
                fflushed_printf("[-] Invalid choice.\n");
            }
            break;
        }
        else
        {
            fflushed_printf("[!] Choose an option beetween 1 and 3\n");
        }
    }
    return nb_bags;
}

void *casting_avada_kedavra(void *args)
{
    character_t *witch = (character_t *)args;
    pthread_cond_wait(&witch->cond, &witch->mutex);
    witch->spell(&witch->hp);
}

int choose_object_level3(gladiator_t *gladiator)
{
    int choice, size;

    while (1)
    {
        menu_object_level3();
        scanf("%d", &choice);
        getchar();

        if (choice > 0 && choice <= 3)
        {

            switch (choice)
            {
            case 1:
                fflushed_printf("[+] Magic wand\n");
                size = 100;
                gladiator->object = (void **)malloc(size);
                break;

            case 2:
                fflushed_printf("[+] Book of spells\n");
                size = 200;
                gladiator->object = (void **)malloc(size);
                break;

            case 3:
                fflushed_printf("[+] Potion of invisibility\n");
                size = 60;
                gladiator->object = (void **)malloc(size);
                break;

            default:
                fflushed_printf("[-] Invalid choice.\n");
            }
            break;
        }
        else
        {
            fflushed_printf("[!] Choose an option beetween 1 and 3\n");
        }
    }
    sleep(1);

    return size;
}

void level3_actions(gladiator_t *gladiator, int object_size)
{
    int choice, index;
    int nb_enchants, enchant_size, nb_enchants_max;
    nb_enchants_max = (int)(object_size / 8);
    size_t sizes[nb_enchants_max];

    while (1)
    {

        menu3();
        scanf("%d", &choice);
        getchar();

        if(choice == 4){
            fflushed_printf("\n[-] End of enchantment.\n");
            break;
        }

        switch (choice)
        {
        case 1:

            if (nb_enchants == nb_enchants_max)
            {
                fflushed_printf("\n[!] You can't enchant any more.\n");
                break;
            }
            else
            {
                fflushed_printf("\n[+] Enter the enchant index: ");
                scanf("%d", &index);
                getchar();

                if (index >= 0 && index < nb_enchants_max)
                {
                    fflushed_printf("\n[+] Enter the enchant size: ");
                    scanf("%d", &enchant_size);
                    getchar();

                    if (enchant_size >= 0 && enchant_size < 2000)
                    {
                        void **object = gladiator->object;
                        object[index] = malloc(enchant_size);
                        sizes[index] = enchant_size;

                        fflushed_printf("[+] Enter your spell: ");
                        fgets(object[index], sizes[index], stdin);
                        ((char *)object[index])[strcspn((char *)object[index], "\n")] = '\0';

                        nb_enchants++;
                    }
                    else
                    {
                        fflushed_printf("\n[-] Invalid enchant size\n");
                    }
                }
                else
                {
                    fflushed_printf("\n[-] Invalid index\n");
                }
            }
            break;

        case 2:

            if (nb_enchants == 0)
            {
                fflushed_printf("\n[!] You have no enchants.\n");
                break;
            }
            else
            {
                fflushed_printf("\n[+] Enter the enchant index: ");
                scanf("%d", &index);
                getchar();

                if (index >= 0 && index < nb_enchants_max)
                {
                    void **object = gladiator->object;
                    if (object[index] != NULL)
                        free(object[index]);

                    nb_enchants--;
                }
                else
                {
                    fflushed_printf("\n[-] Invalid index\n");
                }
            }
            break;

        case 3:

            if (nb_enchants == 0)
            {
                fflushed_printf("\n[!] You have no enchants.\n");
                break;
            }
            else
            {
                fflushed_printf("\n[+] Enter the enchant index: ");
                scanf("%d", &index);
                getchar();

                if (index >= 0 && index < nb_enchants_max)
                {
                    fflushed_printf("[+] You read the enchant: ");
                    fwrite(gladiator->object[index], sizeof(char), sizes[index], stdout);
                }
                else
                {
                    fflushed_printf("\n[-] Invalid index\n");
                }
            }
            break;

        default:
            fflushed_printf("\n[-] Invalid choice.\n");
            break;
        }
    }
}

void level4_actions(gladiator_t *gladiator)
{
    int choice, index;

    int action;
    int size;
    int big_page = 1;

    int max_actions = 10;
    int max_size = 0x68;

    char *pages[max_actions];
    size_t sizes[max_actions];

    while (1)
    {
        if (action == max_actions)
        {
            fflushed_printf("\n[!] You used your 10 tries\n");
            break;
        }
        menu4();
        scanf("%d", &choice);
        getchar();

        switch (choice)
        {
        case 1:

            fflushed_printf("\n[+] Enter the page index that you want to write to: ");
            scanf("%d", &index);
            getchar();
            if (index >= 0 && index < max_actions)
            {
                fflushed_printf("\n[+] Enter the size of the commandment: ");
                scanf("%d", &size);
                getchar();
                if(size==0x418 && big_page)
                {
                    pages[index] = (char *)malloc(size);
                    sizes[index] = size;
                    fflushed_printf("\n[+] (God): Not this one!");
                    big_page = 0;
                }
                else if (size >= 0 && size <= max_size)
                {
                    pages[index] = (char *)malloc(size);
                    sizes[index] = size;
                    fflushed_printf("\n[+] New page for commandment");
                }
                else
                {
                    fflushed_printf("\n[-] Invalid size\n");
                }

                action++;
            }
            else
            {
                fflushed_printf("\n[-] Invalid index\n");
            }

            break;

        case 2:

            fflushed_printf("\n[+] Enter the page index to rewrite: ");
            scanf("%d", &index);
            getchar();

            if (index >= 0 && index < max_actions)
            {
                fflushed_printf("\n[+] Write the commandment");
                fgets(pages[index], sizes[index], stdin);

                ((char *)pages[index])[strcspn((char *)pages[index], "\n")] = '\0';
                fflushed_printf("\n[+] Commandment has been written !");
                break;
            }
            else
            {
                fflushed_printf("\n[-] Invalid index\n");
            }

            break;

        case 3:

            fflushed_printf("\n[+] Enter index page to delete: ");
            scanf("%d", &index);
            getchar();

            if (index >= 0 && index < max_actions)
            {
                if (pages[index] != NULL)
                    free(pages[index]);
                fflushed_printf("[+] Page deleted!");
                break;
            }
            else
            {
                fflushed_printf("\n[-] Invalid index\n");
            }

            action++;
            break;

        case 4:

            fflushed_printf("\n[+] Enter index page to read: ");
            scanf("%d", &index);
            getchar();

            if (index >= 0 && index < max_actions)
            {
                fflushed_printf("[+] You read the content: ");
                fwrite(pages[index], sizeof(char), sizes[index], stdout);
                break;
            }
            else
            {
                fflushed_printf("\n[-] Invalid index\n");
            }

            break;

        default:
            fflushed_printf("\n[-] Invalid choice.\n");
            break;
        }
    }
}

void *create_zombified_gladiator(void *args)
{
    thread_army_t *targ = (thread_army_t *)args;
    int64_t zombified_gladiator_nb = targ->zombified_gladiator_nb;
    void **army = targ->army;

    gladiator_t *zombified_gladiator = (gladiator_t *)malloc(sizeof(gladiator_t));
    zombified_gladiator->hp = 800;

    army[zombified_gladiator_nb] = zombified_gladiator;
}

thread_army_t invocation_army_of_the_dead(character_t *night_king)
{
    void **army;
    army = malloc(10 * sizeof(void *));
    int64_t zombified_gladiator_nb = 0;
    thread_army_t thread_army;

    while (1)
    {

        if (night_king->hp <= 0 || zombified_gladiator_nb == 10)
        {
            fflushed_printf("[!] End invocation\n");
            break;
        }
        else
        {

            zombified_gladiator_nb++;

            thread_army.zombified_gladiator_nb = zombified_gladiator_nb;
            thread_army.army = army;
            pthread_t zombified_gladiator_creation;
            int err = pthread_create(&zombified_gladiator_creation, NULL, create_zombified_gladiator, &thread_army);
            if (err)
            {
                fflushed_printf("[-] Error creating second thread: %d\n", err);
                exit(EXIT_FAILURE);
            }

            pthread_cancel(zombified_gladiator_creation);
            fflushed_printf("[!] A zombified gladiator appeared !\n");

            sleep(1.5);
        }
    }

    return thread_army;
}

void *level_1(void *args)
{
    thread_arg *targ = (thread_arg *)args;
    gladiator_t *gladiator = targ->gladiator;
    npc_t *npc = targ->npc;

    int choice, k;

    fflushed_printf("\n[+] You enter the first arena. Your fight is against a random NPC !\n");

    pthread_cond_signal(&arena_fight.cond_fight_level_1);

    fflushed_printf("\n[+] Fight !\n");
    fflushed_printf("[+] Current HP: %ld\n", gladiator->hp);

    while (1)
    {
        menu();
        scanf("%d", &choice);
        getchar();

        if (choice > 0 && choice <= 3)
        {

            switch (choice)
            {
            case 1:
                gladiator->spell(&npc->hp, 1);
                break;
            case 2:
                fflushed_printf(">>> How many blows ? ");
                scanf("%d", &k);
                getchar();

                if (k <= 20)
                {
                    gladiator->spell(&npc->hp, k);
                }
                else
                {
                    fflushed_printf("[-] Max blows number is 20\n");
                }

                break;
            case 3:
                gladiator->exit(&gladiator->hp);
                break;

            default:
                fflushed_printf("[-] Invalid choice. Try again.\n");
                break;
            }
            sleep(1);
        }
        else
        {
            fflushed_printf("[-] Choose an option beetween 1 and 3\n");
        }
    }

    return NULL;
}

void *level_2(void *args)
{
    thread_arg *targ = (thread_arg *)args;
    gladiator_t *gladiator = targ->gladiator;

    /*********** CREATE NPC ***********/
    npc_t *npc = create_npc(40, flurry_of_blows);

    thread_arg prepare_fighter = {gladiator, npc, NULL, NULL, NULL};

    /*********** STARTING FIGHT ***********/
    pthread_t sixth_thread;
    int err = pthread_create(&sixth_thread, NULL, level_1, &prepare_fighter);
    if (err)
    {
        fflushed_printf("[-] Error creating second thread: %d\n", err);
        exit(EXIT_FAILURE);
    }

    pthread_mutex_lock(&arena_fight.mutex_fight);
    pthread_cond_wait(&arena_fight.cond_fight_level_1, &arena_fight.mutex_fight);
    pthread_mutex_unlock(&arena_fight.mutex_fight);

    /*********** NPC ACTIONS ***********/

    while (gladiator->hp > 0 && npc->hp >= 0)
    {
        sleep(1.5);
        npc->spell(&gladiator->hp, 1);

        if (!(npc->hp <= 0))
        {
            npc->hp += 10;
        }
    }

    /*********** CHECK IF GLADIATOR STILL ALIVE ***********/
    check_death(gladiator);

    if (npc->hp < 0)
    {
        fflushed_printf("\n[+] The random NPC is dead!\n");
        pthread_cancel(sixth_thread);
    }

    /*********** NPC GIVES UP THE GOST ***********/
    free(npc);

    /*********** LEVEL 2 ***********/
    fflushed_printf("\n[+] You had luck ! You can win one arena, but not two.\n");
    fflushed_printf("\n[+] You enter the second arena. Your fight is against a witch !\n");
    character_t *witch = targ->witch;

    /*********** NEW OBJECT ***********/
    fflushed_printf("[+] To prepare yourself for this fight, you can take one of the following objects:\n");

    int64_t nb_bags = choose_object_level2(gladiator);

    /*********** GLADIATOR STARTING FIGHT ***********/
    pthread_cond_signal(&arena_fight.cond_fight_level_2);

    fflushed_printf("\n[+] Fight !\n");
    fflushed_printf("[+] Current HP: %ld\n", gladiator->hp);

    int choice, k;

    while (1)
    {
        menu2();
        scanf("%d", &choice);
        getchar();

        if (choice > 0 && choice <= 4)
        {

            switch (choice)
            {
            case 1:
                gladiator->spell(&witch->hp, 1);
                break;
            case 2:
                fflushed_printf(">>> How many blows ??? ");
                scanf("%d", &k);
                getchar();

                if (k <= 20)
                {
                    gladiator->spell(&witch->hp, k);
                }
                else
                {
                    fflushed_printf("[-] Max blows number is 20\n");
                }

                break;
            case 3:

                void **bag_perlimpinpin_powder = gladiator->object;
                int64_t bag_nb;

                fflushed_printf("[+] Choose a bag of perlimpinpin powder between 0 and %ld: ", nb_bags - 1);

                while (1)
                {
                    scanf("%ld", &bag_nb);
                    getchar();

                    if (bag_nb >= 0 && bag_nb < nb_bags)
                    {
                        fflushed_printf("[+] You throw your perlimpinpin powder on the witch!\n");
                        ((perlimpinpin_t *)bag_perlimpinpin_powder[bag_nb])->magic(&witch->cond);
                        break;
                    }
                    else
                    {
                        fflushed_printf("[-] Choose an existing perlimpinpin bag.\n");
                    }
                }

                break;
            case 4:
                gladiator->exit(&gladiator->hp);
                break;

            default:
                fflushed_printf("[-] Invalid choice. Try again.\n");
                break;
            }
            sleep(1);
        }
        else
        {
            fflushed_printf("[-] Choose an option beetween 1 and 4\n");
        }
    }

    pthread_join(sixth_thread, NULL);
    return NULL;
}

void *level_3(void *args)
{
    thread_arg *targ = (thread_arg *)args;
    gladiator_t *gladiator = targ->gladiator;

    /*********** CREATE WITCH ***********/
    character_t *witch = create_character(400, avada_kedavra);

    if (pthread_mutex_init(&witch->mutex, NULL) != 0)
    {
        fflushed_printf("\n[-] Mutex init failed\n");
        exit(0);
    }

    if (pthread_cond_init(&witch->cond, NULL) != 0)
    {
        fflushed_printf("\n[-] Cond init failed\n");
        exit(0);
    }

    thread_arg prepare_fighter = {gladiator, NULL, witch, NULL, NULL};

    /*********** STARTING FIGHT ***********/
    pthread_t fifth_thread;
    int err = pthread_create(&fifth_thread, NULL, level_2, &prepare_fighter);
    if (err)
    {
        fflushed_printf("[-] Error creating second thread: %d\n", err);
        exit(EXIT_FAILURE);
    }

    pthread_mutex_lock(&arena_fight.mutex_fight);
    pthread_cond_wait(&arena_fight.cond_fight_level_2, &arena_fight.mutex_fight);
    pthread_mutex_unlock(&arena_fight.mutex_fight);

    /*********** WITCH ACTIONS ***********/

    fflushed_printf("[!] The witch is preparing a spell!\n");
    pthread_t casting_thread;
    int err2 = pthread_create(&casting_thread, NULL, casting_avada_kedavra, witch);
    if (err2)
    {
        fflushed_printf("[-] Error creating casting_thread: %d\n", err2);
        exit(EXIT_FAILURE);
    }

    sleep(4);

    if (witch->hp > 0)
    {
        fflushed_printf("\n[!] (Witch): Avada kedavraaaaa !!!\n");
        witch->spell(&gladiator->hp);
    }

    check_death(gladiator);

    if (witch->hp <= 0)
    {
        fflushed_printf("\n[+] The witch is dead!\n");
        pthread_cancel(fifth_thread);
    }

    free(witch);

    /*********** LEVEL 3 ***********/
    fflushed_printf("\n[+] You had luck two times, but not three.\n");
    fflushed_printf("\n[+] You enter the third arena. Your fight is against the Night King !\n");

    character_t *night_king = targ->night_king;

    /*********** NEW OBJECT ***********/
    fflushed_printf("[+] To prepare yourself for this fight, you can take one of the following objects:\n");
    int object_size = choose_object_level3(gladiator);

    /*********** GLADIATOR STARTING FIGHT ***********/
    pthread_cond_signal(&arena_fight.cond_fight_level_3);

    fflushed_printf("\n[+] Fight !\n");
    fflushed_printf("[+] Current HP: %ld\n", gladiator->hp);

    level3_actions(gladiator, object_size);

    pthread_join(fifth_thread, NULL);
    return NULL;
}

void *level_4(void *args)
{
    int choice;
    thread_arg *targ = (thread_arg *)args;
    gladiator_t *gladiator = targ->gladiator;

    /*********** CREATE NIGHT KING ***********/
    character_t *night_king = create_character(80000, avada_kedavra);

    thread_arg prepare_fighter = {gladiator, NULL, NULL, night_king, NULL};

    /*********** STARTING FIGHT ***********/
    pthread_t third_thread;
    int err = pthread_create(&third_thread, NULL, level_3, &prepare_fighter);
    if (err)
    {
        fflushed_printf("[-] Error creating second thread: %d\n", err);
        exit(EXIT_FAILURE);
    }

    /*********** WAITING FIGHT ***********/
    pthread_mutex_lock(&arena_fight.mutex_fight);
    pthread_cond_wait(&arena_fight.cond_fight_level_3, &arena_fight.mutex_fight);
    pthread_mutex_unlock(&arena_fight.mutex_fight);

    /*********** NIGHT KING ACTIONS ***********/
    fflushed_printf("\n[+] The king seems already dead !\n");
    free(night_king);

    thread_army_t thread_army = invocation_army_of_the_dead(night_king);
    if (thread_army.zombified_gladiator_nb == 10)
    {
        fflushed_printf("\n[!] Zombie gladiators are coming for you!\n");
        gladiator->hp = 0;
        check_death(gladiator);
    }
    else
    {
        for (int i = 1; i < thread_army.zombified_gladiator_nb; i++)
        {
            free(thread_army.army[i]);
        }
        fflushed_printf("[!] The army disapeared !\n");
        pthread_cancel(third_thread);
    }

    /*********** NIGHT KING DISAPEARED WITH HIS ARMY ***********/

    /*********** LEVEL 4 ***********/
    fflushed_printf("\n[+] Ok three times, but this time, you can pray to God, he won't save you.\n");
    fflushed_printf("[+] And no loots for you this time. Anyways you can't win this time.\n");
    fflushed_printf("[+] You enter the fourth arena. Your fight is against... \n");
    god_t *god = targ->god;

    fflushed_printf("\n[+] A dazzling light comes from the sky... \n");

    pthread_cond_signal(&arena_fight.cond_fight_level_4);

    fflushed_printf("\n[+] Fight !\n");
    fflushed_printf("[+] Current HP: %ld\n", gladiator->hp);

    level4_actions(gladiator);

    pthread_join(third_thread, NULL);
    return NULL;
}

int main()
{
    fflushed_printf("  +-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+-=-=-=-=-=-=-=-+\n");
    fflushed_printf(" /                               Welcome, Gladiator!                               \\\n");
    fflushed_printf("/                                                                                   \\\n");
    fflushed_printf("\\    To get the victory, you will have to fight and win in 4 different arenas.      /\n");
    fflushed_printf(" \\   Good luck, you will need it, and don't forget: all is fair in love and war.   /\n");
    fflushed_printf("  +-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+-=-=-=-=-=-=-=-+\n\n");

    /*********** CREATE GLADIATOR ***********/
    gladiator_t *gladiator = create_gladiator(10, flurry_of_blows);
    god_t *god = create_god(7500000000, god_power);

    thread_arg prepare_fighter = {gladiator, NULL, NULL, NULL, god};

    /*********** CREATE LEVELS ***********/
    pthread_t first_thread;
    int err = pthread_create(&first_thread, NULL, level_4, &prepare_fighter);
    if (err)
    {
        fflushed_printf("[-] Error creating first thread: %d\n", err);
        exit(EXIT_FAILURE);
    }

    /*********** WAITING FIGHT ***********/
    pthread_mutex_lock(&arena_fight.mutex_fight);
    pthread_cond_wait(&arena_fight.cond_fight_level_4, &arena_fight.mutex_fight);
    pthread_mutex_unlock(&arena_fight.mutex_fight);

    fflushed_printf("\n[+] (God): Who dares to disturb and confront me? \n");

    /*********** GOD ACTIONS ***********/
    fflushed_printf("[+] (God): For your final moments, I give you a book to write the 10 Commandments.\n");
    fflushed_printf("[+] (God): You have only 10 tries, I don't have your time.\n");

    sleep(100);
    fflushed_printf("[!] (God): Ok, stop, I'm too lazy to wait.");
    god->spell(gladiator);

    check_death(gladiator);

    fflushed_printf("\nIt's impossible to win all the arenas :)\n");

    pthread_join(first_thread, NULL);

    return 0;
}
