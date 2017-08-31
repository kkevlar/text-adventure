#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

enum _ct_type 
{
	EQUAL, 
	GREATER,
	LESS,
	EGAREATER,
	ELESS,
	NOT
};
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
// room_t rooms[2000];
char text[10000];
int ti = 0;
int chxi = 0;

int main()
{
	room_t crm;
	FILE* f = fopen("TheRoad.adv","r");
	crm.choices[0] = &text[1];
	while(1)
	{
		char c = getc(f);
		if(c == EOF)
		{
			text[++ti] = '\0';
			break;
		}
		else if(c == '\n')
		{
			text[++ti] = '\0';
			if(chxi+1 < 16)
			{
				crm.choices[++chxi] = &text[ti+1];
			}
		}
		else 
			text[++ti] = c;
		printf("%c",c);
	}
	printf("\n\n\n Now the real fun starts\n");
	for(int i = 0; i < chxi+1; i++)
	{
		printf("String %d is \"%s\"\n",i,crm.choices[i]);
	}
	printf("%d %d\n",ti,chxi);
/*	
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
*/
}
