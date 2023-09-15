///Plan - Produce a deck of cards 
/// - take seven random cards 
/// - find every combination of five cards from the seven cards
/// - check for each type of hand in decending order of value


#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>

#define DECK_SIZE 52
#define HAND_SIZE 7
#define PIPS 13
#define KING 13
#define QUEEN 12
#define JACK 11
#define ACE 1
#define STRAIGHT_HAND 5


#define ITERATIONS_NUMBER 1111111 //reasonable number of iterations

int ZERO = 0;

// defining datatype suit
typedef enum suit {Hearts, Clubs, Diamonds, Spades}suit;
// defining datatype card
typedef struct card {
                    suit su;
                    short pip;
                    }card;

//generating deck of 52 playing cards by assigning eacxh suit to a set of 13 cards
int createDeck(card cardDeck[])
{
    short i;
    for (i = 1; i <= DECK_SIZE; i++)
    {   
        if (i%13==0)
            cardDeck[i-1].pip = 13 ;
        else
            cardDeck[i-1].pip = i%13 ;

        if (i <= 13)
            cardDeck[i-1].su = Hearts;
        else if (i <= 26)
            cardDeck[i-1].su = Clubs;
        else if (i <= 39)
            cardDeck[i-1].su = Diamonds;
        else
            cardDeck[i-1].su = Spades;
    }
    
    return 0;
}

//Generating an array of seven random numbers between 0 and 51
void fill_unique(int array[], int length, int min, int max)
{
    int new_random;
    bool unique;
    for(int i = 0; i < length; i++)
    {
        do
        {
            new_random = (rand() % (max - min +1)) + min;
            unique = true;
            for (int j = 0; j< i;j++)
                if (array[j] == new_random) unique = false;
        }
        while(!unique);
        array[i] =new_random;

    }

}
//The ultimate code checking function for hands dealt and deck generated
int printCards(card cardDeck[], int numCards)
{

    int i;
    for (i = 0; i < numCards; i++)
    {
        short pip = cardDeck[i].pip;
        switch (cardDeck[i].su)
        {
        
        case Hearts:
            switch (pip)
            {
            case ACE:
                printf("Ace of Hearts\n");
                break;

            case KING:
                printf("King of Hearts\n");
                break;

            case QUEEN:
                printf("Queen of Hearts\n");
                break;

            case JACK:
                printf("Jack of Hearts\n");
                break;
            default:
                printf("%d of Hearts\n", cardDeck[i].pip);
                break;
            }
            break;
        case Clubs:
            switch (pip)
            {
            case ACE:
                printf("Ace of Clubs\n");
                break;

            case KING:
                printf("King of Clubs\n");
                break;

            case QUEEN:
                printf("Queen of Clubs\n");
                break;

            case JACK:
                printf("Jack of Clubs\n");
                break;
            default:
                printf("%d of Clubs\n", cardDeck[i].pip);
                break;
            }
            break;
        case Diamonds:
            switch (pip)
            {
            case ACE:
                printf("Ace of Diamonds\n");
                break;

            case KING:
                printf("King of Diamonds\n");
                break;

            case QUEEN:
                printf("Queen of Diamonds\n");
                break;

            case JACK:
                printf("Jack of Diamonds\n");
                break;
            default:
                printf("%d of Diamonds\n", cardDeck[i].pip);
                break;
            }
            break;
        case Spades:
            switch (pip)
            {
            case ACE:
                printf("Ace of Spades\n");
                break;

            case KING:
                printf("King of Spades\n");
                break;

            case QUEEN:
                printf("Queen of Spades\n");
                break;

            case JACK:
                printf("Jack of Spades\n");
                break;
            default:
                printf("%d of Spades\n", cardDeck[i].pip);
                break;
            }
            break;
        }
    }
    return 0;
}

