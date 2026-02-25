#include <iostream>
#include <vector>
#include <set>
#include <algorithm>
using namespace std;

int n;
set<vector<int>> fundamental;

bool isSafe(int row, int col, vector<vector<int>>& board){
    for(int i = 0; i < row; i++){
        if(board[i][col] == 2){
            return false;
        }
    }

    for(int i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--){
        if(board[i][j] == 2){
            return false;
        }
    }

    for(int i = row - 1, j = col + 1; i >= 0 && j < n; i--, j++){
        if(board[i][j] == 2){
            return false;
        }
    }

    return true;
}

vector<int> rotate90(const vector<int>& b){
    vector<int> r(n);
    for(int i = 0; i < n; i++){
        r[b[i]] = n - 1 - i;
    }
    return r;
}

vector<int> reflect(const vector<int>& b){
    vector<int> r(n);
    for(int i = 0; i < n; i++){
        r[i] = n - 1 - b[i];
    }
    return r;
}

vector<int> canonical(vector<int> b){
    vector<vector<int>> forms;
    forms.push_back(b);

    vector<int> r1 = rotate90(b);
    vector<int> r2 = rotate90(r1);
    vector<int> r3 = rotate90(r2);

    forms.push_back(r1);
    forms.push_back(r2);
    forms.push_back(r3);

    forms.push_back(reflect(b));
    forms.push_back(reflect(r1));
    forms.push_back(reflect(r2));
    forms.push_back(reflect(r3));

    return *min_element(forms.begin(), forms.end());
}

void solve(int row, vector<vector<int>>& board, vector<int>& config){

    if(row == n){
        fundamental.insert(canonical(config));
        return;
    }

    for(int col = 0; col < n; col++){
        if(isSafe(row, col, board)){
            board[row][col] = 2;
            config[row] = col;

            solve(row + 1, board, config);

            board[row][col] = 0;
        }
    }
}

void printBoard(const vector<int>& config){
    for(int i = 0; i < n; i++){
        for(int j = 0; j < n; j++){
            if(config[i] == j){
                cout << "Q ";
            }else{
                cout << "- ";
            }
        }
        cout << endl;
    }
    cout << "======================================================\n";
}

int main(){
    cout << "Enter board size: ";
    cin >> n;

    vector<vector<int>> board(n, vector<int>(n, 0));
    vector<int> config(n);

    solve(0, board, config);

    cout << "\nSolutions: " << fundamental.size() << endl << endl;

    for(const auto& sol : fundamental){
        printBoard(sol);
    }

    return 0;
}