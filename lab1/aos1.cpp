#include <iostream>
#include <time.h>
#include <vector>


#define TIMER 10000000

using namespace std;

template <typename T>
double getTime(char oper, T a, T b)
{
	clock_t start, stop;
	T c;
	if (oper == '+') {
		start = clock();
		for (int i = 0; i < TIMER; i++) {
			c = a + b;
			c = a + b;
			c = a + b;
			c = a + b;
			c = a + b;
			c = a + b;
			c = a + b;
			c = a + b;
			c = a + b;
			c = a + b;
		}
		stop = clock();
	}
	else if (oper == '-') {
		start = clock();
		for (int i = 0; i < TIMER; i++) {
			c = a - b;
			c = a - b;
			c = a - b;
			c = a - b;
			c = a - b;
			c = a - b;
			c = a - b;
			c = a - b;
			c = a - b;
			c = a - b;
		}
		stop = clock();
	}
	else if (oper == '*') {
		start = clock();
		for (int i = 0; i < TIMER; i++) {
			c = a * b;
			c = a * b;
			c = a * b;
			c = a * b;
			c = a * b;
			c = a * b;
			c = a * b;
			c = a * b;
			c = a * b;
			c = a * b;
		}
		stop = clock();
	}
	else {
		start = clock();
		for (int i = 0; i < TIMER; i++) {
			c = a / b;
			c = a / b;
			c = a / b;
			c = a / b;
			c = a / b;
			c = a / b;
			c = a / b;
			c = a / b;
			c = a / b;
			c = a / b;
		}
		stop = clock();
	}

	clock_t loop_start = clock();
	for (int i = 0; i < TIMER; i++) {
	}
	clock_t loop_stop = clock();

	return (double)(stop - start + loop_start - loop_stop) / CLOCKS_PER_SEC;
}

long long calc(double time) {
	return (long long)((TIMER * 10) / time);
}

void Draw(int height, long long max_val, long long val) {
	int s_count = (int)((double)val / (double)max_val * height);
	for (int i = 0; i < height; i++) {
		if (i < s_count) cout << "#"; else cout << " ";
	}
	cout << "\t" << (int)((double)val / (double)max_val * 100) << " %\n";
}

void Graph(vector<string> name, vector<long long> time) {
	char operation[4] = { '+','-','*','/' };
	int Draw_height = 60;
	long long mx = -1;
	for (int i = 0; i < time.size(); i++) {
		mx = max(mx, time[i]);
	}
	int t = 0;
	for (int i = 0; i < name.size(); i++) {

		if (i % 4 == 0) cout << "********************************************************************************************\n";
		cout << name[i] << operation[i % 4];

		for (int i = 0; i < (12 - name[i].size()); i++) {
			cout << " ";
		}
		Draw(Draw_height, mx, time[i]);
	}
}

int main() {
	vector<string> name;
	vector<long long> time;
	vector <pair <string, long long>> res;
	int a1 = 345435, b1 = 346436;
	long a2 = 234235346, b2 = 346436346;
	long long a3 = 674574357456, b3 = 457457474357326;
	double a4 = 5453.346346, b4 = 534.346436436;
	float a5 = 546.654645, b5 = 647.57567;
	char operation[4] = { '+','-','*','/' };
	string operations = "+-*/";
	cout << "Type | Operation |                                                             |percent %\n";
	for (int i = 0; i < 4; i++) {
		name.push_back("int       ");
		time.push_back(calc(getTime(operation[i], a1, b1)));
	}
	for (int i = 0; i < 4; i++) {
		name.push_back("long       ");
		time.push_back(calc(getTime(operation[i], a2, b2)));
	}
	for (int i = 0; i < 4; i++) {
		name.push_back("long long   ");
		time.push_back(calc(getTime(operation[i], a3, b3)));
	}
	for (int i = 0; i < 4; i++) {
		name.push_back("double      ");
		time.push_back(calc(getTime(operation[i], a4, b4)));
	}
	for (int i = 0; i < 4; i++) {
		name.push_back("float       ");
		time.push_back(calc(getTime(operation[i], a5, b5)));
	}
	Graph(name, time);
	return 0;
}