//using array of seven numbers the cards are drawn from the equivalent deck position
int sevenHand(card cardDeck[], card hand[])
{
    //generate seven random numbers
    int a[7];   
    fill_unique(a,HAND_SIZE,0,51);
    int i;
    for (i = 0; i < HAND_SIZE; i++)
    {
        hand[i] = cardDeck[a[i]];
    }
    return 0;
}


// Produced every possible combination of 5 hands from the seven to test for straights
void fiveHand(card fiveCards[][STRAIGHT_HAND], card hand[]){
    int numarray[STRAIGHT_HAND] = {0,1,2,3,4};
    int i;
    card hands[STRAIGHT_HAND];
    for (i = 0; i < STRAIGHT_HAND; i++) {
        hands[i] = hand[numarray[i]];
    }
    memcpy(fiveCards[ZERO++], hands, STRAIGHT_HAND * sizeof(card));
    while(1){
        int j;
        
        for(j = STRAIGHT_HAND-1; j >= 0 && numarray[j] == 2 + j; j--);
            if(j<0)break;
            numarray[j]++;
            
        for(++j; j < STRAIGHT_HAND; j++){
            numarray[j] = numarray[j-1]+1;
        }
           
    for (i = 0; i < STRAIGHT_HAND; i++) {
        hands[i] = hand[numarray[i]];
    }
    memcpy(fiveCards[ZERO++], hands, STRAIGHT_HAND * sizeof(card));
    }
}


// Checks for at least one pair (the code will have already checked for two pair etc)
int onePair(card hand[])
{
    // tests to see if any index is equal to another
    int i,j;
    
    // Searching the hand for a pair
    for (i = 0; i < HAND_SIZE; i++)
        for (j = 0; j < HAND_SIZE; j++)
            if(j != i){
                if(hand[i].pip==hand[j].pip)return 1;
            }
    return 0;
}

// Checks for at least two pairs
int twoPair(card hand[])
{
    int i,j;
    int num =0;
    for (i = 0; i < HAND_SIZE; i++)
        for (j = 0; j < HAND_SIZE; j++)
            if(j != i){
                if(hand[i].pip==hand[j].pip){
                    num++;
                }
            }
    if (num >= 4) return 1; //method results in duplication and so num = 2x

    return 0;    
}

// Check for three of a kind
int threeOfaKind(card hand[])
{
    
    int i,j,k;
    int num =0;
    // Searching the hand for a pair
    for (i = 0; i < HAND_SIZE; i++)
        for (j = 0; j < HAND_SIZE; j++)
            for (k = 0; k < HAND_SIZE; k++)
            if(j != i && j != k && i != k){
                if(hand[i].pip==hand[j].pip && hand[k].pip==hand[j].pip && hand[i].pip==hand[k].pip){
                    num++;
                    //printf("\n");
                    //printCards(hand,7);
                }
            }
    if (num >= 6) return 1; //for loops result in num++ x6

    return 0;    

}


// Checks if full house
int fullHouse(card hand[]){
    int i,j,k;
    int num =0;
    // Searches for at least one three of a kind
    for (i = 0; i < HAND_SIZE; i++)
        for (j = 0; j < HAND_SIZE; j++)
            for (k = 0; k < HAND_SIZE; k++)
            if(j != i && j != k && i != k){
                if(hand[i].pip==hand[j].pip && hand[k].pip==hand[j].pip && hand[i].pip==hand[k].pip){
                    num++;
                    //printf("\n");
                    //printCards(hand,7);
                }
            }
    
    int n =0;
    // Searching the hand for two pairs
    for (i = 0; i < HAND_SIZE; i++)
        for (j = 0; j < HAND_SIZE; j++)
            if(j != i){
                if(hand[i].pip==hand[j].pip){
                    n++;
                }
            }
    if (num >= 6 && n >=8) return 1;

    return 0;    
    

}

