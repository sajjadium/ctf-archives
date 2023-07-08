// g++ -g -fstack-protector-all -fno-pie -no-pie main.cpp -o classy

#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <string>

#include <random>

using namespace std;

random_device rd;
mt19937 rng(rd());
uniform_int_distribution<int> rand_uniform(0, 2);

const string wine_answers[3] = {
    "A wine of exceptional stature transcends mere gustatory pleasure, "
    "becoming an ethereal experience that embodies the terroir from which it "
    "originates. It is the harmonious amalgamation of soil, climate, and "
    "meticulous viticulture that imbues a wine with its captivating "
    "complexity. This enigmatic elixir, sculpted by the hands of a skilled "
    "winemaker, weaves together a symphony of flavors, aromas, and textures "
    "that dance upon the palate. Each sip reveals a narrative of time, oak, "
    "and the deft interplay of fruit and acidity. It is in this mysterious "
    "interplay of elements that a wine ascends to the realm of true "
    "exceptionality, enchanting and captivating those fortunate enough to "
    "partake in its enigmatic splendor.",
    "Aging in oak barrels bestows upon wine an exquisite transformation, "
    "elevating it from a mere libation to a work of art. The dance between "
    "wine and oak is a delicate choreography, as the porous wood imparts its "
    "subtle influence upon the liquid it cradles. Over time, the oak infuses "
    "the wine with nuances of vanilla, spice, and a seductive hint of "
    "smokiness. This graceful maturation process allows for the integration of "
    "flavors, the softening of tannins, and the development of a captivating "
    "complexity. The resulting elixir, adorned with the gentle brushstrokes of "
    "the barrel's caress, stands as a testament to the transformative power of "
    "time and oak, offering a sensory journey that is nothing short of "
    "extraordinary.",
    "An intriguing and mysterious wine is a captivating enigma, leaving the "
    "imbiber spellbound by its multifaceted allure. It is the embodiment of "
    "secrets whispered by the vine, concealed within each grape and nurtured "
    "by the terroir that cradles them. This enigmatic elixir reveals itself in "
    "layers, enticing the senses with its beguiling complexity. Its aromas "
    "weave a tale of fruits, flowers, earth, and spice, while its flavors "
    "unfold like a well-crafted narrative, leaving the palate craving more. "
    "The essence of its mystique lies in its ability to elude easy "
    "categorization, offering a tantalizing challenge to the curious imbiber. "
    "In the pursuit of unraveling its secrets, one is rewarded with an "
    "unforgettable sensory journey, where each sip uncovers a new chapter of "
    "its captivating story."};

const string cheese_answers[3] = {
    "An exceptional cheese transcends the realm of mere dairy products, "
    "embodying a sensory masterpiece that echoes the terroir from which it "
    "hails. It is the result of meticulous craftsmanship, where the art of "
    "cheesemaking converges with the nuances of soil, climate, and the unique "
    "qualities of the milk. This harmonious union gives birth to a cheese that "
    "captivates the palate with its symphony of flavors, textures, and aromas. "
    "From the earthy depths of cave-aged varieties to the delicate notes of "
    "grassy freshness in young cheeses, each bite reveals a story of time, "
    "craftsmanship, and the alchemy of fermentation. Truly exceptional cheeses "
    "transport the discerning connoisseur to a world of gastronomic wonder, "
    "where indulgence meets artistry.",
    "Aging is a transformative journey that elevates cheese from a mere curd "
    "to a culinary marvel. Like a voyage through time, the aging process "
    "bestows upon cheese a depth of character and complexity that tantalizes "
    "the senses. Within the controlled embrace of aging cellars, the cheese "
    "undergoes a remarkable metamorphosis. As it matures, flavors deepen, "
    "textures evolve, and an exquisite balance emerges. The interplay of "
    "moisture, temperature, and the unique cultures that inhabit the cheese "
    "contribute to the development of its distinct personality. From the "
    "crumbly crystalline textures of aged cheddars to the silky decadence of "
    "well-aged bloomy rinds, each cheese embodies the culmination of patient "
    "aging, unveiling a world of flavors that is as diverse as it is "
    "captivating.",
    "An intriguing and evocative cheese is a sensory treasure, captivating the "
    "palate with its enigmatic allure. It carries within it the story of its "
    "origin, the terroir it was born from, and the traditions of cheesemaking "
    "that have shaped it. Its aromas transport the connoisseur to rolling "
    "pastures, hidden caves, or alpine meadows, evoking memories of the land "
    "and the animals that contributed their milk. The flavors unfold in a "
    "symphony of taste, revealing layers of complexity, from the subtle "
    "nuttiness of aged cheeses to the lactic tang of fresh varieties. The "
    "textures, too, enchant the senses, ranging from supple and creamy to firm "
    "and crumbly. An intriguing cheese invites exploration, beckoning the "
    "curious palate to embark on a gustatory adventure, where each bite "
    "unravels a new facet of its captivating story."};

