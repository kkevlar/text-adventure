#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

struct _room_t
{
	char label[64];
	char paragraph[2048];
	int choiceIds[16];
	int propSetIds[16];
	bool propIsRelative[16];
	bool quick;

	int childRoomIds[8];
	int prop1[8];
	int prop2[8];
	int condition[8];
	bool is1Literal[8];
	bool is2Literal[8];
};
typedef struct _room_t room_t;

char* choices[1024];
char* propNames[1024];
int propVals[1024];
room_t rooms[2000];

int main()
{
	FILE* f = fopen("TheRoad.adv","r");
	while(1)
	{
		char c = getc(f);
		if(c == EOF)
			break;
		printf("%c",c);
	}
	printf("%d\n",getpid());
	while(1)
	{
		;
	}
}