// Checks for four of a kind using thee of a kind function
int fourOfaKind(card hand[])
{
    int i,j,k;
    int num =0;   
    // Searching the hand for a pair
    for (i = 0; i < HAND_SIZE; i++)
        for (j = 0; j < HAND_SIZE; j++)
            for (k = 0; k < HAND_SIZE; k++)
            if(j != i && j != k && i != k){
                if(hand[i].pip==hand[j].pip && hand[k].pip==hand[j].pip && hand[i].pip==hand[k].pip){
                    num++;
                    //printf("\n");
                    //printCards(hand,7);
                }
            }
    if (num >= 24) return 1; //if a hand contains four of a kind the three of a kind function will trigger four times

   

    return 0;
}

// Checks for flush by creating a count for each suit that increases when acard in that suit is found
int isFlush(card hand[], int hand_size){

    int numHearts= 0;
    int numClubs = 0;
    int numDiamonds = 0;
    int numSpades = 0;

    int i, suit;
    for (i = 0; i < hand_size; i++)
    {
        suit = hand[i].su;
        switch (suit)
        {
        case Hearts:
            numHearts++;
            if (numHearts == 5) // 5 hearts have been found within the hand
                return 1;
            break;
        case Clubs:
            numClubs++;
            if (numClubs == 5)
                return 1;
            break;
        case Diamonds:
            numDiamonds++;
            if (numDiamonds == 5)
                return 1;
            break;
        case Spades:
            numSpades++;
            if (numSpades == 5)
                return 1;
            break;
        }
    }
    return 0;
}

// Used in qsort https://www.tutorialspoint.com/c_standard_library/c_function_qsort.htm
int comparison(const void *a, const void *b)
{
    card *a_card = (card *)a;
    card *b_card = (card *)b;
    return (a_card->pip - b_card->pip);
}

// Tests for a straight
int testStraight(card hand[]){

    // qsort puts the hand in pip order
    qsort(hand, STRAIGHT_HAND, sizeof(card), comparison);
    if(hand[0].pip == ACE  && hand[1].pip == 10 && hand[2].pip == JACK && hand[3].pip == QUEEN && hand[4].pip == KING){    
        return 1;
    }
    int i;
    for(i = 0; STRAIGHT_HAND-1 > i; i++){
        if((hand[i+1].pip - hand[i].pip) != 1) return 0; //if any of the cards in the set of five are not one less than the adjacent - not a straight
        }       
        return 1;
    }

//the array of straights creates a binary flagging system for straights
void arrayOfstraights(card fiveCards[][STRAIGHT_HAND], int array01Straights[]){
    int i;
    for(i = 0; i<21; i++){
        if(testStraight(fiveCards[i]))
            array01Straights[i] = 1;
    }
}
// This method checks to see whether a hand has a straight in it.
int isStraight(int array01Straights[]){
    int i;
    for(i = 0; i<21; i++){
        if(array01Straights[i]) return 1;
    }
    return 0;
}


// Reads binary flagging system
int straightFlush(card fiveCards[][STRAIGHT_HAND], int array01Straights[]){

    int i;
    for(i = 0; i<21; i++){
        if(array01Straights[i]){
            
            if(isFlush(fiveCards[i], STRAIGHT_HAND)){
                //printCards(combos[i],5);
                //printf("\n");
                return 1;}
            }
        }
    
    return 0;
}


// Checks for royal flush by testing for straight then high straight then flush
int royalFlush(card fiveCards[][STRAIGHT_HAND], int array01Straights[]){
    int i;
    for(i = 0; i<21; i++){
        if(array01Straights[i]){
            int j;
            //printf("\n");
            //printCards(combos[i],5);
            
            if(fiveCards[i][4].pip == KING && fiveCards[i][0].pip == ACE)//checks for high straight
                if (isFlush(fiveCards[i], STRAIGHT_HAND)) 
                {   //printCards(combos[i],5);
                    //printf("\n");
                    return 1;}
        }
    }
    return 0;
}

