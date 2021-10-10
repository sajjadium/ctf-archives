 //abcdefghijklmnopqrstuvwxyz!@#$%^&*()_+-=

int t(int k) {
        int r = rand() % k + 1;
        for (int i = 0; i < r; i++) {
                if (char(k) == 'a') {
                        k = 122;
                        continue;
                }
                k--;
        }
        for (int i = r - 1; i >= 0; i--) {
                if (char(k) == 'z') {
                        k = 97;
                        continue;
                }
                k++;
        }
        return char(k);
}
int l(int k) {
        int e = k;
        for (int i = 0; i < rand() % 1000 + 2; i++) {
                e = (e % 2) ? (((e + 1) / 2) * e) : ((e / 2) * (e + 1));
        }
        return e;
}

string b(int k) {
        vector < char > a;
        a.clear();

        int temp;

        for (int i = 0; k > 0; i++) {
                temp = k % 16;

                if (k % 16 < 10) {
                        a.push_back(temp + 48);
                } else {
                        a.push_back(temp + 87);
                }
                k /= 16;
        }

        string o = "";

        for (int i = a.size() - 1; i >= 0; i--) {
                o += a[i];
        }
        o+=" ";
        return o;
}

int c(int k, int b) {
        int z;
        for (int j = 1; j <= 4; j++) {
                for (int i = 0; i < 50; i++) {
                        if (j % 2 != 0) {
                                k += b;
                        } else {
                                k -= b;
                        }
                }
        }
        return char(k);
}

int main() {
        fstream secret;
        secret.open("secret.txt");

        getline(secret, f);

        for (int i = 0; i < f.size(); i++) {
                f[i] = t(tolower(f[i]));
        }
        secret.close();

        int j = 0, plh;
        string o = "";

        int ar[f.size()];

        for (int j = 0; j < f.size(); j++) {
                ar[j] = rand() % f.size() + 1;
        }

        for (auto i: f) {
                plh=t(i);
                f[j] = c(f[j], ar[j]);
                plh = l(i);
                o += b(plh);
                j++;
        }
        cout << o << endl;
}