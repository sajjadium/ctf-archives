#include <iostream>
#include <vector>
#include <algorithm>

int binarySearch(const std::vector<int>& arr, int target) {
    int left = 0, right = arr.size() -1;
    while(left <= right){
        int mid = left + (right - left) /2;
        if(arr[mid] == target)
            return mid;
        if(arr[mid] < target)
            left = mid +1;
        else
            right = mid -1;
    }
    return -1;
}

int main(){
    std::vector<int> data = {2, 3, 4, 10, 40};
    int target = 10;
    std::sort(data.begin(), data.end());
    int result = binarySearch(data, target);
    if(result != -1)
        std::cout << "Element found at index " << result << std::endl;
    else
        std::cout << "Element not found" << std::endl;
    return 0;
}