int main(void){
    //create variables to count number of each type of hand
    double royalFlushcount = 0.0, straightFlushcount = 0.0, fourOfaKindcount = 0.0, fullHousecount = 0.0, flush = 0.0, straight = 0.0, threeOfaKindcount = 0.0, twoPaircount = 0.0, pair = 0.0 ,highCardCount = 0.0;
    
    card deck[DECK_SIZE];
    createDeck(deck);
    card hand[HAND_SIZE], fiveCards[21][STRAIGHT_HAND];
        int i, j;
    int array01Straights[21];
    for(i = 0; i<=ITERATIONS_NUMBER; i++){
        
        sevenHand(deck, hand);
        //print_cards(hand, HAND_SIZE);
        
        // zero all indices marking locations of straights
        for(j = 0; j<21; j++){
            array01Straights[j] = 0;
        }

        fiveHand(fiveCards,hand);

        arrayOfstraights(fiveCards, array01Straights);

        if(royalFlush(fiveCards, array01Straights)){
            royalFlushcount++;
        }

        else if(straightFlush(fiveCards, array01Straights)){
            straightFlushcount++;
        }

        else if(fourOfaKind(hand)){
            fourOfaKindcount++;
        }

        else if(fullHouse(hand)){
            fullHousecount++;
        }

        else if(isFlush(hand, HAND_SIZE)){
            flush++;
        }

        else if(isStraight(array01Straights)){
            straight++;
        }

        else if(threeOfaKind(hand)){
            threeOfaKindcount++;
        }

        else if(twoPair(hand)){
            twoPaircount++;
        }
        else if(onePair(hand)){
            pair++;
        }

        else highCardCount++;
        ZERO = 0;
    }

    printf("Royal Flush - %lf\n", royalFlushcount/ITERATIONS_NUMBER);
    printf("Straight Flush - %lf\n", straightFlushcount/ITERATIONS_NUMBER);
    printf("Four of a Kind - %lf\n", fourOfaKindcount/ITERATIONS_NUMBER);
    printf("Full House - %lf\n", fullHousecount/ITERATIONS_NUMBER);
    printf("Flush - %lf\n", flush/ITERATIONS_NUMBER);
    printf("Straight - %lf\n", straight/ITERATIONS_NUMBER);
    printf("Three of a Kind - %lf\n", threeOfaKindcount/ITERATIONS_NUMBER);
    printf("Two Pairs - %lf\n", twoPaircount/ITERATIONS_NUMBER);
    printf("Pair - %lf\n", pair/ITERATIONS_NUMBER);
    printf("High Card - %lf\n", highCardCount/ITERATIONS_NUMBER);
    printf("Total - %lf\n",(royalFlushcount+straightFlushcount+fourOfaKindcount+fullHousecount+threeOfaKindcount+flush+straight+twoPaircount+pair+highCardCount)/ITERATIONS_NUMBER);
    return 0;
}




// testing code
//   int main(void)
//   {
//       srand(time(NULL)*getpid());
//       int a[7]; 
       
//       fill_unique(a,7,0,51);
//       //for (int i=0;i<7;i++)
//           //printf("a[%d] = %d\n",i,a[i]);
     
      
//       card cardDeck[52];
//       init(cardDeck);
//       int j;
//       //for(j=0;j<52;j++) 
//          //printf("\n%d",cardDeck[j].pip);
//       //printCards(cardDeck,52);
//       card hand[HAND_SIZE];
//       dealHand(cardDeck, hand);
//       printCards(hand,7);
//       int i;
//       card combos[21][SUB_HAND];
//       int indices[21] = {0};
//       for(j = 0; j<21; j++){
//             indices[j] = 0;
//         }
        
//         // Get all possible combinations (7C5) of that hand
//         //card result[SUB_HAND];
//       combinations(combos,hand);
//       int k;
//       for(k=0;k<21;k++){
//         printf("\nCombo Number:%d\n",k+1);
//         printCards(combos[k],5);
//       }
//   }













