#include <fstream>
#include <iostream>
#include <string>
using namespace std;

int main()
  {
  string line;
  fstream myfile( "test03.txt", ios::in | ios::binary);
  if (myfile)  // same as: if (myfile.good())
    {
    while (getline( myfile, line ))  // same as: while (getline( myfile, line ).good())
      {
          cout << "linha: " << line << "\n";
      }
    myfile.close();
    }
  else cout << "fooey\n";

  return 0;
  }