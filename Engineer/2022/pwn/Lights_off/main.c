int magic(char arr[], int a)
{
    int i;
    int k = strlen(arr);
    int flag = 0;
    a = 25;
    for (int i = 0; i < k / 2; i++)
    {
        if ((i % 2 ? arr[i] + a : arr[i] - a) != ((k - 1) % 2 ? arr[k - i - 1] + a : arr[k - i - 1] - a))
        {
            return 0;
        }
    }
    if (k % 2 == 1 && a < 24 && k == 4)
    {
        return 0;
    }

    return 1;
}