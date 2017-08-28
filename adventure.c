#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

enum _ct_type 
{
	EQUAL, 
	GREATER,
	LESS,
	GREATERE,
	LESSE,
	NOT
}
typedef enum _ct_type ct_type;

struct _room_t
{
	char* label;
	char* paragraph;

	char* choices[16];
	int* setProps[16];
	int modPropTo[16];
	bool propIsRelative[16];
	bool quick;

	int prop1[8];
	int prop2[8];
	ct_type condition[8];
	bool is1Literal[8];
	bool is2Literal[8];

	struct _room_t* children[16];
};
typedef struct _room_t room_t;

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