string flag;

const string password = "hunter";

class Connoisseur {
public:
  virtual void TalkAboutFlags() = 0;
  void TalkAboutCheese();
  void TalkAboutWine();
};

void Connoisseur::TalkAboutWine() {
  cout << wine_answers[rand_uniform(rng)] << endl;
}

void Connoisseur::TalkAboutCheese() {
  cout << cheese_answers[rand_uniform(rng)] << endl;
}

class LowLevelConnoisseur : public Connoisseur {
public:
  void TalkAboutFlags();
};

void LowLevelConnoisseur::TalkAboutFlags() {

  cout << "Your level of intellectual engagement is undeniably intriguing; "
          "however, regrettably, your grasp of the necessary erudition to "
          "engage in discourse pertaining to flagology appears to be "
          "somewhat deficient."
       << endl;
}

class HighLevelConnoisseur : public Connoisseur {
public:
  void TalkAboutFlags();
};

void HighLevelConnoisseur::TalkAboutFlags() {
  cout << "Behold, in the realm of symbolism, we find a captivating tapestry "
          "unfurled before us. A flag of mesmerizing allure, adorned with "
          "the cryptic inscription "
       << flag
       << ", invites us to embark on an enigmatic journey. This flag, a "
          "visual expression of identity, bears the essence of a selective "
          "community, an elevated echelon that beckons us into the realm of "
          "opulence and privilege."
       << endl;
  cout << flag
       << "encapsulates an enigmatic passphrase that whispers the secrets of "
          "an exclusive enclave. It tantalizes the inquisitive mind, "
          "alluding to an inner circle where societal elevation resides. A "
          "cipher of hidden prestige, it evokes a realm where social strata "
          "intertwine with cultural refinement, offering a glimpse into the "
          "rarified atmosphere of the upper echelons of human existence."
       << endl;
  cout << "Within the fibers of this resplendent standard, a narrative "
          "unfolds, laden with aspirations of grandeur and aspirations of "
          "social ascent. Its vibrant hues weave a tale of aspiration, "
          "promising a world where elegance and refinement reign supreme. "
          "This flag, a beacon of high society, speaks to the pursuit of "
          "sophistication, bespoke experiences, and the embrace of refined "
          "pleasures."
       << endl;
  cout << "As we gaze upon this mesmerizing flag, we are transported to a "
          "dimension where exclusivity intertwines with glamour, and "
          "societal conventions intertwine with whispered secrets. It stirs "
          "our imagination, inviting us to venture beyond the ordinary and "
          "embrace the allure of the extraordinary. "
       << flag
       << ", a key to a world veiled in prestige, invites us to explore the "
          "realms of privilege and indulge in the alluring mystique of high "
          "society."
       << endl;
}

void talk(Connoisseur &con, int choice) {
  switch (choice) {
  case 1:
    con.TalkAboutWine();
    break;
  case 2:
    con.TalkAboutCheese();
    break;
  case 3:
    con.TalkAboutFlags();
    break;
  }
}

struct input_info {
  char text[256];
  HighLevelConnoisseur hCon;
  LowLevelConnoisseur lCon;
};

void handle_input() {
  input_info input;
  int level = 0;
  cout << "What is your Connoisseur level?" << endl;
  cin >> level;
  cin.clear();

  if (level != 1 && level != 2) {
    cout << "Invalid level." << endl;
    return;
  }

  if (level == 2) {
    cout << "Please provide the password:" << endl;

    string user_password;
    cin >> user_password;

    if (user_password != password) {
      cout << "Wrong password." << endl;
      return;
    }
  }

  while (true) {
    cout << "What do you want to talk about?" << endl;
    cout << "[1] Wine" << endl;
    cout << "[2] Cheese" << endl;
    cout << "[3] Flags" << endl;
    cout << "[4] I think I know enough now to be a higher level." << endl;

    int choice = 0;
    cin >> choice;
    cin.clear();

    if (choice == 4) {
      return;
    }
  
    cout << "Now what do you want to tell me?" << endl;
    scanf("%s", input.text);
    if (level == 1) {
      talk(input.lCon, choice);
    } else {
      talk(input.hCon, choice);
    }
  }
}

int main() {
  auto flag_env = getenv("FLAG");
  if (flag_env == NULL) {
    flag = "CSR{not_the_flag}";
  } else {
    flag = string(flag_env);
  }

  while (true) {
    handle_input();
  }
}