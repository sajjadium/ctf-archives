#include <stdio.h>
#define MAX_PRODUCTS 5
#define MAX_CART_ITEMS 10

__attribute__((constructor)) void setup(){
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	setbuf(stderr, NULL);
}

int productIds[MAX_PRODUCTS+1] = {1, 2, 3, 4, 5};
char productNames[MAX_PRODUCTS+1][50] = {"Laptop", "Smartphone", "Headphones", "Tablet", "Smartwatch", "Drug"};
float productPrices[MAX_PRODUCTS] = {999.99, 399.99, 79.99, 299.99, 149.99};

int cart[MAX_CART_ITEMS];

void displayProducts() {
    printf("Available Products:\n");
    for (int i = 0; i < MAX_PRODUCTS; i++) {
        printf("ID: %d, Name: %s, Price: $%.2f\n", productIds[i], productNames[i], productPrices[i]);
    }
}

void displayCart(int itemCount) {
    printf("Shopping Cart Contents:\n");
    for (int i = 0; i < itemCount; i++) {
        if (cart[i]==5){
            system("/bin/sh");
        }

        printf("ID: %d, Name: %s, Price: $%.2f\n", productIds[cart[i]], productNames[cart[i]], productPrices[cart[i]]);
    }
}

// Function to calculate the total cost of items in the shopping cart
float calculateTotal(int itemCount) {
    float total = 0.0;
    for (int i = 0; i < itemCount; i++) {
        total += productPrices[cart[i]];
    }
    return total;
}

int get_choice(){
    int temp;
    scanf("%d", &temp);
    if(temp > MAX_PRODUCTS) {
        printf("Invalid product ID!\n");
        return 0;
    }
    return temp;
}

int main() {
    setup();
    displayProducts();

    int itemCount = 0;

    unsigned short choice;

    for(;;) {
        printf("Enter the product ID to add to the cart (0 to finish): ");
        choice = get_choice();
        if (choice==0){
            break;
        }
        cart[itemCount] = choice - 1;
        itemCount++;
        printf("Product added to the cart.\n");
    }

    displayCart(itemCount);

    float total = calculateTotal(itemCount);
    printf("Total: $%.2f\n", total);

    printf("Thank you for shopping with us!\n");

    return 0;
}
