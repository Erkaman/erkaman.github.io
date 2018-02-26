#include <stdio.h>
#include <string>
#include <stdlib.h>

int main() {


    std::string s = "";

    int cs[] = {
        // original
        //6, 4, 3, 5 ,4, 6, 8, 7

        // blended
         6, 4, 7, 4, 9, 5, 8, 7

        // non-blended
        //6, 4, 26, 22, 26, 21, 8, 7

        //   21, 24, 26, 22, 26, 21, 23, 28

        //  0,1 ,2, 3, 4, 5, 6, 7

    };
    int n = sizeof(cs) / sizeof(cs[0]);

    s += "convert -size ";
    s += std::to_string(n * 100) + "x100 xc:skyblue";

    for(int i = 0; i < n; ++i) {
        int g = (int)((cs[i] / 30.0) * 255.0f);

        s += " -fill 'gray(" + std::to_string(g) + ")'";

        int xs = (i+0) * 100;
        int xe = (i+1)* 100;

        s += " -draw \"rectangle " + std::to_string(xs) +",0 " + std::to_string(xe) + ",100\"";
    }
    s += " draw.png";

//    printf("%s\n",s.c_str());
    system(s.c_str());

}
