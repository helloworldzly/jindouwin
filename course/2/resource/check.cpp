#include <bits/stdc++.h>
#define LL long long
using namespace std;

const int maxn = 100000 + 10;
int a[maxn], d[maxn], f[maxn];
int l[maxn], r[maxn];
int n, tot;

void add(int u, int x) {
	for (; u <= tot; u += u & -u)
		f[u] += x;
}

int sum(int u) {
	int ret = 0;
	for (; u; u -= u & -u)
		ret += f[u];
	return ret;
}

int main() {
	while (scanf("%d", &n) == 1) {
		LL ret = 0;
		tot = 0;
		memset(f, 0, sizeof(f));
		for (int i = 1; i <= n; ++i) {
			scanf("%d", a + i);
			d[tot++] = a[i];
		}
		sort(d, d + tot);
		tot = unique(d, d + tot) - d;
		for (int i = 1; i <= n; ++i)
			a[i] = lower_bound(d, d + tot, a[i]) - d + 1;

		for (int i = n; i; --i) {
			int cnt = (n - i) - sum(a[i]);
			ret += 1LL * cnt * (cnt - 1) / 2;
			add(a[i], 1);
		}

		memset(f, 0, sizeof(f));
		for (int i = 1; i <= n; ++i) {
			l[i] = sum(a[i] - 1);
			add(a[i], 1);
		}
		memset(f, 0, sizeof(f));
		for (int i = n; i; --i) {
			r[i] = (n - i) - sum(a[i] - 1);
			add(a[i], 1);
		}
		for (int i = 1; i <= n; ++i)
			ret -= 1LL * l[i] * r[i];
		cout << ret << endl;
	}
}
