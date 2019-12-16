#include <iostream>
#include <cmath>

using namespace std;

void apply_gravity(int* a, int* b) {
    int x,y,z;
    x = 1 + (*a > *b) * -2 + (*a == *b) * -1;
    y = 1 + (*(a+1) > *(b+1)) * -2 + (*(a+1) == *(b+1)) * -1;
    z = 1 + (*(a+2) > *(b+2)) * -2 + (*(a+2) == *(b+2)) * -1;
    *(a + 3) += x;
    *(a + 4) += y;
    *(a + 5) += z;
    *(b + 3) -= x;
    *(b + 4) -= y;
    *(b + 5) -= z;
}

uint64_t repeats(int field) {
    int moons[24]{ 14,9,14, 0,0,0, 9,11,6, 0,0,0, -6,14,-4, 0,0,0, 4,-4,-3, 0,0,0};
    // int moons[24]{-1,0,2,0,0,0,2,-10,-7,0,0,0,4,-8,8,0,0,0,3,5,-1,0,0,0};
    int current_energy = 0;

    for(uint64_t step = 1; step < 5000000000; ++step) {
        // for(int i = 0; i < 24; ++i) {
        //     cout << moons[i] << " ";
        // }
        // cout << endl;
        apply_gravity(moons, moons + 6);
        apply_gravity(moons, moons + 12);
        apply_gravity(moons, moons + 18);
        apply_gravity(moons + 6, moons + 12);
        apply_gravity(moons + 6, moons + 18);
        apply_gravity(moons + 12, moons + 18);
        for(int moon = 0; moon < 24; moon += 6) {
            moons[moon] += moons[moon + 3];
            moons[moon + 1] += moons[moon + 4];
            moons[moon + 2] += moons[moon + 5];
        }
        current_energy = 0;
        for(int moon = 0; moon < 24; moon += 6) {
            current_energy += (abs(moons[moon + field])) * (abs(moons[moon + field + 3]));
        }
        if(current_energy == 0) {
            return step;
        }
    }
}

int main() {
    uint64_t x = repeats(0);
    uint64_t y = repeats(1);
    uint64_t z = repeats(2);
    cout << x << " " << y << " " << z << endl;
    cout << (x * y * z) << endl;
}